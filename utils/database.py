###############################################
#
# File: utils.database
# Date: 09/03/2026 (EU)
# Date Edited: 03/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import discord
import asyncio
import sqlite3

databases = {
    "banished": [
        {"table_name": "banished_ids", "data": "user_id INT"},
        {"table_name": "banished_words_bypasses", "data": "bypass TEXT"},
        {"table_name": "banished_flagmsg", "data": "word TEXT"},
        {"table_name": "banished_words_noignore", "data": "word TEXT, message TEXT"},
        {"table_name": "banished_words", "data": "word TEXT, message TEXT"},
    ],
    # "other_stuff": [
    #     {"table_name": "jobs", "data": "id INTEGER, job TEXT, wage REAL"}
    # ],
    "user_data": [
        {"table_name": "pings", "data": "user_id INT, allowed INT"},
        {"table_name": "afk_users", "data": "user_id INT, name TEXT, message TEXT, since TEXT, toggle INT"},
        {"table_name": "cooldowns", "data": "user_id INT, since TEXT"},
        {"table_name": "user_data", "data": "used INT, user_id INT, alise TEXT, job TEXT, tokens INT, wallet INT, bank INT"}
    ]
}

class Database():
    def __init__(cls, *args, **kargs):
        super().__init__(*args, **kargs)
        
    @classmethod
    def init(cls):
        ## Create databases
        if not os.path.exists(f"data"):
            os.mkdir("data")
        
        for database in databases:
            # Exists? Check if all tables exist.
            if os.path.exists(f"data/{database}.db"):
                conn = sqlite3.connect(f"data/{database}.db")
                
                for table in databases[database]:
                    data = conn.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table['table_name']}'")
                    
                    if data.fetchone()[0] < 1:
                        conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")

                conn.close()
            else:
                conn = sqlite3.connect(f"data/{database}.db")

                for table in databases[database]:
                    conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")
                    ## 21/03/2026 - kmskmskmskms
                    # if table["table_name"] == "jobs":
                    #     conn.execute(f'CREATE TABLE {table['table_name']} ({table['data']}) (PRIMARY KEY("id" AUTOINCREMENT))')
                    # else:
                    #     conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")
                
                conn.close()
        
        cls.banished_conn = sqlite3.connect(f"data/banished.db", timeout=30, check_same_thread=False)
        cls.jobs_conn = sqlite3.connect(f"data/jobs.db", timeout=30, check_same_thread=False)
        cls.userdata_conn = sqlite3.connect(f"data/user_data.db", timeout=30, check_same_thread=False)
        
        cls.banished_conn.execute("PRAGMA journal_mode=WAL;")
        cls.jobs_conn.execute("PRAGMA journal_mode=WAL;")
        cls.userdata_conn.execute("PRAGMA journal_mode=WAL;")
        
    banished_conn = None
    jobs_conn = None
    userdata_conn = None

    db_lock = asyncio.Lock()

    @classmethod
    async def execute(self, database: str, query, params=()):
        # async with self.db_lock:
        conn = None
        if database.lower() == "banished":
            conn = Database.banished_conn
        elif database.lower == "jobs":
            conn = Database.jobs_conn
        elif database.lower() == "userdata":
            conn = Database.userdata_conn

            
        if conn != None:
            conn.execute(query, params)
            conn.commit()

    @classmethod
    def fetchone(self, database: str, query, params=()):
        conn = None
        if database.lower() == "banished":
            conn = Database.banished_conn
        elif database.lower == "jobs":
            conn = Database.jobs_conn
        elif database.lower() == "userdata":
            conn = Database.userdata_conn

            
        if conn != None:
            cur = conn.execute(query, params)
            return cur.fetchone()
        return []

    @classmethod
    def fetchall(self, database: str, query, params=()):
        # async with self.db_lock:
        conn = None
        if database.lower() == "banished":
            conn = Database.banished_conn
        elif database.lower == "jobs":
            conn = Database.jobs_conn
        elif database.lower() == "userdata":
            conn = Database.userdata_conn

            
        if conn != None:
            cur = conn.execute(query, params)
            return cur.fetchall()
        return []
            
    def allow_ping(id: int):
        ping = Database.userdata_conn.execute(f"SELECT * FROM pings WHERE user_id={id}").fetchone()

        if ping == None:
            Database.userdata_conn.execute(f'INSERT INTO pings VALUES ({id}, {int("1")})')
            Database.userdata_conn.commit()
            ping = Database.userdata_conn.execute(f"SELECT * FROM pings WHERE user_id={id}").fetchone()
            
        if ping[1] == 1:
            return True
        
        return False
        

    def get_jobs():
        jobs_raw = Database.fetchall("jobs", "SELECT * FROM jobs ORDER BY job ASC")

        result = {
            "jobs": []
        }

        for job in jobs_raw:
            result["jobs"].append({
                "job": job[1],
                "wage": job[2]
            })
            
        return result


    def get_afks():
        users_raw = Database.fetchall("userdata", "SELECT * FROM afk_users")

        result = {
            "users": []
        }

        for user in users_raw:
            result['users'].append({
                'user_id': user[0],
                'name': user[1],
                'message': user[2],
                'since': user[3]
            })

        return result
    
    def get_banished():
        resultBanishedIds = Database.fetchall("banished", "SELECT * FROM banished_ids")
        resultBypassesRaw = Database.fetchall("banished", "SELECT * FROM banished_words_bypasses")
        resultFlagMsgRaw = Database.fetchall("banished", "SELECT * FROM banished_flagmsg")
        resultNoIgnoreRaw = Database.fetchall("banished", "SELECT * FROM banished_words_noignore")
        resultBanishedWordsRaw = Database.fetchall("banished", "SELECT * FROM banished_words")

        result = {
            "ids": [],
            "bypasses": [],
            "flagmsg": [],
            "noignore": {},
            "words": {}
        }

        for id in resultBanishedIds:
            result['ids'].append(id[0])
        for bypass in resultBypassesRaw:
            result['bypasses'].append(bypass[0])
        for flag in resultFlagMsgRaw:
            result['flagmsg'].append(flag[0])

        for noignore in resultNoIgnoreRaw:
            result["noignore"][noignore[0]] = noignore[1]
        for banished in resultBanishedWordsRaw:
            result["words"][banished[0]] = banished[1]
        
        return result
