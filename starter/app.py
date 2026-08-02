from flask import Flask, jsonify, render_template, request

from sudoku import GameStore, find_incorrect_cells, generate_puzzle_for_difficulty

app = Flask(__name__)

game_store = GameStore()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    puzzle, solution = generate_puzzle_for_difficulty(difficulty)
    game_store.set_game(puzzle, solution)
    return jsonify({'puzzle': puzzle})


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json or {}
    board = data.get('board')
    if game_store.solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = find_incorrect_cells(board, game_store.solution)
    return jsonify({'incorrect': incorrect})


@app.route('/hint')
def get_hint():
    if game_store.solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    if game_store.puzzle is None:
        return jsonify({'error': 'No game in progress'}), 400

    for row in range(len(game_store.puzzle)):
        for col in range(len(game_store.puzzle[row])):
            if game_store.puzzle[row][col] == 0:
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': game_store.solution[row][col]
                })
    return jsonify({'error': 'No empty cells remain'}), 400


if __name__ == '__main__':
    app.run(debug=True)