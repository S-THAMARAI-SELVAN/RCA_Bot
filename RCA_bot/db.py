import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_FILE = os.path.join(DB_FOLDER, "rca.db")

os.makedirs(DB_FOLDER, exist_ok=True)


def create_table():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_failures(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        failure_log TEXT,

        success_log TEXT,

        git_diff TEXT,

        rca_report TEXT

    )
    """)

    conn.commit()
    conn.close()


def save_failure(
    timestamp,
    failure_log,
    success_log,
    git_diff,
    rca_report
):

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pipeline_failures(

        timestamp,

        failure_log,

        success_log,

        git_diff,

        rca_report

    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        timestamp,
        failure_log,
        success_log,
        git_diff,
        rca_report
    ))

    conn.commit()
    conn.close()

    print("Data Stored In SQLite")


create_table()