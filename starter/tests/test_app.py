import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    app_module.game_store.clear()
    with app_module.app.test_client() as client:
        yield client


def test_index_route_renders_template(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<!doctype html>' in response.data.lower()


def test_new_game_route_returns_puzzle(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert isinstance(payload['puzzle'], list)


def test_check_solution_route_returns_error_without_game(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_check_solution_route_reports_incorrect_cells(client):
    app_module.game_store.set_game(
        [[0] * 9 for _ in range(9)],
        [[i + j for j in range(9)] for i in range(9)],
    )

    response = client.post('/check', json={'board': [[1] * 9 for _ in range(9)]})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload['incorrect']
