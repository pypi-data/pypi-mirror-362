import os
import sqlite3
from datetime import datetime
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class SaveMemory:
    def __init__(self, synmem):
        self.sm = synmem

    def savePerception(self, ctx: str):
        if len(self.sm.perception) >= self.sm.perceptionLimit:
            self.sm.perception.pop(0)
        self.sm.perception.append(ctx)

    def saveData(self, path, ctx, response=None):
        self.sm.ensureDir(path)
        ts = datetime.now().isoformat()
        content = (
            ctx.decode('utf-8', errors='replace') if isinstance(ctx, bytes)
            else ctx if isinstance(ctx, str)
            else str(ctx)
        )
        try:
            with self.sm.dbLock, sqlite3.connect(path) as conn:
                cur = conn.cursor()
                cur.execute("PRAGMA table_info(memory)")
                cols = [c[1] for c in cur.fetchall()]
                if 'response' in cols:
                    cur.execute(
                        'INSERT INTO memory (dtStamp, content, response) VALUES (?, ?, ?)',
                        (ts, content, response)
                    )
                else:
                    cur.execute(
                        'INSERT INTO memory (dtStamp, content) VALUES (?, ?)',
                        (ts, content)
                    )
                conn.commit()
        except Exception:
            logger.exception(f"saveData failed on {path}")

    def saveSensory(self, ctx, response, user, path):
        self.sm.ensureDir(path)
        db = self.sm.getDir(path, f"{user}.db")
        self.sm.createPersonalDatabase(db)
        with self.sm.dbLock, sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM memory')
            if cur.fetchone()[0] >= self.sm.sensoryLimit:
                cur.execute('DELETE FROM memory WHERE id = (SELECT MIN(id) FROM memory)')
                conn.commit()
        self.saveData(db, ctx, response)

    def saveConversationDetails(self, ctx, response, user, path):
        db = self.sm.getDir(path, "STM.db")
        self.sm.ensureDir(db)
        self.sm.createMemoryDatabase(db)
        ts = datetime.now().isoformat()
        content = (
            ctx.decode('utf-8', errors='replace') if isinstance(ctx, bytes)
            else ctx if isinstance(ctx, str)
            else str(ctx)
        )
        try:
            with self.sm.dbLock, sqlite3.connect(db) as conn:
                conn.execute(
                    "INSERT INTO memory (user, dtStamp, content, response) VALUES (?, ?, ?, ?)",
                    (user, ts, content, response)
                )
                conn.commit()
        except Exception:
            logger.exception(f"saveConversationDetails failed on {db}")

    def saveInteractionDetails(self, user, path):
        db = self.sm.getDir(path, "Details.db")
        self.sm.ensureDir(db)
        self.sm.createDetailsDatabase(db)
        self.saveData(db, user)

    def saveImageDetails(self, subject, path):
        db = self.sm.getDir(path, "Details.db")
        self.sm.ensureDir(db)
        self.sm.createDetailsDatabase(db)
        self.saveData(db, subject)

    def setImageDir(self, base):
        now = datetime.now()
        return self.sm.getDir(base,
            now.strftime("%Y").lower(),
            now.strftime("%m"),
            now.strftime("%d").lower()
        )

    def getNextAvailableFilename(self, directory, baseName, extension=".png"):
        counter = 1
        while True:
            fn = f"{baseName}{counter}{extension}"
            fp = self.sm.getDir(directory, fn)
            if not os.path.exists(fp):
                return fn
            counter += 1

    def saveCreatedImage(self, subject, imageData, path1, path2):
        img = Image.open(BytesIO(imageData.content))
        dir_ = self.setImageDir(path1)
        self.sm.ensureDir(dir_)
        fn = self.getNextAvailableFilename(dir_, subject)
        fp = self.sm.getDir(dir_, fn)
        self.sm.ensureDir(fp)
        self.saveImageDetails(fn, path2)
        img.save(fp)
        img.show()
