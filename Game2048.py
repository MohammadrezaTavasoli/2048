#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pygame
import random

# Define some constants
BOARD_SIZE = 500
BOARD_ROWS = 4
BOARD_COLS = 4
TILE_SIZE = BOARD_SIZE // BOARD_ROWS
BACKGROUND_COLOR = (204, 192, 179)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 64
FPS = 60

class Game2048:
    def __init__(self):
        self.board = [[0] * BOARD_COLS for _ in range(BOARD_ROWS)]
        self.score = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_tiles = [(i, j) for i in range(BOARD_ROWS) for j in range(BOARD_COLS) if self.board[i][j] == 0]
        if empty_tiles:
            row, col = random.choice(empty_tiles)
            self.board[row][col] = 2 if random.random() < 0.5 else 4

    def move_left(self):
        moved = False
        for row in range(BOARD_ROWS):
            for col in range(1, BOARD_COLS):
                if self.board[row][col] != 0:
                    for k in range(col):
                        if self.board[row][k] == 0:
                            self.board[row][k] = self.board[row][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif self.board[row][k] == self.board[row][col]:
                            self.board[row][k] *= 2
                            self.score += self.board[row][k]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif k == col - 1:
                           # self.board[row][k + 1] = self.board[row][col]
                            #self.board[row][col] = 0
                            moved = True
        if moved:
            self.add_random_tile()

    def move_right(self):
        moved = False
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS - 2, -1, -1):
                if self.board[row][col] != 0:
                    for k in range(col + 1, BOARD_COLS):
                        if self.board[row][k] == 0:
                            self.board[row][k] = self.board[row][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif self.board[row][k] == self.board[row][col]:
                            self.board[row][k] *= 2
                            self.score += self.board[row][k]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif k == BOARD_COLS - 1:
                           # self.board[row][k - 1] = self.board[row][col]
                            #self.board[row][col] = 0
                            moved = True
        if moved:
            self.add_random_tile()
    def move_up(self):
        moved = False
        for col in range(4):
            for row in range(1, 4):
                if self.board[row][col] != 0:
                    for k in range(row):
                        if self.board[k][col] == 0:
                            self.board[k][col] = self.board[row][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif self.board[k][col] == self.board[row][col]:
                            self.board[k][col] *= 2
                            self.score += self.board[k][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif k == row - 1:
                          #  self.board[k + 1][col] = self.board[row][col]
                           # self.board[row][col] = 0
                            moved = True
        if moved:
            self.add_random_tile()
            # Initialize Pygame
    def move_down(self):
        moved = False
        for col in range(4):
            for row in range(2, -1, -1):
                if self.board[row][col] != 0:
                    for k in range(row + 1, 4):
                        if self.board[k][col] == 0:
                            self.board[k][col] = self.board[row][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif self.board[k][col] == self.board[row][col]:
                            self.board[k][col] *= 2
                            self.score += self.board[k][col]
                            self.board[row][col] = 0
                            moved = True
                            break
                        elif k == 3:
                         #   self.board[k - 1][col] = self.board[row][col]
                          #  self.board[row][col] = 0
                            moved = True
        if moved:
            self.add_random_tile()

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
          #  print(value)
            if value != 0:
                # Draw a colored rectangle for the tile
                #color = 255 - int(255 / 64 * value)
              #  print(color)
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if value==2:
                    color1, color2, color3 =(238, 228, 218)
                if value==4:
                    color1, color2, color3 =(237, 224, 200)
                if value==8:
                    color1, color2, color3 =(242, 177, 121)
                if value==16:
                    color1, color2, color3 =(245, 149, 99)
                if value==32:
                    color1, color2, color3 =(246, 124, 95)
                if value==64:
                    color1, color2, color3 =(246, 94, 59)
                if value==128:
                    color1, color2, color3 =(237, 207, 114)
                if value==256:
                    color1, color2, color3 =(237, 204, 97)
                if value==512:
                    color1, color2, color3 =(237, 200, 80)
                if value==1024:
                    color1, color2, color3 = (237, 197, 63)
                if value==2048:
                    color1, color2, color3 =(237, 194, 46)
                pygame.draw.rect(screen, (color1, color2, color3), rect)

                # Draw the number for the tile
                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    # Draw the score
    fontone = pygame.font.SysFont("Arial", 16)
    score_text = fontone.render("Score: " + str(game.score), True,(0,0,0))
  #  font = pygame.font.SysFont("Arial", 64)
    score_rect = score_text.get_rect(topright=(BOARD_SIZE - 10, 10))
    screen.blit(score_text, score_rect)

    # Update the display
    pygame.display.update()

# Create a new game
game = Game2048()

# Main game loop
clock = pygame.time.Clock()
while not game.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            elif event.key == pygame.K_RIGHT:
                game.move_right()
            elif event.key == pygame.K_UP:
                game.move_up()
            elif event.key == pygame.K_DOWN:
                game.move_down()

    # Update the display
    draw_board(game)

    # Wait for the next frame
    clock.tick(FPS)

# Quit Pygame
pygame.quit()

 


# In[ ]:




