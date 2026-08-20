import sqlite3
from datetime import datetime

def create_appointment(
    connection: sqlite3.Connection,
    cliente_nome: str,
    profissional_id: int,
    data_inicio: datetime,
    data_fim: datetime,
    status: str = "agendado",
) -> dict[str, int | str]:
    inicio_iso = data_inicio.isoformat(timespec="seconds")
    fim_iso = data_fim.isoformat(timespec="seconds")

    cursor = connection.execute(
        """
        INSERT INTO agendamentos (
            cliente_nome, profissional_id, data_inicio, data_fim, status
        ) VALUES (?, ?, ?, ?, ?)
        """,
        (cliente_nome, profissional_id, inicio_iso, fim_iso, status),
    )
    connection.commit()

    return {
        "id": cursor.lastrowid,
        "cliente_nome": cliente_nome,
        "profissional_id": profissional_id,
        "data_inicio": inicio_iso,
        "data_fim": fim_iso,
        "status": status,
    }


def get_appointment_by_id(
    connection: sqlite3.Connection,
    appointment_id: int,
) -> dict[str, int | str] | None:
    connection.row_factory = sqlite3.Row
    row = connection.execute(
        "SELECT id, cliente_nome, profissional_id, data_inicio, data_fim, status FROM agendamentos WHERE id = ?",
        (appointment_id,),
    ).fetchone()

    if row is None:
        return None

    return dict(row)


def list_appointments(
    connection: sqlite3.Connection,
) -> list[dict[str, int | str]]:
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        "SELECT id, cliente_nome, profissional_id, data_inicio, data_fim, status "
        "FROM agendamentos ORDER BY id"
    ).fetchall()

    return [dict(row) for row in rows]
