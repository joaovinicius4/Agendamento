from pathlib import Path
from app.database import get_connection, initialize_database
from app.repositories.profissionais import create_professional, list_professionals

def test_create_professional(tmp_path: Path) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        professional = create_professional(
            connection,
            nome="Ana Souza",
            especialidade="Fisioterapia",
        )

        assert professional["id"] == 1
        assert professional["nome"] == "Ana Souza"
        assert professional["especialidade"] == "Fisioterapia"
    finally:
        connection.close()

def test_list_professionals_returns_all_registered_professionals(
    tmp_path: Path,
) -> None:
    connection = get_connection(tmp_path / "test_agendamento.db")
    initialize_database(connection)

    try:
        first = create_professional(connection, "Ana Souza", "Fisioterapia")
        second = create_professional(connection, "Bruno Lima", "Odontologia")
        professionals = list_professionals(connection)

        assert professionals == [first, second]
    finally:
        connection.close()
