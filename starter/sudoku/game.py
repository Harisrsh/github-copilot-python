class GameStore:
    def __init__(self):
        self.puzzle = None
        self.solution = None

    def set_game(self, puzzle, solution):
        self.puzzle = puzzle
        self.solution = solution

    def clear(self):
        self.puzzle = None
        self.solution = None
