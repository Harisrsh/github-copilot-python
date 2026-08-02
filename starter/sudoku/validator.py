SIZE = 9


def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def find_incorrect_cells(board, solution):
    incorrect = []
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return incorrect


def count_solutions(board, limit=2):
    def search(current_board):
        if limit <= 0:
            return 0

        for row in range(SIZE):
            for col in range(SIZE):
                if current_board[row][col] == 0:
                    solution_count = 0
                    for num in range(1, SIZE + 1):
                        if is_safe(current_board, row, col, num):
                            current_board[row][col] = num
                            solution_count += search(current_board)
                            current_board[row][col] = 0
                            if solution_count >= limit:
                                return solution_count
                    return solution_count

        return 1

    return search([row[:] for row in board])
