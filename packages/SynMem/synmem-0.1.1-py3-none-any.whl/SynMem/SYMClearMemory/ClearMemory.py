import os
import sqlite3
import logging

logger = logging.getLogger(__name__)

class ClearMemory:
    def __init__(self, synmem):
        self.sm = synmem

    def clearPerception(self):
        self.sm.perception.clear()

    def clearFirstEntry(self, user):
        self._clearBy(user, 'MIN')

    def clearLastEntry(self, user):
        self._clearBy(user, 'MAX')

    def clearAllEntries(self, user):
        sen = self.sm.getDir(self.sm.senDir,                     f"{user}.db")
        stm = self.sm.getDir(self.sm.stmUserConversationDetails, "STM.db")
        ltm = self.sm.getDir(self.sm.ltmUserConversationDetails, "LTM.db")
        self._delete(sen, "DELETE FROM memory")
        self._delete(stm, "DELETE FROM memory WHERE user = ? COLLATE NOCASE", [user])
        self._delete(ltm, "DELETE FROM memory WHERE user = ? COLLATE NOCASE", [user])

    def _clearBy(self, user, which):
        sen = self.sm.getDir(self.sm.senDir,                     f"{user}.db")
        stm = self.sm.getDir(self.sm.stmUserConversationDetails, "STM.db")
        ltm = self.sm.getDir(self.sm.ltmUserConversationDetails, "LTM.db")
        self._delete(sen, f"DELETE FROM memory WHERE id = (SELECT {which}(id) FROM memory)")
        self._delete(stm,
            f"DELETE FROM memory WHERE id = (SELECT {which}(id) FROM memory WHERE user = ? COLLATE NOCASE)",
            [user]
        )
        self._delete(ltm,
            f"DELETE FROM memory WHERE id = (SELECT {which}(id) FROM memory WHERE user = ? COLLATE NOCASE)",
            [user]
        )

    def _delete(self, dbPath, query, params=None):
        if not os.path.exists(dbPath):
            return
        try:
            with self.sm.dbLock, sqlite3.connect(dbPath) as conn:
                conn.execute(query, params or [])
                conn.commit()
        except Exception:
            logger.exception(f"_delete failed on {dbPath}")
