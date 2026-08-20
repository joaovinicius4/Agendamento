import sqlite3
from pathlib import Path
from app.database import get_connection, initialize_database

def test_initialize_database_creates_profissionais_table(tmp_path: Path):
    test_db_path = tmp_path / "test_agendamento.db"
    conn = get_connection(test_db_path)
    initialize_database(conn)
    
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='profissionais';"
    )
    resultado = cursor.fetchone()
    
    assert resultado is not None
    assert resultado[0] == "profissionais"

    cursor.execute(
        "SELECT name FROM sqlite_master Where type ='table' AND name ='agendamentos';"
    )
    resultado = cursor.fetchone()

    assert resultado is not None
    assert resultado[0] == "agendamentos"

    conn.close()