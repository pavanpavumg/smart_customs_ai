import sqlite3
import datetime
import logging
import pandas as pd

DB_NAME = "risk_logs.db"

def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS risk_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    scenario TEXT,
                    verdict TEXT,
                    impact INTEGER,
                    likelihood INTEGER,
                    risk_score INTEGER
                )
            """)
    except sqlite3.Error as e:
        logging.error(f"Failed to initialize database: {e}")

def save_verdict(scenario, verdict, impact=1, likelihood=1):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_score = impact * likelihood 

    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO risk_logs 
                (timestamp, scenario, verdict, impact, likelihood, risk_score) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (now, scenario, verdict, impact, likelihood, total_score))
    except sqlite3.Error as e:
        logging.error(f"Failed to save verdict to database: {e}")

def get_all_logs():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            # We use pandas directly to read the SQL table into a Dashboard-ready format
            df = pd.read_sql_query("SELECT * FROM risk_logs ORDER BY timestamp DESC", conn)
            return df
    except Exception as e:
        logging.error(f"Failed to fetch logs: {e}")
        return pd.DataFrame() # Return empty DataFrame on failure so app doesn't crash

# Automatically initialize the database whenever this file is imported
init_db()
