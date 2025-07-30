import os
import sqlite3
from datetime import datetime
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class RetrieveMemory:
    def __init__(self, synmem):
        self.sm = synmem

    def retrievePerception(self):
        return "\n".join(self.sm.perception) if self.sm.perception else "No Perception Feedback Available."

    def retrieveMemoryFromDb(self, dbFile, query, params, returnTimestampOnly=False):
        out = []
        if not os.path.exists(dbFile):
            return out
        try:
            with self.sm.dbLock, sqlite3.connect(dbFile) as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                for row in cur.fetchall():
                    if returnTimestampOnly:
                        out.append(row[0])
                    else:
                        ts, content = row[0], row[1]
                        resp = row[2] if len(row) > 2 else ""
                        out.append((ts, content, resp))
        except Exception:
            logger.exception(f"retrieveMemoryFromDb failed on {dbFile}")
        return out

    def retrieveDetailsFromDb(self, dbFile, query, params):
        out = []
        if not os.path.exists(dbFile):
            return out
        with self.sm.dbLock, sqlite3.connect(dbFile) as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            for ts, content in cur.fetchall():
                out.append((ts, content))
        return out

    def retrieveSensory(self, path):
        return self.retrieveMemoryFromDb(path,
            'SELECT dtStamp, content, response FROM memory', [])

    def retrieveConversationDetails(self, user, paths, startDate=None, endDate=None):
        dbs = [self.sm.getDir(p, fn) for p, fn in zip(paths, ("STM.db","LTM.db"))]
        q = 'SELECT dtStamp, content, response FROM memory WHERE user = ? COLLATE NOCASE'
        ps = [user]
        if startDate:
            ps.append(self.sm.formatIsoDate(startDate))
            q += ' AND dtStamp >= ?'
        if endDate:
            ps.append(self.sm.formatIsoDate(endDate))
            q += ' AND dtStamp <= ?'
        mem = []
        for db in dbs:
            mem += self.retrieveMemoryFromDb(db, q, ps)
        return mem

    def retrieveInteractionDetails(self, paths, startDate=None, endDate=None):
        dbs = [self.sm.getDir(p, "Details.db") for p in paths]
        q = 'SELECT dtStamp, content FROM memory WHERE 1=1'
        ps = []
        if startDate:
            ps.append(self.sm.formatIsoDate(startDate)); q += ' AND dtStamp >= ?'
        if endDate:
            ps.append(self.sm.formatIsoDate(endDate));   q += ' AND dtStamp <= ?'
        mem = []
        for db in dbs:
            mem += self.retrieveDetailsFromDb(db, q, ps)
        return mem

    def retrieveLastInteractionTime(self, user, paths):
        cfg = [
            (f"{user}.db",    'SELECT dtStamp FROM memory ORDER BY dtStamp DESC LIMIT 1', []),
            ("STM.db",        'SELECT dtStamp FROM memory WHERE user = ? COLLATE NOCASE ORDER BY dtStamp DESC LIMIT 1', [user]),
            ("LTM.db",        'SELECT dtStamp FROM memory WHERE user = ? COLLATE NOCASE ORDER BY dtStamp DESC LIMIT 1', [user])
        ]
        for (fn, q, ps), base in zip(cfg, paths):
            db = self.sm.getDir(base, fn)
            ts = self.retrieveMemoryFromDb(db, q, ps, returnTimestampOnly=True)
            if ts:
                try:
                    return datetime.now() - datetime.fromisoformat(ts[0])
                except ValueError:
                    logger.warning(f"Bad timestamp: {ts[0]}")
        return datetime.now() - self.sm.sessionStart

    def retrieveLastInteractionDate(self, user, paths):
        cfg = [
            (f"{user}.db",    'SELECT dtStamp FROM memory ORDER BY dtStamp DESC LIMIT 1', []),
            ("STM.db",        'SELECT dtStamp FROM memory WHERE user = ? COLLATE NOCASE ORDER BY dtStamp DESC LIMIT 1', [user]),
            ("LTM.db",        'SELECT dtStamp FROM memory WHERE user = ? COLLATE NOCASE ORDER BY dtStamp DESC LIMIT 1', [user])
        ]
        for (fn, q, ps), base in zip(cfg, paths):
            db = self.sm.getDir(base, fn)
            ts = self.retrieveMemoryFromDb(db, q, ps, returnTimestampOnly=True)
            if ts:
                try:
                    return datetime.fromisoformat(ts[0])
                except ValueError:
                    logger.warning(f"Bad timestamp: {ts[0]}")
        return self.sm.sessionStart

    def retrieveImageDetails(self, paths, startDate=None, endDate=None):
        dbs = [self.sm.getDir(p, "Details.db") for p in paths]
        q = 'SELECT dtStamp, content FROM memory WHERE 1=1'
        ps = []
        if startDate:
            ps.append(self.sm.formatIsoDate(startDate)); q += ' AND dtStamp >= ?'
        if endDate:
            ps.append(self.sm.formatIsoDate(endDate));   q += ' AND dtStamp <= ?'
        mem = []
        for db in dbs:
            mem += self.retrieveDetailsFromDb(db, q, ps)
        return mem

    def retrieveCreatedImage(self, directory, imageName):
        date = datetime.strptime(imageName[:10], "%Y-%m-%d")  # if you prefix filenames with date
        imgPath = self.sm.getDir(directory,
                                 date.strftime("%Y").lower(),
                                 date.strftime("%m"),
                                 date.strftime("%d").lower(),
                                 f"{imageName}.png")
        if os.path.exists(imgPath):
            Image.open(imgPath).show()
            return imgPath
        else:
            logger.warning(f"Image not found: {imgPath}")
            return f"Image not found: {imgPath}"
