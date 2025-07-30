
import os
import sqlite3
import threading
from datetime import datetime
from PIL import Image
from pathlib import Path
import numpy as np
import logging

logger = logging.getLogger(__name__)

class SparkMemory:
    def __init__(self, synmem):
        self.sm = synmem
        self.embeddingModel = self.sm.embeddingModel  # Initial value

    def setEmbeddingModel(self, model):
        self.embeddingModel = model

    def semanticSearch(self, query, paths: list, user: str = None, topK=5):
        model = self.embeddingModel or getattr(self.sm, 'embeddingModel', None)
        if model is None:
            raise ValueError("Embedding model not set. Use synmem.setEmbeddingModel(model).")

        # Collect all (id, content, response, dbPath) rows across all paths, filtered by user if given
        rows = []
        for path in paths:
            dbFiles = []
            # Each path can be a directory or a specific DB file
            if os.path.isdir(path):
                # Look for *.db files in the directory
                dbFiles = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.db')]
            elif os.path.isfile(path):
                dbFiles = [path]
            else:
                continue

            for dbFile in dbFiles:
                # Figure out if this db has a 'user' column
                try:
                    with sqlite3.connect(dbFile) as conn:
                        cursor = conn.cursor()
                        cursor.execute("PRAGMA table_info(memory)")
                        cols = [col[1] for col in cursor.fetchall()]
                    if 'user' in cols and user:
                        query_str = "SELECT id, content, response FROM memory WHERE user = ? COLLATE NOCASE"
                        params = [user]
                    else:
                        query_str = "SELECT id, content, response FROM memory"
                        params = []
                    # Get rows
                    db_rows = self.sm.retrieveMemoryFromDb(dbFile, query_str, params)
                    for row in db_rows:
                        # row[0]=timestamp, row[1]=content, row[2]=response
                        # Attach DB context for trace/debug, but only id/content for semantic search
                        rows.append((f"{dbFile}:{row[0]}", row[1], row[2] if len(row) > 2 else ""))
                except Exception as ex:
                    logger.warning(f"Error reading for semantic search: {dbFile}: {ex}")
                    continue

        if not rows:
            return []

        # Prepare contents for embedding
        contents = [content for (_, content, _) in rows]
        entry_embeddings = model.encode(contents)
        query_embedding = model.encode([query])[0]
        # Calculate cosine similarity
        scores = np.dot(entry_embeddings, query_embedding) / (
            np.linalg.norm(entry_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        # Sort by score
        top_indices = np.argsort(scores)[::-1][:topK]
        results = [(rows[i][0], rows[i][1], rows[i][2], float(scores[i])) for i in top_indices]
        return results