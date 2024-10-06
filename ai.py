class AI:
    def __init__(self, game):
        self.game = game

    def make_move(self):
        best_move = self.find_best_move()
        self.execute_move(best_move)

    def find_best_move(self):
        best_score = float('-inf')
        best_move = None

        for rotation in range(4):
            for x in range(self.game.grid_width):
                test_piece = {
                    'shape': self.game.current_piece['shape'],
                    'x': x,
                    'y': self.game.current_piece['y']
                }

                for _ in range(rotation):
                    test_piece['shape'] = list(zip(*test_piece['shape'][::-1]))

                if self.game.can_move(test_piece):
                    while self.game.can_move(test_piece, dy=1):
                        test_piece['y'] += 1

                    score = self.evaluate_move(test_piece)
                    if score > best_score:
                        best_score = score
                        best_move = (rotation, x)

        return best_move

    def evaluate_move(self, piece):
        test_grid = [row[:] for row in self.game.grid]
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    test_grid[piece['y'] + y][piece['x'] + x] = 1

        height = self.get_height(test_grid)
        holes = self.count_holes(test_grid)
        cleared_lines = self.count_cleared_lines(test_grid)

        return -height - 2 * holes + cleared_lines * 10

    def get_height(self, grid):
        for y in range(len(grid)):
            if any(grid[y]):
                return len(grid) - y
        return 0

    def count_holes(self, grid):
        holes = 0
        for x in range(len(grid[0])):
            block_found = False
            for y in range(len(grid)):
                if grid[y][x]:
                    block_found = True
                elif block_found:
                    holes += 1
        return holes

    def count_cleared_lines(self, grid):
        return sum(1 for row in grid if all(row))

    def execute_move(self, move):
        if move is None:
            return

        rotation, x = move

        for _ in range(rotation):
            self.game.rotate_piece()

        while self.game.current_piece['x'] < x:
            self.game.move_right()
        while self.game.current_piece['x'] > x:
            self.game.move_left()

        self.game.drop()
