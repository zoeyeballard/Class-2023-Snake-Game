import pygame
import random

from pygame import QUIT
from enum import Enum


class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 112)
    BLACK = (0, 0, 0)
    RED = (252, 58, 58)
    DARK_RED = (184, 0, 40)
    GREEN = (46, 117, 46)
    BLUE = (0, 125, 184)


class Direction(Enum):
    NOT_MOVING = -1
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3


class Snake:
    xy_list: list
    length: int
    head_x: int
    head_y: int
    direction: Direction

    def __init__(self, head_x, head_y):
        self.xy_list = []
        self.length = 1
        self.head_x = head_x
        self.head_y = head_y
        self.direction = Direction.NOT_MOVING


# Initialize the program
pygame.init()

# Colors


# Screen Dimensions
scrn_width = 600
scrn_height = 400

# Create the Screen
screen = pygame.display.set_mode((scrn_width, scrn_height))
pygame.display.set_caption('ZOEY BALLARD - SNAKE GAME')

# Both of these create the speed of the snake
clock = pygame.time.Clock()
speed = 15

# Size of the pixel
pixel_size = 10

# Further Design - Fonts! :D
font_sty = pygame.font.SysFont("twcen", 25)
font_score = pygame.font.SysFont("agencyfb", 35)


# This is a function to display the score while the user plays
def display_score(score):
    value = font_score.render("YOUR SCORE: " + str(score), True, Color.WHITE)
    screen.blit(value, [0, 0])


def update_snake(new_direction, snake):
    x_change = 0
    y_change = 0

    # Repetition of if you click the corner "X", you can leave
    # Establishes directions for all the arrow keys
    if new_direction == Direction.WEST:
        x_change = -pixel_size
    elif new_direction == Direction.EAST:
        x_change = pixel_size
    elif new_direction == Direction.NORTH:
        y_change = -pixel_size
    elif new_direction == Direction.SOUTH:
        y_change = pixel_size

    # This is the changes in direction
    snake.head_x += x_change
    snake.head_y += y_change

    # This creates the "head" of the snake
    snake_head = [snake.head_x, snake.head_y]
    snake.xy_list.append(snake_head)
    if len(snake.xy_list) > snake.length:
        del snake.xy_list[0]

    # Starts programs, creating snake and displaying the score
    for x in snake.xy_list:
        pygame.draw.rect(screen, Color.GREEN, [x[0], x[1], pixel_size, pixel_size])

    # Update direction
    snake.direction = new_direction

    return snake


# This is just to display messages, mainly the ending message ("You Lost")
def display_msg(msg, color):
    mesg = font_sty.render(msg, True, color)
    screen.blit(mesg, [scrn_width / 10, scrn_height / 2.5])


# This function is the MAIN one, where basically all the game is stored
def game_start():
    restart = False
    finished = False

    snake = Snake(scrn_width / 2, scrn_height / 2)

    # To randomly place the food wherever on the screen
    food_x = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0

    while not restart:

        # While the game is finished, it will tell the user the message and wait to see if they want to restart or not
        while finished:
            screen.fill(Color.BLACK)
            display_msg("YOU LOST! Press ENTER-Restart or DELETE-Quit", Color.DARK_RED)
            display_score(snake.length - 1)
            pygame.display.update()

            # Allows user to leave if they press "esc" button or "QUIT" or "DELETE"
            # Replay if "ENTER" key pressed
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        restart = True
                        finished = False
                    if event.key == pygame.K_DELETE:
                        restart = True
                        finished = False
                    if event.key == pygame.K_RETURN:
                        game_start()
                elif event.type == QUIT:
                    restart = True
                    finished = False

        event_list = pygame.event.get()

        last_dir_key = []
        for event in event_list:
            if event.type == pygame.QUIT:
                restart = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or \
                        (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
                    last_dir_key = event.key

        if last_dir_key == pygame.K_LEFT:
            snake = update_snake(Direction.WEST, snake)
        elif last_dir_key == pygame.K_RIGHT:
            snake = update_snake(Direction.EAST, snake)
        elif last_dir_key == pygame.K_UP:
            snake = update_snake(Direction.NORTH, snake)
        elif last_dir_key == pygame.K_DOWN:
            snake = update_snake(Direction.SOUTH, snake)
        else:
            snake = update_snake(snake.direction, snake)

        # This is what ends the game if snake eats itself or goes off screen
        if snake.head_x >= scrn_width or snake.head_x < 0 or snake.head_y >= scrn_height or snake.head_y < 0:
            finished = True

        # Draw "Food" using Apple color
        pygame.draw.rect(screen, Color.RED, [food_x, food_y, pixel_size, pixel_size])

        snake_head = [snake.head_x, snake.head_y]
        for x in snake.xy_list[:-1]:
            if x == snake_head:
                finished = True

        display_score(snake.length - 1)

        pygame.display.update()

        # This adds the points and length to snake while moving the food randomly
        if (snake.head_x == food_x) and (snake.head_y == food_y):
            food_x = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0
            snake.length += 1

        # This controls the snake speed
        clock.tick(speed)

        # Background color
        screen.fill(Color.BLACK)

    # When program finished, prints final score for user
    print("\n\nLast Score: " + str(snake.length - 1))

    # Quits the programs
    pygame.quit()
    quit()


# Starting the code
game_start()
