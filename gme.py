import pygame
import random

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid_size = 30
        self.grid_width = 10
        self.grid_height = 20
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

    def new_piece(self):
        shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]]
        ]
        return {
            'shape': random.choice(shapes),
            'x': self.grid_width // 2 - len(shapes[0]) // 2,
            'y': 0
        }

    def update(self):
        if self.can_move(self.current_piece, dy=1):
            self.current_piece['y'] += 1
        else:
            self.place_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()

    def can_move(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    if (new_x < 0 or new_x >= self.grid_width or
                        new_y >= self.grid_height or
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = 1

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.grid) if all(row)]
        for line in full_lines:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(self.grid_width)])

    def rotate_piece(self):
        rotated = list(zip(*self.current_piece['shape'][::-1]))
        if self.can_move({'shape': rotated, 'x': self.current_piece['x'], 'y': self.current_piece['y']}):
            self.current_piece['shape'] = rotated

    def move_left(self):
        if self.can_move(self.current_piece, dx=-1):
            self.current_piece['x'] -= 1

    def move_right(self):
        if self.can_move(self.current_piece, dx=1):
            self.current_piece['x'] += 1

    def drop(self):
        while self.can_move(self.current_piece, dy=1):
            self.current_piece['y'] += 1

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (x * self.grid_size, y * self.grid_size, self.grid_size - 1, self.grid_size - 1))

        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, (255, 0, 0),
                                     ((self.current_piece['x'] + x) * self.grid_size,
                                      (self.current_piece['y'] + y) * self.grid_size,
                                      self.grid_size - 1, self.grid_size - 1))
