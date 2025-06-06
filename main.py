import threading
import time
import pygame
import random
from pygame import mixer

# We initialize our variables
width = 1280
height = 720
tetris_width = 320
tetris_height = 640
board_width = 10
board_height = 20
sqr_size = 32
game_score = 0
game_corner_x = (width - tetris_width) / 3
game_corner_y = (height - tetris_height) / 2
board = [[0 for x in range(board_width)] for y in range(board_height)]
easy_mode = False
hard_mode = False
moving_bool = False
score_thread_bool = False

# Locations of tetromino blocks
S = (((0, -1), (1, -1), (-1, 0), (0, 0)),
     ((1, 0), (1, 1), (0, -1), (0, 0)),
     ((0, 1), (-1, 1), (1, 0), (0, 0)),
     ((-1, -1), (-1, 0), (0, 1), (0, 0)))
Z = (((-1, -1), (0, -1), (0, 0), (1, 0)),
     ((1, -1), (1, 0), (0, 0), (0, 1)),
     ((1, 1), (0, 1), (0, 0), (-1, 0)),
     ((-1, 1), (-1, 0), (0, 0), (0, -1)))
O = (((-1, -1), (0, -1), (-1, 0), (0, 0)),
     ((-1, -1), (0, -1), (-1, 0), (0, 0)),
     ((-1, -1), (0, -1), (-1, 0), (0, 0)),
     ((-1, -1), (0, -1), (-1, 0), (0, 0)))
I = (((-2, 0), (-1, 0), (0, 0), (1, 0)),
     ((0, -1), (0, 0), (0, 1), (0, 2)),
     ((-2, 1), (-1, 1), (0, 1), (1, 1)),
     ((-1, -1), (-1, 0), (-1, 1), (-1, 2)))
J = (((-1, -1), (-1, 0), (0, 0), (1, 0)),
     ((1, -1), (0, -1), (0, 0), (0, 1)),
     ((1, 1), (1, 0), (0, 0), (-1, 0)),
     ((-1, 1), (0, 1), (0, 0), (0, -1)))
L = (((1, -1), (-1, 0), (0, 0), (1, 0)),
     ((1, 1), (0, -1), (0, 0), (0, 1)),
     ((-1, 1), (1, 0), (0, 0), (-1, 0)),
     ((-1, -1), (0, 1), (0, 0), (0, -1)))
T = (((0, -1), (-1, 0), (0, 0), (1, 0)),
     ((1, 0), (0, -1), (0, 0), (0, 1)),
     ((0, 1), (1, 0), (0, 0), (-1, 0)),
     ((-1, 0), (0, 1), (0, 0), (0, -1)))

# We assign colours to variables
black = (0, 0, 0)
white = (255, 255, 255)
grey = pygame.image.load("grey-block.png")
blue = pygame.image.load("blue-block.png")
green = pygame.image.load("green-block.png")
red = pygame.image.load("red-block.png")
orange = pygame.image.load("orange-block.png")
yellow = pygame.image.load("yellow-block.png")
purple = pygame.image.load("purple-block.png")
cyan = pygame.image.load("cyan-block.png")
lvl_block = pygame.image.load("level-block.png")
lvl_color = (0, 255, 0)

# The array of our tetrominoes
shapes = [S, Z, O, I, L, J, T]
# The array of colours assigned to tetrominoes
shape_images = [blue, green, red, orange, yellow, purple, cyan]

# We initialize a window for display
SCREEN = pygame.display.set_mode((width, height))
# We set a name for the window
pygame.display.set_caption("Tetris")
# We fill our display with black colour
SCREEN.fill(black)
# We update the full display to the screen
pygame.display.flip()


# We create a class for tetrominoes
class Tetromino(object):

    # The constructor for our tetrominoes
    def __init__(self, shape, x, y):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_images[shapes.index(shape)]
        self.rotation = 0
        self.blocks = [4]
        self.set_blocks()

    # Setting rotation to one
    def set_rotation(self, i):
        self.rotation = i

    # Setting the blocks
    def set_blocks(self):
        self.blocks = [self.shape[self.rotation][0],
                       self.shape[self.rotation][1],
                       self.shape[self.rotation][2],
                       self.shape[self.rotation][3]]

    # Function that moves tetrominoes down
    def move_down(self):
        remove_tetromino(self)
        self.y += 1
        draw_tetromino(self)
        draw_grid()

    # Function that moves tetrominoes left
    def move_left(self):
        remove_tetromino(self)
        self.x -= 1
        if valid_position(self):
            draw_tetromino(self)
        else:
            self.x += 1
            draw_tetromino(self)
        draw_grid()

    # Function that moves tetrominoes right
    def move_right(self):
        remove_tetromino(self)
        self.x += 1
        if valid_position(self):
            draw_tetromino(self)
        else:
            self.x -= 1
            draw_tetromino(self)
        draw_grid()

    # Function that rotates the tetrominoes
    def rotate(self, right_or_left):
        remove_tetromino(self)
        temp_x = self.x
        temp_rotation = self.rotation
        is_stuck = True
        if right_or_left == "right":
            self.rotation = (self.rotation + 1) % 4
        elif right_or_left == "left":
            self.rotation = (self.rotation - 1) % 4

        self.set_blocks()
        if valid_position(self):
            draw_tetromino(self)
            is_stuck = False
        else:
            self.x += 1
            if valid_position(self):
                draw_tetromino(self)
                is_stuck = False
            else:
                self.x -= 2
                if valid_position(self):
                    draw_tetromino(self)
                    is_stuck = False
                else:
                    if self.shape == I:
                        self.x += 3
                        if valid_position(self):
                            draw_tetromino(self)
                            is_stuck = False
                        else:
                            self.x -= 4
                            if valid_position(self):
                                draw_tetromino(self)
                                is_stuck = False
        if is_stuck:
            self.x = temp_x
            self.rotation = temp_rotation
            self.set_blocks()
            draw_tetromino(self)

        draw_grid()


# Function that returns the maximum value from the array of integers
def max_value(x, y, z, t):
    int_list = [x, y, z, t]
    return max(int_list)


# Function that returns the minimum value from the array of integers
def min_value(x, y, z, t):
    int_list = [x, y, z, t]
    return min(int_list)


# Function that removes the tetromino
def remove_tetromino(tetromino):
    temp = tetromino
    for i in range(0, 4):
        square = pygame.Rect((temp.blocks[i][0] + temp.x) * sqr_size + game_corner_x,
                             (temp.blocks[i][1] + temp.y) * sqr_size + game_corner_y,
                             sqr_size, sqr_size)
        pygame.draw.rect(SCREEN, black, square, 0)


# Function that draws tetrominoes
def draw_tetromino(tetromino):
    for i in range(0, 4):
        square = tetromino.color.get_rect(
            topleft=((tetromino.blocks[i][0] + tetromino.x) * sqr_size + game_corner_x,
                     (tetromino.blocks[i][1] + tetromino.y) * sqr_size + game_corner_y))
        SCREEN.blit(tetromino.color, square)


# Function that draws the next tetrominoes
def draw_next_tetromino(tetromino):
    for i in range(0, 4):
        square = tetromino.color.get_rect(
            topleft=((tetromino.blocks[i][0] + tetromino.x + 3) * sqr_size + game_corner_x + tetris_width,
                     (tetromino.blocks[i][1] + tetromino.y + 12) * sqr_size + game_corner_y))
        SCREEN.blit(tetromino.color, square)
    square = pygame.Rect(game_corner_x + tetris_width + 4 * sqr_size, game_corner_y + 10 * sqr_size,
                         8 * sqr_size, 4 * sqr_size)
    pygame.draw.rect(SCREEN, white, square, 1)


# Function that removes the next tetromino
def remove_next_tetromino():
    square = pygame.Rect(game_corner_x + tetris_width + 3 * sqr_size, game_corner_y + 10 * sqr_size,
                         8 * sqr_size, 4 * sqr_size)
    pygame.draw.rect(SCREEN, black, square, 0)


def next_tetromino_grid(tetromino):
    for i in range(0, 4):
        square = pygame.Rect((tetromino.blocks[i][0] + tetromino.x + 3) * sqr_size + game_corner_x + tetris_width,
                             (tetromino.blocks[i][1] + tetromino.y + 12) * sqr_size + game_corner_y,
                             sqr_size, sqr_size)
        pygame.draw.rect(SCREEN, white, square, 1)


# Function that creates a new tetromino
def new_tetromino():
    return Tetromino(random.choice(shapes), 5, 0)


# Function that fills the board with black colour
def fill_board():
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            board[i][j] = black


# Function that freezes a tetromino
def freeze(tetromino):
    for i in range(0, 4):
        temp_x = tetromino.blocks[i][0]
        temp_y = tetromino.blocks[i][1]
        board[temp_y + tetromino.y][temp_x + tetromino.x] = tetromino.color


# Function that makes tetrominoes fall down forever
def move_vertical():
    global current_tetromino, next_tetromino, game_score
    bottom = current_tetromino.y + max_value(current_tetromino.blocks[0][1],
                                             current_tetromino.blocks[1][1],
                                             current_tetromino.blocks[2][1],
                                             current_tetromino.blocks[3][1])

    if bottom < 19 and valid_move_down(current_tetromino):
        current_tetromino.move_down()
    else:
        freeze(current_tetromino)
        remove_next_tetromino()
        current_tetromino = next_tetromino
        next_tetromino = new_tetromino()
        draw_next_tetromino(next_tetromino)
        next_tetromino_grid(next_tetromino)
        draw_tetromino(current_tetromino)
        for i in range(0, 20):
            # If the row is full then 1000 more points are added to the score
            if row_is_full(i):
                move_rows_down(i)
                draw_new_rows()
                game_score += 1000
        # If the tetromino falls on the other tetromino or the bottom, then 100 more points are added to the score
        game_score += 100
        # If easy or hard modes are chosen, then game with modes is displayed
        if easy_mode or hard_mode:
            game_table_modes()
            # Display updated
            pygame.display.update()
        # If levels are chosen, then game with some level is displayed
        else:
            game_table_levels()
            # Display updated
            pygame.display.update()


# Function that draws the grid
def draw_grid():
    for x in range(0, tetris_width + 2 * sqr_size, sqr_size):
        # The grey frame is drawn
        square1 = grey.get_rect(topleft=(x + game_corner_x - sqr_size,
                                         game_corner_y - sqr_size))
        square2 = grey.get_rect(topleft=(x + game_corner_x - sqr_size,
                                         game_corner_y + tetris_height))
        SCREEN.blit(grey, square1)
        SCREEN.blit(grey, square2)
    for y in range(0, tetris_height + 2 * sqr_size, sqr_size):
        # The grey frame is drawn
        square1 = grey.get_rect(topleft=(game_corner_x - sqr_size,
                                         y + game_corner_y - sqr_size))
        square2 = grey.get_rect(topleft=(game_corner_x + tetris_width,
                                         y + game_corner_y - sqr_size))
        SCREEN.blit(grey, square1)
        SCREEN.blit(grey, square2)
    for x in range(0, tetris_width, sqr_size):
        # Black blocks for the grid are drawn
        for y in range(0, tetris_height, sqr_size):
            square = pygame.Rect(x + game_corner_x, y + game_corner_y, sqr_size, sqr_size)
            pygame.draw.rect(SCREEN, white, square, 1)


# Function that creates the game table screen for the modes
def game_table_modes():
    table = pygame.Rect(game_corner_x + tetris_width + 2 * sqr_size, game_corner_y,
                        13 * sqr_size, 20 * sqr_size)
    score_clear = pygame.Rect(game_corner_x + tetris_width + 2 * sqr_size, game_corner_y + 3 * sqr_size,
                              10 * sqr_size, 3 * sqr_size)

    # Score display is created
    s_title_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    s_title = s_title_font.render("SCORE", True, white, black)
    score_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    score_text = score_font.render(str(game_score), True, white, black)
    # High score display is created
    hs_title_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    hs_title = hs_title_font.render("HIGH SCORE", True, white, black)
    high_score_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    high_score_text = high_score_font.render(str(get_high_score()), True, white, black)
    # Next shape display is created
    next_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    next_text = next_font.render("NEXT SHAPE", True, white, black)

    s_title_rect = s_title.get_rect()
    score_rect = score_text.get_rect()
    hs_title_rect = hs_title.get_rect()
    high_score_rect = high_score_text.get_rect()
    next_rect = next_text.get_rect()

    # Positions of displays are assigned
    s_title_rect.center = (game_corner_x + tetris_width + 5 * sqr_size, game_corner_y + 2 * sqr_size)
    score_rect.center = (game_corner_x + tetris_width + 5 * sqr_size, game_corner_y + 4 * sqr_size)
    hs_title_rect.center = (game_corner_x + tetris_width + 11 * sqr_size, game_corner_y + 2 * sqr_size)
    high_score_rect.center = (game_corner_x + tetris_width + 11 * sqr_size, game_corner_y + 4 * sqr_size)
    next_rect.center = (game_corner_x + tetris_width + 8 * sqr_size, game_corner_y + 8 * sqr_size)

    pygame.draw.rect(SCREEN, black, score_clear, 0)
    pygame.draw.rect(SCREEN, white, table, 1)
    SCREEN.blit(s_title, s_title_rect)
    SCREEN.blit(score_text, score_rect)
    SCREEN.blit(hs_title, hs_title_rect)
    SCREEN.blit(high_score_text, high_score_rect)
    SCREEN.blit(next_text, next_rect)


# Function that creates the game table screen for the levels
def game_table_levels():
    table = pygame.Rect(game_corner_x + tetris_width + 2 * sqr_size, game_corner_y,
                        12 * sqr_size, 20 * sqr_size)
    score_clear = pygame.Rect(game_corner_x + tetris_width + 3 * sqr_size, game_corner_y + 4 * sqr_size,
                              9 * sqr_size, 3 * sqr_size)

    # Score display is created
    text_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    text = text_font.render("SCORE", True, white, black)
    score_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    score_text = score_font.render(str(game_score), True, white, black)
    # Next shape display is created
    next_font = pygame.font.Font(pygame.font.get_default_font(), 32)
    next_text = next_font.render("NEXT SHAPE", True, white, black)

    text_rect = text.get_rect()
    score_rect = score_text.get_rect()
    next_rect = next_text.get_rect()

    # Positions of displays are assigned
    text_rect.center = (game_corner_x + tetris_width + 8 * sqr_size, game_corner_y + 2 * sqr_size)
    score_rect.center = (game_corner_x + tetris_width + 8 * sqr_size, game_corner_y + 5 * sqr_size)
    next_rect.center = (game_corner_x + tetris_width + 8 * sqr_size, game_corner_y + 8 * sqr_size)

    pygame.draw.rect(SCREEN, black, score_clear, 0)
    pygame.draw.rect(SCREEN, white, table, 1)
    SCREEN.blit(text, text_rect)
    SCREEN.blit(score_text, score_rect)
    SCREEN.blit(next_text, next_rect)


# Function that checks whether a tetromino can move down
def valid_move_down(tetromino):
    block_1 = [tetromino.x + tetromino.blocks[0][0], tetromino.y + tetromino.blocks[0][1] + 1]
    block_2 = [tetromino.x + tetromino.blocks[1][0], tetromino.y + tetromino.blocks[1][1] + 1]
    block_3 = [tetromino.x + tetromino.blocks[2][0], tetromino.y + tetromino.blocks[2][1] + 1]
    block_4 = [tetromino.x + tetromino.blocks[3][0], tetromino.y + tetromino.blocks[3][1] + 1]
    if board[block_1[1]][block_1[0]] == black \
            and board[block_2[1]][block_2[0]] == black \
            and board[block_3[1]][block_3[0]] == black \
            and board[block_4[1]][block_4[0]] == black:
        return True
    else:
        return False


# Function that checks whether the tetromino is valid position, meaning the tetromino is inside the grid
def valid_position(tetromino):
    try:
        block_1 = [tetromino.x + tetromino.blocks[0][0], tetromino.y + tetromino.blocks[0][1]]
        block_2 = [tetromino.x + tetromino.blocks[1][0], tetromino.y + tetromino.blocks[1][1]]
        block_3 = [tetromino.x + tetromino.blocks[2][0], tetromino.y + tetromino.blocks[2][1]]
        block_4 = [tetromino.x + tetromino.blocks[3][0], tetromino.y + tetromino.blocks[3][1]]

        if 0 <= block_1[0] <= 9 \
                and 0 <= block_2[0] <= 9 \
                and 0 <= block_3[0] <= 9 \
                and 0 <= block_4[0] <= 9 \
                and board[block_1[1]][block_1[0]] == black \
                and board[block_2[1]][block_2[0]] == black \
                and board[block_3[1]][block_3[0]] == black \
                and board[block_4[1]][block_4[0]] == black:
            return True
        else:
            return False
    except:
        return False


# Function that makes a tetromino falls down to the bottom
def hard_drop(tetromino):
    for i in range(0, 19):
        move_vertical()
        if not valid_position(tetromino):
            break


# Function that checks whether a row consists of any colour blocks, but black ones
def row_is_full(row):
    for i in range(0, len(board[row])):
        if board[row][i] == black:
            return False
        elif i == 9 and board[row][i] != black:
            return True


# Function that make rows fall after the lowest row was cleared
def move_rows_down(row):
    clr = mixer.Sound("clear-row.mp3")
    clr.play(0)
    for i in range(row, -1, -1):
        for j in range(0, 10):
            if i != 0:
                board[i][j] = board[i - 1][j]
            else:
                board[i][j] = black


def draw_new_rows():
    for i in range(0, 20):
        for j in range(0, 10):
            if board[i][j] is black:
                square = pygame.Rect(game_corner_x + j * sqr_size, game_corner_y + i * sqr_size, sqr_size, sqr_size)
                pygame.draw.rect(SCREEN, board[i][j], square, 0)
            elif board[i][j] is lvl_color:
                square = lvl_block.get_rect(topleft=(game_corner_x + j * sqr_size, game_corner_y + i * sqr_size))
                SCREEN.blit(lvl_block, square)
            else:
                square = board[i][j].get_rect(topleft=(game_corner_x + j * sqr_size, game_corner_y + i * sqr_size))
                SCREEN.blit(board[i][j], square)
            draw_grid()


# Function that returns the high score
def get_high_score():
    if easy_mode:
        f = open('easy_high_score.txt', 'r')
        score_list = [int(score) for score in f.read().split()]
        if len(score_list) == 0:
            return 0
        else:
            return max(score_list)
    elif hard_mode:
        f = open('hard_high_score.txt', 'r')
        score_list = [int(score) for score in f.read().split()]
        if len(score_list) == 0:
            return 0
        else:
            return max(score_list)


# Function that decreases the score while playing the levels
def score_dic():
    global game_score, score_thread_bool
    while score_thread_bool:
        time.sleep(0.8)
        game_score -= 100
        game_table_levels()


# Function that makes the thread of tetrominoes falling down endlessly
def move_down_thread():
    global game_score, thread_bool
    # If the easy mode is chosen, then the speed of falling is increasing slower
    while thread_bool and easy_mode:
        if game_score < 5000:
            time.sleep(1)
        elif game_score < 10000:
            time.sleep(0.9)
        elif game_score < 15000:
            time.sleep(0.8)
        elif game_score < 20000:
            time.sleep(0.7)
        elif game_score < 25000:
            time.sleep(0.6)
        else:
            time.sleep(0.5)
        move_vertical()
    # If the hard mode is chosen, then the speed of falling is increasing faster
    while thread_bool and hard_mode:
        if game_score < 5000:
            time.sleep(0.75)
        elif game_score < 10000:
            time.sleep(0.65)
        elif game_score < 15000:
            time.sleep(0.55)
        elif game_score < 20000:
            time.sleep(0.45)
        elif game_score < 25000:
            time.sleep(0.35)
        else:
            time.sleep(0.25)
        move_vertical()
    # If the levels is chosen, then the speed of falling is constant
    while thread_bool and not easy_mode and not hard_mode:
        time.sleep(0.8)
        move_vertical()


# This function is not necessary for the code, but finishing the levels might be hard, so it can be used to see what
# happens when a level is completed. To do that, uncomment fill_test() in level_1() and comment fill_level_1() in
# level_1().
def fill_test():
    board[19][3] = lvl_color


# Function that draws level blocks for the first level
def fill_level_1():
    for i in range(3, 7):
        board[19][i] = lvl_color
    for i in range(2, 7, 4):
        board[18][i] = lvl_color
        board[18][i + 1] = lvl_color
    for i in range(1, 9):
        board[17][i] = lvl_color
    for i in range(1, 8, 3):
        board[16][i] = lvl_color
        board[16][i + 1] = lvl_color
    for i in range(2, 8):
        board[15][i] = lvl_color
    for i in range(3, 7):
        board[14][i] = lvl_color


# Function that draws level blocks for the second level
def fill_level_2():
    board[9][9] = lvl_color
    for i in range(8, 10):
        board[10][i] = lvl_color
    board[11][9] = lvl_color
    for i in range(0, 4):
        board[12][i] = lvl_color
    for i in range(6, 10):
        board[12][i] = lvl_color
    for i in range(8, 10):
        for j in range(16, 18):
            board[j][i] = lvl_color
    for i in range(0, 2):
        for j in range(18, 20):
            board[j][i] = lvl_color


# Function that draws level blocks for the third level
def fill_level_3():
    for i in range(0, 3):
        board[17][i] = lvl_color
    for i in range(7, 10):
        board[17][i] = lvl_color
    board[13][0] = lvl_color
    board[13][9] = lvl_color
    for i in range(0, 2):
        board[12][i] = lvl_color
    for i in range(8, 10):
        board[12][i] = lvl_color
    board[11][0] = lvl_color
    board[11][9] = lvl_color
    for i in range(0, 2):
        board[8][i] = lvl_color
    for i in range(8, 10):
        board[8][i] = lvl_color
    board[7][0] = lvl_color
    board[7][9] = lvl_color
    for i in range(0, 2):
        board[6][i] = lvl_color
    for i in range(8, 10):
        board[6][i] = lvl_color


# Function that creates the screen where levels can be chosen
def levels():
    global game_score, easy_mode, hard_mode
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    background = pygame.image.load("background.jpg")
    # Creating buttons that indicate each level
    lvl_1_button = pygame.image.load("lvl_1_button.png")
    lvl_2_button = pygame.image.load("lvl_2_button.png")
    lvl_3_button = pygame.image.load("lvl_3_button.png")
    bg_sqr = background.get_rect(topleft=(0, 0))
    lvl_1_sqr = lvl_1_button.get_rect(center=(width / 2 - 192, height / 2))
    lvl_2_sqr = lvl_2_button.get_rect(center=(width / 2, height / 2))
    lvl_3_sqr = lvl_3_button.get_rect(center=(width / 2 + 192, height / 2))
    lvl_1_frame = pygame.Rect(width / 2 - 256, height / 2 - 64,
                              128, 128)
    lvl_2_frame = pygame.Rect(width / 2 - 64, height / 2 - 64,
                              128, 128)
    lvl_3_frame = pygame.Rect(width / 2 + 128, height / 2 - 64,
                              128, 128)

    SCREEN.blit(background, bg_sqr)
    SCREEN.blit(lvl_1_button, lvl_1_sqr)
    SCREEN.blit(lvl_2_button, lvl_2_sqr)
    SCREEN.blit(lvl_3_button, lvl_3_sqr)
    pygame.draw.rect(SCREEN, black, lvl_1_frame, 1)
    pygame.draw.rect(SCREEN, black, lvl_2_frame, 1)
    pygame.draw.rect(SCREEN, black, lvl_3_frame, 1)
    f1 = open('lvl_1_comp.txt', 'r')
    f2 = open('lvl_2_comp.txt', 'r')
    f3 = open('lvl_3_comp.txt', 'r')
    lvl_1_list = [int(score) for score in f1.read().split()]
    lvl_2_list = [int(score) for score in f2.read().split()]
    lvl_3_list = [int(score) for score in f3.read().split()]
    # If the first level is completed, then the colour of the button is changed
    if len(lvl_1_list) > 0:
        lvl_1_c_button = pygame.image.load('level_1_completed.png')
        lvl_1_c_sqr = lvl_1_c_button.get_rect(center=(width / 2 - 192, height / 2))
        lvl_1_c_frame = pygame.Rect(width / 2 - 256, height / 2 - 64,
                                    128, 128)
        SCREEN.blit(lvl_1_c_button, lvl_1_c_sqr)
        pygame.draw.rect(SCREEN, black, lvl_1_c_frame, 1)
    # If the second level is completed, then the colour of the button is changed
    if len(lvl_2_list) > 0:
        lvl_2_c_button = pygame.image.load('level_2_completed.png')
        lvl_2_c_sqr = lvl_2_c_button.get_rect(center=(width / 2, height / 2))
        lvl_2_c_frame = pygame.Rect(width / 2 - 64, height / 2 - 64,
                                    128, 128)
        SCREEN.blit(lvl_2_c_button, lvl_2_c_sqr)
        pygame.draw.rect(SCREEN, black, lvl_2_c_frame, 1)
    # If the third level is completed, then the colour of the button is changed
    if len(lvl_3_list) > 0:
        lvl_3_c_button = pygame.image.load('level_3_completed.png')
        lvl_3_c_sqr = lvl_3_c_button.get_rect(center=(width / 2 + 192, height / 2))
        lvl_3_c_frame = pygame.Rect(width / 2 + 128, height / 2 - 64,
                                    128, 128)
        SCREEN.blit(lvl_3_c_button, lvl_3_c_sqr)
        pygame.draw.rect(SCREEN, black, lvl_3_c_frame, 1)
    # Display updated
    pygame.display.update()
    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If the escape button is pressed, then we go to the main menu screen
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse button is pressed at the first level's button's location, then the first level is played
                if (width / 2 - 224 < pygame.mouse.get_pos()[0] < width / 2 - 160) and \
                        (height / 2 - 32 < pygame.mouse.get_pos()[1] < height / 2 + 32):
                    easy_mode = False
                    hard_mode = False
                    game_score = 10000
                    level_1()
                # If the mouse button is pressed at the second level's button's location, then the second level is played
                elif (width / 2 - 32 < pygame.mouse.get_pos()[0] < width / 2 + 32) and \
                        (height / 2 - 32 < pygame.mouse.get_pos()[1] < height / 2 + 32):
                    easy_mode = False
                    hard_mode = False
                    game_score = 10000
                    level_2()
                # If the mouse button is pressed at the third level's button's location, then the third level is played
                elif (width / 2 + 160 < pygame.mouse.get_pos()[0] < width / 2 + 224) and \
                        (height / 2 - 32 < pygame.mouse.get_pos()[1] < height / 2 + 32):
                    easy_mode = False
                    hard_mode = False
                    game_score = 10000
                    level_3()


# Function that creates the game over screen
def end_menu(score):
    end = mixer.Sound("end-sound.mp3")
    end.play(0)
    # If the easy mode was played, then the high score for an easy mode is updated
    if easy_mode:
        with open('easy_high_score.txt', 'a') as f:
            f.write(str(score) + '\n')
    # If the hard mode was played, then the high score for the hard mode is updated
    elif hard_mode:
        with open('hard_high_score.txt', 'a') as f:
            f.write(str(score) + '\n')

    clear = pygame.Rect(0, 0, width, height)
    # Game over text, home button and replay button are created
    game_over_text = pygame.image.load("game-over.png")
    home_button = pygame.image.load("home_button.png")
    replay_button = pygame.image.load("replay-button.png")

    go_sqr = game_over_text.get_rect(center=(width / 2, height / 2 - 128))
    home_sqr = home_button.get_rect(center=(width / 2 - 128, height / 2 + 128))
    rply_sqr = replay_button.get_rect(center=(width / 2 + 128, height / 2 + 128))
    score_font = pygame.font.Font(pygame.font.get_default_font(), 48)
    score_text = score_font.render(str(score), True, white, black)
    score_sqr = score_text.get_rect(center=(width / 2, height / 2))

    pygame.draw.rect(SCREEN, black, clear, 0)
    SCREEN.blit(game_over_text, go_sqr)
    SCREEN.blit(home_button, home_sqr)
    SCREEN.blit(replay_button, rply_sqr)
    SCREEN.blit(score_text, score_sqr)
    pygame.display.update()

    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse button is pressed at the home button's location, then we go to main menu
                if (width / 2 - 160 < pygame.mouse.get_pos()[0] < width / 2 - 96) and \
                        (height / 2 + 96 < pygame.mouse.get_pos()[1] < height / 2 + 160):
                    main_menu()
                # If the mouse button is pressed at the replay button's location, then we go to play menu
                elif (width / 2 + 96 < pygame.mouse.get_pos()[0] < width / 2 + 160) and \
                        (height / 2 + 96 < pygame.mouse.get_pos()[1] < height / 2 + 160):
                    play_menu()


# Function that creates the "you won" screen
def win_menu(score):
    win = mixer.Sound("win-sound.mp3")
    win.play(0)
    clear = pygame.Rect(0, 0, width, height)
    # You won text, home button and replay button are created and placed on the screen
    game_over_text = pygame.image.load("you-won.png")
    home_button = pygame.image.load("home_button.png")
    replay_button = pygame.image.load("replay-button.png")

    go_sqr = game_over_text.get_rect(center=(width / 2, height / 2 - 128))
    home_sqr = home_button.get_rect(center=(width / 2 - 128, height / 2 + 128))
    rply_sqr = replay_button.get_rect(center=(width / 2 + 128, height / 2 + 128))
    score_font = pygame.font.Font(pygame.font.get_default_font(), 48)
    score_text = score_font.render(str(score), True, white, black)
    score_sqr = score_text.get_rect(center=(width / 2, height / 2))

    pygame.draw.rect(SCREEN, black, clear, 0)
    SCREEN.blit(game_over_text, go_sqr)
    SCREEN.blit(home_button, home_sqr)
    SCREEN.blit(replay_button, rply_sqr)
    SCREEN.blit(score_text, score_sqr)
    pygame.display.update()

    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse button is pressed at the home button's location, then we go to main menu
                if (width / 2 - 160 < pygame.mouse.get_pos()[0] < width / 2 - 96) and \
                        (height / 2 + 96 < pygame.mouse.get_pos()[1] < height / 2 + 160):
                    main_menu()
                # If the mouse button is pressed at the replay button's location, then we go to play menu
                elif (width / 2 + 96 < pygame.mouse.get_pos()[0] < width / 2 + 160) and \
                        (height / 2 + 96 < pygame.mouse.get_pos()[1] < height / 2 + 160):
                    play_menu()


# Function that creates the screen where you can choose the modes or choose playing levels
def play_menu():
    global game_score, easy_mode, hard_mode
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    # Easy mode button, hard mode button and levels button are created and placed on the screen
    background = pygame.image.load("background.jpg")
    easy_button = pygame.image.load("easy-button.png")
    hard_button = pygame.image.load("hard-button.png")
    levels_button = pygame.image.load("levels-button.png")

    bg_sqr = background.get_rect(topleft=(0, 0))
    easy_sqr = easy_button.get_rect(center=(width / 2, height / 2 - 192))
    hard_sqr = hard_button.get_rect(center=(width / 2, height / 2))
    lvl_sqr = levels_button.get_rect(center=(width / 2, height / 2 + 192))
    easy_button_frame = pygame.Rect(width / 2 - 128, height / 2 - 256,
                                    256, 128)
    hard_button_frame = pygame.Rect(width / 2 - 128, height / 2 - 64,
                                    256, 128)
    levels_button_frame = pygame.Rect(width / 2 - 128, height / 2 + 128,
                                      256, 128)

    SCREEN.blit(background, bg_sqr)
    SCREEN.blit(easy_button, easy_sqr)
    SCREEN.blit(hard_button, hard_sqr)
    SCREEN.blit(levels_button, lvl_sqr)
    pygame.draw.rect(SCREEN, black, easy_button_frame, 1)
    pygame.draw.rect(SCREEN, black, hard_button_frame, 1)
    pygame.draw.rect(SCREEN, black, levels_button_frame, 1)
    pygame.display.update()
    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If the escape button is pressed, then we go to the main menu screen
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse button is pressed at the easy mode button's location, then the easy mode is played
                if (width / 2 - 128 < pygame.mouse.get_pos()[0] < width / 2 + 128) and \
                        (height / 2 - 256 < pygame.mouse.get_pos()[1] < height / 2 - 128):
                    easy_mode = True
                    hard_mode = False
                    game_score = 0
                    game_default()
                # If the mouse button is pressed at the hard mode button's location, then the hard mode is played
                elif (width / 2 - 128 < pygame.mouse.get_pos()[0] < width / 2 + 128) and \
                        (height / 2 - 64 < pygame.mouse.get_pos()[1] < height / 2 + 64):
                    hard_mode = True
                    easy_mode = False
                    game_score = 0
                    game_default()
                # If the mouse button is pressed at the levels' button's location, then we go to the levels' menu
                elif (width / 2 - 128 < pygame.mouse.get_pos()[0] < width / 2 + 128) and \
                        (height / 2 + 128 < pygame.mouse.get_pos()[1] < height / 2 + 256):
                    levels()


# Function that creates the guide screen is shown
def guide():
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    # Guide is created and placed on the screen
    gd = pygame.image.load("guide.png")
    gd_sqr = gd.get_rect(center=(width / 2, height / 2))
    SCREEN.blit(gd, gd_sqr)
    pygame.display.update()
    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If the escape button is pressed, then we go to the main menu screen
                if event.key == pygame.K_ESCAPE:
                    main_menu()


# Function that creates the main menu screen
def main_menu():
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    # Tetris logo, play button and guide button are created and placed on the screen
    background = pygame.image.load("background.jpg")
    tetris_logo = pygame.image.load("tetris_logo.png")
    play_button = pygame.image.load("play-button.png")
    guide_button = pygame.image.load("guide-button.png")

    bg_sqr = background.get_rect(topleft=(0, 0))
    logo_sqr = tetris_logo.get_rect(center=(width / 2, height / 2 - 192))
    pb_sqr = play_button.get_rect(center=(width / 2, height / 2))
    op_sqr = guide_button.get_rect(center=(width / 2, height / 2 + 192))
    play_button_frame = pygame.Rect(width / 2 - 128, height / 2 - 64,
                                    256, 128)
    guide_button_frame = pygame.Rect(width / 2 - 128, height / 2 + 128,
                                     256, 128)

    SCREEN.blit(background, bg_sqr)
    SCREEN.blit(tetris_logo, logo_sqr)
    SCREEN.blit(play_button, pb_sqr)
    SCREEN.blit(guide_button, op_sqr)
    pygame.draw.rect(SCREEN, black, play_button_frame, 1)
    pygame.draw.rect(SCREEN, black, guide_button_frame, 1)
    pygame.display.update()
    while True:
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the mouse button is pressed at the play button's location, then we go to play menu
                if (width / 2 - 128 < pygame.mouse.get_pos()[0] < width / 2 + 128) and \
                        (height / 2 - 64 < pygame.mouse.get_pos()[1] < height / 2 + 64):
                    play_menu()
                # If the mouse button is pressed at the guide button's location, then we go to the guide menu
                elif (width / 2 - 128 < pygame.mouse.get_pos()[0] < width / 2 + 128) and \
                        (height / 2 + 128 < pygame.mouse.get_pos()[1] < height / 2 + 256):
                    guide()
            if event.type == pygame.KEYDOWN:
                # If the escape button is pressed, then the game and the window closes
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()


# Function that creates first level
def level_1():
    global game_score, current_tetromino, next_tetromino, thread_bool, score_thread_bool
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    SCREEN.fill(black)
    draw_grid()
    current_tetromino = new_tetromino()
    next_tetromino = new_tetromino()
    game_table_levels()
    draw_next_tetromino(next_tetromino)
    next_tetromino_grid(next_tetromino)
    fill_board()
    # fill_test()
    fill_level_1()
    draw_new_rows()
    pygame.display.update()
    thread_bool = True
    score_thread_bool = True
    moving_thread = threading.Thread(target=move_down_thread)
    moving_thread.start()
    score_thread = threading.Thread(target=score_dic)
    score_thread.start()
    while True:
        # If there are no level blocks, then the first level is completed and win menu appears
        if not any(lvl_color in x for x in board):
            thread_bool = False
            score_thread_bool = False
            with open('lvl_1_comp.txt', 'a') as f:
                f.write(str(1) + '\n')
            moving_thread.join()
            score_thread.join()
            win_menu(game_score)
        # If the score is less or equal to zero, then the end menu appears
        elif game_score <= 0:
            thread_bool = False
            score_thread_bool = False
            moving_thread.join()
            score_thread.join()
            end_menu(0)
        else:
            for i in range(0, 10):
                # If in the first row of the board there is a non-black block, then the end menu appears
                if board[0][i] != black:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    end_menu(0)
                else:
                    draw_grid()
        left_x = current_tetromino.x + min_value(current_tetromino.blocks[0][0],
                                                 current_tetromino.blocks[1][0],
                                                 current_tetromino.blocks[2][0],
                                                 current_tetromino.blocks[3][0])
        right_x = current_tetromino.x + max_value(current_tetromino.blocks[0][0],
                                                  current_tetromino.blocks[1][0],
                                                  current_tetromino.blocks[2][0],
                                                  current_tetromino.blocks[3][0])
        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If "a" button is pressed, then current tetromino moves to the left
                if event.key == pygame.K_a:
                    if left_x > 0:
                        current_tetromino.move_left()
                # If "d" button is pressed, then current tetromino moves to the right
                elif event.key == pygame.K_d:
                    if right_x < 9:
                        current_tetromino.move_right()
                # If "s" button is pressed, then current tetromino moves down
                elif event.key == pygame.K_s:
                    move_vertical()

                # If space is pressed, then current tetromino is hard dropped
                elif event.key == pygame.K_SPACE:
                    hd = mixer.Sound("hard-drop.mp3")
                    hd.play(0)
                    hard_drop(current_tetromino)
                    game_score += 100

                # If "q" button is pressed, then current tetromino is rotated to the left
                elif event.key == pygame.K_q:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("left")

                # If "e" button is pressed, then current tetromino is rotated to the right
                elif event.key == pygame.K_e:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("right")

                # If escape is pressed, then we go to the main menu
                elif event.key == pygame.K_ESCAPE:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    main_menu()

        pygame.display.update()


# Function that creates second level
def level_2():
    global game_score, current_tetromino, next_tetromino, thread_bool, score_thread_bool
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    SCREEN.fill(black)
    draw_grid()
    current_tetromino = new_tetromino()
    next_tetromino = new_tetromino()
    game_table_levels()
    draw_next_tetromino(next_tetromino)
    next_tetromino_grid(next_tetromino)
    fill_board()
    fill_level_2()
    draw_new_rows()
    pygame.display.update()
    thread_bool = True
    score_thread_bool = True
    moving_thread = threading.Thread(target=move_down_thread)
    moving_thread.start()
    score_thread = threading.Thread(target=score_dic)
    score_thread.start()
    while True:
        # If there are no level blocks, then the second level is completed and win menu appears
        if not any(lvl_color in x for x in board):
            thread_bool = False
            score_thread_bool = False
            with open('lvl_2_comp.txt', 'a') as f:
                f.write(str(1) + '\n')
            moving_thread.join()
            score_thread.join()
            win_menu(game_score)
        # If the score is less or equal to zero, then the end menu appears
        elif game_score <= 0:
            thread_bool = False
            score_thread_bool = False
            moving_thread.join()
            score_thread.join()
            end_menu(0)
        else:
            for i in range(0, 10):
                # If in the first row of the board there is a non-black block, then the end menu appears
                if board[0][i] != black:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    end_menu(0)
                else:
                    draw_grid()
        left_x = current_tetromino.x + min_value(current_tetromino.blocks[0][0],
                                                 current_tetromino.blocks[1][0],
                                                 current_tetromino.blocks[2][0],
                                                 current_tetromino.blocks[3][0])
        right_x = current_tetromino.x + max_value(current_tetromino.blocks[0][0],
                                                  current_tetromino.blocks[1][0],
                                                  current_tetromino.blocks[2][0],
                                                  current_tetromino.blocks[3][0])

        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If "a" button is pressed, then current tetromino moves to the left
                if event.key == pygame.K_a:
                    if left_x > 0:
                        current_tetromino.move_left()
                # If "d" button is pressed, then current tetromino moves to the right
                elif event.key == pygame.K_d:
                    if right_x < 9:
                        current_tetromino.move_right()
                # If "s" button is pressed, then current tetromino moves down
                elif event.key == pygame.K_s:
                    move_vertical()

                # If space is pressed, then current tetromino is hard dropped
                elif event.key == pygame.K_SPACE:
                    hd = mixer.Sound("hard-drop.mp3")
                    hd.play(0)
                    hard_drop(current_tetromino)
                    game_score += 100

                # If "q" button is pressed, then current tetromino is rotated to the left
                elif event.key == pygame.K_q:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("left")

                # If "e" button is pressed, then current tetromino is rotated to the right
                elif event.key == pygame.K_e:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("right")

                # If escape is pressed, then we go to the main menu
                elif event.key == pygame.K_ESCAPE:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    main_menu()

        pygame.display.update()


# Function that creates third level
def level_3():
    global game_score, current_tetromino, next_tetromino, thread_bool, score_thread_bool
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    SCREEN.fill(black)
    draw_grid()
    current_tetromino = new_tetromino()
    next_tetromino = new_tetromino()
    game_table_levels()
    draw_next_tetromino(next_tetromino)
    next_tetromino_grid(next_tetromino)
    fill_board()
    fill_level_3()
    draw_new_rows()
    pygame.display.update()
    thread_bool = True
    score_thread_bool = True
    moving_thread = threading.Thread(target=move_down_thread)
    moving_thread.start()
    score_thread = threading.Thread(target=score_dic)
    score_thread.start()
    while True:
        # If there are no level blocks, then the second level is completed and win menu appears
        if not any(lvl_color in x for x in board):
            thread_bool = False
            score_thread_bool = False
            with open('lvl_3_comp.txt', 'a') as f:
                f.write(str(1) + '\n')
            moving_thread.join()
            score_thread.join()
            win_menu(game_score)
        # If the score is less or equal to zero, then the end menu appears
        elif game_score <= 0:
            thread_bool = False
            score_thread_bool = False
            moving_thread.join()
            score_thread.join()
            end_menu(0)
        else:
            for i in range(0, 10):
                # If in the first row of the board there is a non-black block, then the end menu appears
                if board[0][i] != black:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    end_menu(0)
                else:
                    draw_grid()
        left_x = current_tetromino.x + min_value(current_tetromino.blocks[0][0],
                                                 current_tetromino.blocks[1][0],
                                                 current_tetromino.blocks[2][0],
                                                 current_tetromino.blocks[3][0])
        right_x = current_tetromino.x + max_value(current_tetromino.blocks[0][0],
                                                  current_tetromino.blocks[1][0],
                                                  current_tetromino.blocks[2][0],
                                                  current_tetromino.blocks[3][0])

        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If "a" button is pressed, then current tetromino moves to the left
                if event.key == pygame.K_a:
                    if left_x > 0:
                        current_tetromino.move_left()
                # If "d" button is pressed, then current tetromino moves to the right
                elif event.key == pygame.K_d:
                    if right_x < 9:
                        current_tetromino.move_right()
                # If "s" button is pressed, then current tetromino moves down
                elif event.key == pygame.K_s:
                    move_vertical()

                # If space is pressed, then current tetromino is hard dropped
                elif event.key == pygame.K_SPACE:
                    hd = mixer.Sound("hard-drop.mp3")
                    hd.play(0)
                    hard_drop(current_tetromino)
                    game_score += 100

                # If "q" button is pressed, then current tetromino is rotated to the left
                elif event.key == pygame.K_q:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("left")

                # If "e" button is pressed, then current tetromino is rotated to the right
                elif event.key == pygame.K_e:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("right")

                # If escape is pressed, then we go to the main menu
                elif event.key == pygame.K_ESCAPE:
                    thread_bool = False
                    score_thread_bool = False
                    moving_thread.join()
                    score_thread.join()
                    main_menu()

        pygame.display.update()


# Function that creates a default game (game with easy or hard mode)
def game_default():
    global game_score, current_tetromino, next_tetromino, thread_bool
    click = mixer.Sound("button-click.mp3")
    click.play(0)
    SCREEN.fill(black)
    pygame.display.update()
    draw_grid()
    current_tetromino = new_tetromino()
    next_tetromino = new_tetromino()
    game_table_modes()
    draw_next_tetromino(next_tetromino)
    next_tetromino_grid(next_tetromino)
    fill_board()
    thread_bool = True
    moving_thread = threading.Thread(target=move_down_thread)
    moving_thread.start()
    while True:
        for i in range(0, 10):
            # If in the first row of the board there is a non-black block, then the end menu appears
            if board[0][i] != black:
                thread_bool = False
                moving_thread.join()
                end_menu(game_score)
            else:
                draw_grid()
        left_x = current_tetromino.x + min_value(current_tetromino.blocks[0][0],
                                                 current_tetromino.blocks[1][0],
                                                 current_tetromino.blocks[2][0],
                                                 current_tetromino.blocks[3][0])
        right_x = current_tetromino.x + max_value(current_tetromino.blocks[0][0],
                                                  current_tetromino.blocks[1][0],
                                                  current_tetromino.blocks[2][0],
                                                  current_tetromino.blocks[3][0])

        # The loop that gets events from the queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # If "a" button is pressed, then current tetromino moves to the left
                if event.key == pygame.K_a:
                    if left_x > 0:
                        current_tetromino.move_left()
                # If "d" button is pressed, then current tetromino moves to the right
                elif event.key == pygame.K_d:
                    if right_x < 9:
                        current_tetromino.move_right()
                # If "s" button is pressed, then current tetromino moves down
                elif event.key == pygame.K_s:
                    move_vertical()

                # If space is pressed, then current tetromino is hard dropped
                elif event.key == pygame.K_SPACE:
                    hd = mixer.Sound("hard-drop.mp3")
                    hd.play(0)
                    hard_drop(current_tetromino)
                    game_score += 100

                # If "q" button is pressed, then current tetromino is rotated to the left
                elif event.key == pygame.K_q:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("left")

                # If "e" button is pressed, then current tetromino is rotated to the right
                elif event.key == pygame.K_e:
                    rot = mixer.Sound("rotate.mp3")
                    rot.play(0)
                    current_tetromino.rotate("right")

                # If escape is pressed, then we go to the main menu
                elif event.key == pygame.K_ESCAPE:
                    thread_bool = False
                    moving_thread.join()
                    main_menu()

        pygame.display.update()


# We initialize the mixer module
pygame.mixer.init()
# We initialize all imported pygame modules
pygame.init()
main_menu()
# We update portions of the screen for software displays
pygame.display.update()
