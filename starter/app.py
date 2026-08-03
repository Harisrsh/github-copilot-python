import os

from flask import Flask, jsonify, render_template, request, session

from sudoku import GameStore, find_incorrect_cells, generate_puzzle_for_difficulty

VALID_DIFFICULTIES = {'easy', 'medium', 'hard'}

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')


def get_session_game_store():
    if 'game_store' not in session:
        session['game_store'] = GameStore().to_dict()
    return GameStore.from_dict(session['game_store'])


def save_session_game_store(game_store):
    session['game_store'] = game_store.to_dict()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = (request.args.get('difficulty', 'medium') or 'medium').lower()
    if difficulty not in VALID_DIFFICULTIES:
        return jsonify({'error': 'Invalid difficulty value'}), 400

    puzzle, solution = generate_puzzle_for_difficulty(difficulty)
    game_store = get_session_game_store()
    game_store.set_game(puzzle, solution)
    save_session_game_store(game_store)
    return jsonify({'puzzle': puzzle})


@app.route('/check', methods=['POST'])
def check_solution():
    if not request.is_json:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    try:
        data = request.get_json(force=False, silent=False)
    except Exception:
        return jsonify({'error': 'Request body must be valid JSON'}), 400

    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must be a JSON object'}), 400

    board = data.get('board')
    if not isinstance(board, list) or len(board) != 9 or any(not isinstance(row, list) or len(row) != 9 for row in board):
        return jsonify({'error': 'Board must be a 9x9 grid of integers'}), 400

    if any(not isinstance(value, int) for row in board for value in row):
        return jsonify({'error': 'Board must be a 9x9 grid of integers'}), 400

    game_store = get_session_game_store()
    if game_store.solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = find_incorrect_cells(board, game_store.solution)
    return jsonify({'incorrect': incorrect})


@app.route('/hint')
def get_hint():
    game_store = get_session_game_store()
    if game_store.solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if game_store.puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    for row in range(len(game_store.puzzle)):
        for col in range(len(game_store.puzzle[row])):
            if game_store.puzzle[row][col] == 0:
                game_store.puzzle[row][col] = game_store.solution[row][col]
                save_session_game_store(game_store)
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': game_store.solution[row][col]
                })
    return jsonify({'error': 'No empty cells remain'}), 400


if __name__ == '__main__':
    app.run(debug=True)