import sqlite3

def create_professional(
    connection: sqlite3.Connection,
    nome: str,
    especialidade: str,
) -> dict[str, int | str]:
    cursor = connection.execute(
        "INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)",
        (nome, especialidade),
    )
    connection.commit()

    return {
        "id": cursor.lastrowid,
        "nome": nome,
        "especialidade": especialidade,
    }

def list_professionals(
    connection: sqlite3.Connection,
) -> list[dict[str, int | str]]:
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        "SELECT id, nome, especialidade FROM profissionais ORDER BY id"
    ).fetchall()

    return [dict(row) for row in rows]





