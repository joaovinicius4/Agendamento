import sqlite3
from pathlib import Path

def get_connection(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_database(connection: sqlite3.Connection) -> None:
    ddl_profissionais = """
    CREATE TABLE IF NOT EXISTS profissionais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especialidade TEXT NOT NULL
    );
    """
    connection.execute(ddl_profissionais)
    connection.commit()