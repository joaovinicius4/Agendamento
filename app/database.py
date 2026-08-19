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
    ddl_agendamentos = """
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_nome TEXT NOT NULL,
        profissional_id INTEGER NOT NULL,
        data_inicio TEXT NOT NULL,
        data_fim TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'agendado'
        CHECK (status IN ('agendado', 'cancelado')),
        FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
        CHECK (data_fim > data_inicio)
    );
    """

    connection.execute(ddl_profissionais)
    connection.execute(ddl_agendamentos)
    connection.commit()