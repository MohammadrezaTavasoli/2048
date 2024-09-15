#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

import pygame
import random
import sys

# Define some constants
BOARD_SIZE = 500
BOARD_ROWS = 4
BOARD_COLS = 4
TILE_SIZE = BOARD_SIZE // BOARD_ROWS
BACKGROUND_COLOR = (204, 192, 179)
EMPTY_TILE_COLOR = (205, 193, 180)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 64
FPS = 60
DELAY = 2000  # Delay in milliseconds between AI moves

class Game2048:
    def __init__(self):
        self.board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def copy(self):
        # Create a new instance without calling __init__
        new_game = Game2048.__new__(Game2048)
        new_game.board = [row[:] for row in self.board]
        new_game.score = self.score
        new_game.game_over = self.game_over
        return new_game

    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(BOARD_ROWS) for j in range(BOARD_COLS) if self.board[i][j] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.board[row][col] = 2 if random.random() < 0.9 else 4

    def compress(self, row):
        """Compress the non-zero tiles to the left."""
        new_row = [num for num in row if num != 0]
        new_row += [0] * (BOARD_COLS - len(new_row))
        return new_row

    def merge(self, row):
        """Merge the tiles in a row towards the left."""
        for i in range(BOARD_COLS - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for row in range(BOARD_ROWS):
            original_row = self.board[row][:]
            compressed_row = self.compress(self.board[row])
            merged_row = self.merge(compressed_row)
            final_row = self.compress(merged_row)
            self.board[row] = final_row
            if final_row != original_row:
                moved = True
        if moved:
            self.add_random_tile()
        return moved

    def move_right(self):
        moved = False
        for row in range(BOARD_ROWS):
            original_row = self.board[row][:]
            reversed_row = original_row[::-1]
            compressed_row = self.compress(reversed_row)
            merged_row = self.merge(compressed_row)
            final_row = self.compress(merged_row)
            final_row = final_row[::-1]
            self.board[row] = final_row
            if final_row != original_row:
                moved = True
        if moved:
            self.add_random_tile()
        return moved

    def move_up(self):
        moved = False
        for col in range(BOARD_COLS):
            original_column = [self.board[row][col] for row in range(BOARD_ROWS)]
            compressed_column = self.compress(original_column)
            merged_column = self.merge(compressed_column)
            final_column = self.compress(merged_column)
            for row in range(BOARD_ROWS):
                self.board[row][col] = final_column[row]
            if final_column != original_column:
                moved = True
        if moved:
            self.add_random_tile()
        return moved

    def move_down(self):
        moved = False
        for col in range(BOARD_COLS):
            original_column = [self.board[row][col] for row in range(BOARD_ROWS)]
            reversed_column = original_column[::-1]
            compressed_column = self.compress(reversed_column)
            merged_column = self.merge(compressed_column)
            final_column = self.compress(merged_column)
            final_column = final_column[::-1]
            for row in range(BOARD_ROWS):
                self.board[row][col] = final_column[row]
            if final_column != original_column:
                moved = True
        if moved:
            self.add_random_tile()
        return moved

    def is_game_over(self):
        # Check for empty tiles
        for row in self.board:
            if 0 in row:
                return False

        # Check for possible merges horizontally
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS - 1):
                if self.board[row][col] == self.board[row][col + 1]:
                    return False

        # Check for possible merges vertically
        for col in range(BOARD_COLS):
            for row in range(BOARD_ROWS - 1):
                if self.board[row][col] == self.board[row + 1][col]:
                    return False

        return True

    def print_board(self):
        """Print the board to the console for debugging."""
        print(f"Score: {self.score}")
        for row in self.board:
            print(row)
        print("-" * 20)

pygame.init()
screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("2048")

# Define fonts
font = pygame.font.SysFont("Arial", FONT_SIZE)

def draw_board(game):
    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the tiles
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            value = game.board[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if value != 0:
                # Define tile colors based on value
                tile_colors = {
                    2: (238, 228, 218),
                    4: (237, 224, 200),
                    8: (242, 177, 121),
                    16: (245, 149, 99),
                    32: (246, 124, 95),
                    64: (246, 94, 59),
                    128: (237, 207, 114),
                    256: (237, 204, 97),
                    512: (237, 200, 80),
                    1024: (237, 197, 63),
                    2048: (237, 194, 46),
                }
                color = tile_colors.get(value, (60, 58, 50))
                pygame.draw.rect(screen, color, rect)

                # Draw the number for the tile
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, EMPTY_TILE_COLOR, rect)

    # Draw the score
    font_small = pygame.font.SysFont("Arial", 24)
    score_text = font_small.render("Score: " + str(game.score), True, (0, 0, 0))
    score_rect = score_text.get_rect(topright=(BOARD_SIZE - 10, 10))
    screen.blit(score_text, score_rect)

    # Update the display
    pygame.display.update()

def heuristic(game):
    empty_tiles = sum(row.count(0) for row in game.board)
    max_tile = max(max(row) for row in game.board)
    return empty_tiles + max_tile / 2048

def get_best_move(game):
    best_score = -float('inf')
    best_move = None
    moves = ['left', 'right', 'up', 'down']
    for move in moves:
        new_game = game.copy()
        if move == 'left':
            moved = new_game.move_left()
        elif move == 'right':
            moved = new_game.move_right()
        elif move == 'up':
            moved = new_game.move_up()
        elif move == 'down':
            moved = new_game.move_down()

        # If the move doesn't change the board, skip it
        if not moved:
            continue

        score = heuristic(new_game)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# Create a new game
game = Game2048()

# Main game loop
clock = pygame.time.Clock()
while not game.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.game_over = True

    # AI makes a move
    move = get_best_move(game)
    if move == 'left':
        moved = game.move_left()
    elif move == 'right':
        moved = game.move_right()
    elif move == 'up':
        moved = game.move_up()
    elif move == 'down':
        moved = game.move_down()
    else:
        game.game_over = True  # No valid moves left

    # Debug: Print the board after the move
    print(f"Move: {move}")
    game.print_board()

    # Check if the game is over
    if game.is_game_over():
        game.game_over = True

    # Update the display
    draw_board(game)

    # Delay to slow down the AI moves
    pygame.time.wait(DELAY)

    # Wait for the next frame
    clock.tick(FPS)

# Display Game Over message
font_large = pygame.font.SysFont("Arial", 48)
game_over_text = font_large.render("Game Over!", True, (0, 0, 0))
game_over_rect = game_over_text.get_rect(center=(BOARD_SIZE // 2, BOARD_SIZE // 2))
screen.blit(game_over_text, game_over_rect)
pygame.display.update()
pygame.time.wait(3000)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()


# In[ ]:




