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


if __name__ == '__main__':
    app.run(debug=True)