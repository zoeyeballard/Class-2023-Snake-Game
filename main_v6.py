import pygame
import random

from pygame import QUIT
from enum import Enum


class Color:
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
    pixel_list: list
    length: int
    head_x: int
    head_y: int
    direction: Direction

    def __init__(self, head_x, head_y):
        self.pixel_list = []
        self.length = 1
        self.head_x = round(head_x / pixel_size) * pixel_size
        self.head_y = round(head_y / pixel_size) * pixel_size
        self.direction = Direction.NOT_MOVING


# Initialize the program
pygame.init()

# Size of the pixel
pixel_size = 15

# Screen Dimensions
screen_width = 640
screen_height = 480

screen_width = round(screen_width / (2 * pixel_size)) * 2 * pixel_size
screen_height = round(screen_height / (2 * pixel_size)) * 2 * pixel_size

# Create the Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('ZOEY BALLARD - SNAKE GAME')

# Both of these create the clock_speed
clock = pygame.time.Clock()
clock_speed = 12

# Further Design - Fonts! :D
font_msg = pygame.font.SysFont("twcen", 25)
font_score = pygame.font.SysFont("agencyfb", 35)


# This is a function to display the score while the user plays
def display_score(score):
    score_rendered = font_score.render("YOUR SCORE: " + str(score), True, Color.WHITE)
    screen.blit(score_rendered, [0, 0])


"""
Name: update_snake
Purpose: Moves snake based on input direction (N, E, S, W)
Parameters: new_direction (input) - the updated direction to move the snake
            snake (input/output) - snake object
                 direction      - current snake direction
                 head_x, head_y - head of snake
                 pixel_list     - list of snake pixels
                 length         - length of the snake in pixels         
"""
def update_snake(new_direction, snake):
    x_delta = 0
    y_delta = 0

    # Repetition of if you click the corner "X", you can leave
    # Establishes directions for all the arrow keys
    if new_direction == Direction.WEST:
        x_delta = -pixel_size
    elif new_direction == Direction.EAST:
        x_delta = pixel_size
    elif new_direction == Direction.NORTH:
        y_delta = -pixel_size
    elif new_direction == Direction.SOUTH:
        y_delta = pixel_size

    # This is the changes in direction
    snake.head_x += x_delta
    snake.head_y += y_delta

    # This creates the "head" of the snake
    snake_head = [snake.head_x, snake.head_y]
    snake.pixel_list.append(snake_head)
    if len(snake.pixel_list) > snake.length:
        del snake.pixel_list[0]

    # Starts programs, creating snake and displaying the score
    for pixel in snake.pixel_list:
        pygame.draw.rect(screen, Color.GREEN, [pixel[0], pixel[1], pixel_size, pixel_size])

    # Update direction
    snake.direction = new_direction

    return snake


# This is just to display messages, mainly the ending message ("You Lost")
def display_msg(msg, color):
    msg_rendered = font_msg.render(msg, True, color)
    screen.blit(msg_rendered, [screen_width / 8, screen_height / 2.5])


# This function is the MAIN one, where basically all the game is stored
def game_start():
    restart = False
    finished = False

    snake = Snake(screen_width / 2, screen_height / 2)

    # To randomly place the apple wherever on the screen
    apple_x = round(random.randrange(0, screen_width - pixel_size) / pixel_size) * pixel_size
    apple_y = round(random.randrange(0, screen_height - pixel_size) / pixel_size) * pixel_size

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
        if snake.head_x < 0 or snake.head_x >= screen_width or \
                snake.head_y < 0 or snake.head_y >= screen_height:
            finished = True

        # Draw apple
        pygame.draw.rect(screen, Color.RED, [apple_x, apple_y, pixel_size, pixel_size])

        snake_head = [snake.head_x, snake.head_y]
        for pixel in snake.pixel_list[:snake.length-1]:
            if pixel == snake_head:
                finished = True

        display_score(snake.length - 1)
        pygame.display.update()

        # This adds the points and length to snake while moving the apple randomly
        if (snake.head_x == apple_x) and (snake.head_y == apple_y):
            apple_x = round(random.randrange(0, screen_width - pixel_size) / pixel_size) * pixel_size
            apple_y = round(random.randrange(0, screen_height - pixel_size) / pixel_size) * pixel_size
            snake.length += 1

        # This controls the snake clock_speed
        clock.tick(clock_speed)

        # Background color
        screen.fill(Color.BLACK)

    # When program finished, prints final score for user
    print("\n\nLast Score: " + str(snake.length - 1))

    # Quits the programs
    pygame.quit()
    quit()


# Starting the code
game_start()
