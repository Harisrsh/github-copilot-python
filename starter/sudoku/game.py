class GameStore:
    def __init__(self, puzzle=None, solution=None):
        self.puzzle = puzzle
        self.solution = solution

    def set_game(self, puzzle, solution):
        self.puzzle = puzzle
        self.solution = solution

    def clear(self):
        self.puzzle = None
        self.solution = None

    def to_dict(self):
        return {
            'puzzle': self.puzzle,
            'solution': self.solution,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(puzzle=data.get('puzzle'), solution=data.get('solution'))
