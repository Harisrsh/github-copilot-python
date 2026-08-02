import copy

import sudoku


def test_create_empty_board_has_expected_shape():
    board = sudoku.create_empty_board()

    assert len(board) == sudoku.SIZE
    assert all(len(row) == sudoku.SIZE for row in board)
    assert all(cell == sudoku.EMPTY for row in board for cell in row)


def test_is_safe_detects_conflicts_in_row_and_column_and_box():
    board = sudoku.create_empty_board()
    board[0][0] = 5
    board[0][1] = 1
    board[1][0] = 1
    board[2][2] = 5

    assert sudoku.is_safe(board, 0, 2, 5) is False
    assert sudoku.is_safe(board, 0, 2, 4) is True


def test_fill_board_solves_a_simple_board():
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    solved = copy.deepcopy(board)
    assert sudoku.fill_board(solved) is True
    assert all(cell != sudoku.EMPTY for row in solved for cell in row)
    for row in solved:
        assert len(set(row)) == sudoku.SIZE
    for col in range(sudoku.SIZE):
        assert len({row[col] for row in solved}) == sudoku.SIZE
    for box_row in range(0, sudoku.SIZE, 3):
        for box_col in range(0, sudoku.SIZE, 3):
            values = []
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    values.append(solved[row][col])
            assert len(set(values)) == sudoku.SIZE


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = sudoku.generate_puzzle(clues=30)

    assert isinstance(puzzle, list)
    assert isinstance(solution, list)
    assert len(puzzle) == sudoku.SIZE
    assert len(solution) == sudoku.SIZE
    assert puzzle != solution


def test_generate_puzzle_creates_uniquely_solvable_puzzles():
    for _ in range(3):
        puzzle, _ = sudoku.generate_puzzle(clues=30)
        assert sudoku.count_solutions(puzzle, limit=2) == 1


def test_difficulty_levels_generate_expected_clue_counts():
    easy_puzzle, _ = sudoku.generate_puzzle_for_difficulty('easy')
    medium_puzzle, _ = sudoku.generate_puzzle_for_difficulty('medium')
    hard_puzzle, _ = sudoku.generate_puzzle_for_difficulty('hard')

    easy_clues = sum(cell != sudoku.EMPTY for row in easy_puzzle for cell in row)
    medium_clues = sum(cell != sudoku.EMPTY for row in medium_puzzle for cell in row)
    hard_clues = sum(cell != sudoku.EMPTY for row in hard_puzzle for cell in row)

    assert 40 <= easy_clues <= 50
    assert 30 <= medium_clues <= 40
    assert 20 <= hard_clues <= 30
