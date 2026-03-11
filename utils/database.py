import os
import sqlite3

databases = [
    "afk",
    "banished"
]

class Database():
    def __init__(*args, **kargs):
        super().__init__(*args, **kargs)
        
    def create_databases(logger):
        for database in databases:
            doStuff = True

            if os.path.exists(f"misc/{database}.db"):
                doStuff = False
            
            conn = sqlite3.connect(f"misc/{database}.db")

            if database == "afk":
                if doStuff:
                    cursor = conn.cursor()
                
                    cursor.execute(f"CREATE TABLE users (name TEXT, user_id INT, return_message BOOL, message TEXT, since TEXT)")
                    conn.commit()
                conn.close()
            elif database == "banished":
                if doStuff:
                    cursor = conn.cursor()
                
                    cursor.execute(f"CREATE TABLE banished_ids (user_id INT)")
                    cursor.execute(f"CREATE TABLE banished_words_bypasses (bypass TEXT)")
                    cursor.execute(f"CREATE TABLE banished_flagmsg (word TEXT)")
                    cursor.execute(f"CREATE TABLE banished_words_noignore (word TEXT, message TEXT)")
                    cursor.execute(f"CREATE TABLE banished_words (word TEXT, message TEXT)")
                    conn.commit()
                conn.close()
            else:
                if doStuff:
                    conn.close()

    def get_afks():
        conn = sqlite3.connect(f"misc/afk.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        usersRaw = cursor.fetchall()

        conn.close()

        result = {
            "users": []
        }

        for user in usersRaw:
            result['users'].append({
                'name': user[0],
                'user_id': user[1],
                'return_message': user[2],
                'message': user[3],
                'since': user[4]
            })

        return result
    
    def get_banished():
        conn = sqlite3.connect(f"misc/banished.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM banished_ids")
        resultBanishedIds = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_bypasses")
        resultBypassesRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_flagmsg")
        resultFlagMsgRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_noignore")
        resultNoIgnoreRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words")
        resultBanishedWordsRaw = cursor.fetchall()

        conn.close()

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


    
    # def create_database(logger, filename: str, table_data: {}):
    #     path = os.path.abspath(f"data/{filename}.db")
    #     if os.path.exists(path):
    #         logger.info(f"The database with the file name {filename}.db in data already exists.")
    #     else:
    #         conn = sqlite3.connect(path)

    #         if len(table_data) > 0:
    #             cursor = conn.cursor()
    #             for data in table_data:
    #                 print(data)
    #                 cursor.execute(f"CREATE TABLE {table_data[data]['table_name']} {table_data[data]['table_values']}")
    #                 conn.commit()

    #         conn.close()
    