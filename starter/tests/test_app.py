import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as client:
        yield client


def test_index_route_renders_template(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<!doctype html>' in response.data.lower()


def test_new_game_route_returns_puzzle(client):
    response = client.get('/new?difficulty=medium')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert isinstance(payload['puzzle'], list)


def test_check_solution_route_returns_error_without_game(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No game in progress'


def test_check_solution_route_reports_incorrect_cells(client):
    with app_module.app.test_client() as client_one:
        with client_one.session_transaction() as session:
            session['game_store'] = {
                'puzzle': [[0] * 9 for _ in range(9)],
                'solution': [[i + j for j in range(9)] for i in range(9)],
            }

        response = client_one.post('/check', json={'board': [[1] * 9 for _ in range(9)]})

        assert response.status_code == 200
        payload = response.get_json()
        assert payload['incorrect']

    with app_module.app.test_client() as client_two:
        response = client_two.get('/new?difficulty=easy')
        assert response.status_code == 200
        with client_two.session_transaction() as session:
            assert session['game_store'] is not None
