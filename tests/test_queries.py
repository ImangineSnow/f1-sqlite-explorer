from main import connect, race_results, team_drivers, team_results


def test_expected_table_sizes():
    with connect() as connection:
        counts = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ("Drivers", "Teams", "Races", "Race_Drivers", "Race_Teams")
        }
    assert counts == {
        "Drivers": 22,
        "Teams": 10,
        "Races": 22,
        "Race_Drivers": 435,
        "Race_Teams": 220,
    }


def test_parameterized_queries_return_data():
    with connect() as connection:
        assert len(race_results(connection, "Bahrain")) > 0
        assert len(team_results(connection, "Red Bull Racing")) == 22
        assert len(team_drivers(connection, "Red Bull Racing")) == 2

