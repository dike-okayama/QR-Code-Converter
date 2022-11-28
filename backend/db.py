#!python3.10
# -*- coding: utf-8 -*-

import os
from contextlib import closing
import sqlite3


__this__ = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(__this__, "log.db")


if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("CREATE TABLE Log(id INTEGER PRIMARY KEY time ")
