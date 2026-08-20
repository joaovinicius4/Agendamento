import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from app.database import get_connection, initialize_database
from app.repositories.agendamentos import (
    create_appointment,
    get_appointment_by_id,
    list_appointments,
)
from app.repositories.profissionais import create_professional


def create_test_professional(connection):
    return create_professional(
        connection,
        nome="Ana Souza",
        especialidade="Fisioterapia",
    )


def test_create_appointment(tmp_path: Path) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        professional = create_test_professional(connection)
        appointment = create_appointment(
            connection,
            cliente_nome="Aline",
            profissional_id=professional["id"],
            data_inicio=datetime(2025, 12, 10, 10, 0),
            data_fim=datetime(2025, 12, 10, 11, 0),
        )

        assert appointment["id"] == 1
        assert appointment["cliente_nome"] == "Aline"
        assert appointment["profissional_id"] == professional["id"]
        assert appointment["data_inicio"] == "2025-12-10T10:00:00"
        assert appointment["data_fim"] == "2025-12-10T11:00:00"
        assert appointment["status"] == "agendado"
    finally:
        connection.close()


def test_get_appointment_by_id(tmp_path: Path) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        professional = create_test_professional(connection)
        created = create_appointment(
            connection,
            cliente_nome="Aline",
            profissional_id=professional["id"],
            data_inicio=datetime(2025, 12, 10, 10, 0),
            data_fim=datetime(2025, 12, 10, 11, 0),
        )
        found = get_appointment_by_id(connection, created["id"])

        assert found == created
    finally:
        connection.close()


def test_list_appointment_returns_all_registered_appointments(
    tmp_path: Path,
) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        professional = create_test_professional(connection)
        first = create_appointment(
            connection,
            cliente_nome="Aline",
            profissional_id=professional["id"],
            data_inicio=datetime(2025, 12, 10, 10, 0),
            data_fim=datetime(2025, 12, 10, 11, 0),
        )
        second = create_appointment(
            connection,
            cliente_nome="Mariana",
            profissional_id=professional["id"],
            data_inicio=datetime(2025, 12, 10, 11, 0),
            data_fim=datetime(2025, 12, 10, 12, 0),
        )
        appointments = list_appointments(connection)

        assert appointments == [first, second]
    finally:
        connection.close()


def test_get_nonexistent_appointment_returns_none(tmp_path: Path) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        appointment = get_appointment_by_id(connection, appointment_id=999)

        assert appointment is None
    finally:
        connection.close()


def test_create_appointment_with_nonexistent_professional_fails(
    tmp_path: Path,
) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        with pytest.raises(sqlite3.IntegrityError):
            create_appointment(
                connection,
                cliente_nome="Aline",
                profissional_id=999,
                data_inicio=datetime(2025, 12, 10, 10, 0),
                data_fim=datetime(2025, 12, 10, 11, 0),
            )
    finally:
        connection.close()


def test_create_appointment_with_invalid_time_range_fails(
    tmp_path: Path,
) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        professional = create_test_professional(connection)

        with pytest.raises(sqlite3.IntegrityError):
            create_appointment(
                connection,
                cliente_nome="Aline",
                profissional_id=professional["id"],
                data_inicio=datetime(2025, 12, 10, 11, 0),
                data_fim=datetime(2025, 12, 10, 10, 0),
            )
    finally:
        connection.close()
