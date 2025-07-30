import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

class ViewMemory:
    def __init__(self, synmem):
        self.sm = synmem

    def viewDatabase(self, path, limit=None):
        return self._viewTable(path, "memory", limit)

    def viewDetailsDatabase(self, path, limit=None):
        return self._viewTable(path, "memory", limit)

    def _viewTable(self, path, table, limit):
        if not os.path.exists(path):
            logger.warning(f"Not found: {path}")
            return []
        try:
            with self.sm.dbLock, sqlite3.connect(path) as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                if not cur.fetchone():
                    return []
                cur.execute(f"PRAGMA table_info({table})")
                cols = [c[1] for c in cur.fetchall()]
                q = f"SELECT * FROM {table}"
                if limit:
                    q += f" ORDER BY id DESC LIMIT {limit}"
                cur.execute(q)
                return [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            logger.exception(f"viewDatabase failed on {path}")
            return []
