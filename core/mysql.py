import sqlite3
import discord


conn = sqlite3.connect("data/ema.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS guilds(id INTEGER, type TEXT, value TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS whitelist(id INTEGER)""")

def insert_data_entry(id, type, value):
    cur.execute("""INSERT INTO guilds(id, type, value) VALUES (?, ?, ?)""", (id, type, value))
    conn.commit()

def read_data_entry(id, type):
    cur.execute("""SELECT value FROM guilds WHERE id=(?) AND type=(?)""", (id, type))
    val = None
    try:
        val = cur.fetchone()[0]
    except:
        if type == "greet-message":
            insert_data_entry(id, type, None)
            val = None
        elif type == "leave-message":
            insert_data_entry(id, type, None)
            val = None
        elif type == "join-leave-channel":
            insert_data_entry(id, type, None)
            val = None
        elif type == "join-role":
            insert_data_entry(id, type, None)
            val = None

    return val

def update_data_entry(id, type, value):
    exists = read_data_entry(id, type)
    cur.execute("""UPDATE guilds SET value=(?) WHERE id=(?) AND type=(?)""", (value, id, type))
    conn.commit()

def delete_data_entry(id, type):
    cur.execute("""DELETE FROM guilds WHERE id=(?) AND type=(?)""", (id, type))
    conn.commit()



create_tables()
