import os
import sqlite3
import shutil
import threading
import time
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

class MemoryMaintenance:
    def __init__(self, synmem):
        self.sm = synmem

    def startAutoMaintenance(self, interval=5*60):
        def loop():
            while True:
                self._performChecks()
                time.sleep(interval)
        threading.Thread(target=loop, daemon=True).start()

    def performStartupChecks(self, delay=1):
        for fn in (
            lambda: self.removeOldSensory(),
            # …
        ):
            fn(); time.sleep(delay)

    def _performChecks(self):
        for fn in (
            lambda: self.archiveConversationDetails(),
            lambda: self.archiveInteractionDetails(),
            lambda: self.archiveImageDetails(),
        ):
            fn(); time.sleep(1)

    def checkDatabases(self, sourceDir, mtimeFunc, action, expireDelta):
        if not sourceDir or not os.path.exists(sourceDir):
            return
        for root, _, files in os.walk(sourceDir):
            for f in files:
                fp = self.sm.getDir(root, f)
                if datetime.now() - mtimeFunc(fp) > expireDelta:
                    action(fp, f)

    def moveDatabase(self, src, dst, createSQL, selectSQL, insertSQL):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with self.sm.dbLock, sqlite3.connect(dst) as conn:
            conn.execute(createSQL); conn.commit()
        try:
            with self.sm.dbLock, sqlite3.connect(src) as sconn:
                scur = sconn.cursor()
                scur.execute(selectSQL)
                rows = scur.fetchall()
                if not rows: return
                with sqlite3.connect(dst) as dconn:
                    dcur = dconn.cursor()
                    dcur.executemany(insertSQL, rows)
                    dconn.commit()
                scur.execute("PRAGMA table_info(memory)")
                cols = [c[1] for c in scur.fetchall()]
                if "user" in cols:
                    scur.executemany(
                        "DELETE FROM memory WHERE user = ? AND dtStamp = ?",
                        [(r[0],r[1]) for r in rows]
                    )
                else:
                    scur.executemany(
                        "DELETE FROM memory WHERE dtStamp = ?",
                        [(r[0],) for r in rows]
                    )
        except Exception:
            logger.exception(f"moveDatabase failed from {src} to {dst}")

    def removeOldSensory(self):
        self.checkDatabases(
            self.sm.senDir,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            lambda f,_: os.remove(f),
            self.sm.getTimedelta(self.sm.sensoryExpireUnit, self.sm.sensoryExpireValue)
        )

    def removeOldInteractionDetails(self):
        self.checkDatabases(
            self.sm.stmUserInteractionDetails,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            lambda f,_: os.remove(f),
            self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
        )

    def removeOldImageDetails(self):
        self.checkDatabases(
            self.sm.stmCreatedImageDetails,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            lambda f,_: os.remove(f),
            self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
        )

    def removeOldConversationDetails(self):
        db = self.sm.getDir(self.sm.senDir, "STM.db")
        if os.path.exists(db):
            thresh = datetime.now() - self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
            with self.sm.dbLock, sqlite3.connect(db) as conn:
                conn.execute("DELETE FROM memory WHERE dtStamp <= ?", (thresh.isoformat(),))
                conn.commit()

    def archiveConversationDetails(self):
        self.checkDatabases(
            self.sm.stmUserConversationDetails,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            self.moveConversationDetails,
            self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
        )

    def archiveInteractionDetails(self):
        self.checkDatabases(
            self.sm.stmUserInteractionDetails,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            self.moveInteractionDetails,
            self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
        )

    def archiveImageDetails(self):
        self.checkDatabases(
            self.sm.stmCreatedImageDetails,
            lambda f: datetime.fromtimestamp(os.path.getmtime(f)),
            self.moveImageDetails,
            self.sm.getTimedelta(self.sm.memoryExpireUnit, self.sm.memoryExpireValue)
        )

    def archiveCreatedImages(self):
        expire = self.sm.getTimedelta(self.sm.imageExpireUnit, self.sm.imageExpireValue)
        base = self.sm.stmCreatedImages
        if base and os.path.exists(base):
            for root,_,files in os.walk(base):
                for f in files:
                    if not f.lower().endswith(".png"):
                        continue
                    fp = self.sm.getDir(root,f)
                    if datetime.now() - datetime.fromtimestamp(os.path.getmtime(fp)) > expire:
                        rel = os.path.relpath(fp, base)
                        dst = self.sm.getDir(self.sm.ltmCreatedImages, rel)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.move(fp, dst)

    def moveConversationDetails(self, srcFile, _):
        dst = self.sm.getDir(self.sm.ltmUserConversationDetails, "LTM.db")
        selectSQL = "SELECT user, dtStamp, content, response FROM memory"
        self.sm.createMemoryDatabase(dst)
        self.moveDatabase(
            srcFile, dst,
            '''CREATE TABLE IF NOT EXISTS memory (
                   id INTEGER PRIMARY KEY, user TEXT, dtStamp TEXT, content TEXT, response TEXT)''',
            selectSQL,
            'INSERT INTO memory (user,dtStamp,content,response) VALUES (?,?,?,?)'
        )

    def moveInteractionDetails(self, srcFile, fname):
        self.sm.createDetailsDatabase(srcFile)
        dst = self.sm.getDir(self.sm.ltmUserInteractionDetails, fname)
        self.moveDatabase(
            srcFile, dst,
            'CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, dtStamp TEXT, content TEXT)',
            'SELECT dtStamp, content FROM memory',
            'INSERT INTO memory (dtStamp,content) VALUES (?,?)'
        )

    def moveImageDetails(self, srcFile, fname):
        self.sm.createDetailsDatabase(srcFile)
        dst = self.sm.getDir(self.sm.ltmCreatedImageDetails, fname)
        self.moveDatabase(
            srcFile, dst,
            'CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, dtStamp TEXT, content TEXT)',
            'SELECT dtStamp, content FROM memory',
            'INSERT INTO memory (dtStamp,content) VALUES (?,?)'
        )
