import pygame
import random

from pygame import QUIT

# Initialize the program
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 112)
black = (0, 0, 0)
red = (252, 58, 58)
dark_red = (184, 0, 40)
green = (46, 117, 46)
blue = (0, 125, 184)

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
    value = font_score.render("YOUR SCORE: " + str(score), True, white)
    screen.blit(value, [0, 0])


# This creates the snake
def draw_snake(pixel_size, snake):
    for x in snake.xy_list:
        pygame.draw.rect(screen, green, [x[0], x[1], pixel_size, pixel_size])


def update_snake(event_list, snake):
    # x1_change = 0
    # y1_change = 0

    # Repetition of if you click the corner "X", you can leave
    # Establishes directions for all the arrow keys
    for event in event_list:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.x1_change = -pixel_size
                snake.y1_change = 0
            elif event.key == pygame.K_RIGHT:
                snake.x1_change = pixel_size
                snake.y1_change = 0
            elif event.key == pygame.K_UP:
                snake.y1_change = -pixel_size
                snake.x1_change = 0
            elif event.key == pygame.K_DOWN:
                snake.y1_change = pixel_size
                snake.x1_change = 0

    # This is the changes in direction
    snake.x1 += snake.x1_change
    snake.y1 += snake.y1_change

    # This creates the "head" of the snake
    snake_head = [snake.x1, snake.y1]
    snake.xy_list.append(snake_head)
    if len(snake.xy_list) > snake.length:
        del snake.xy_list[0]

    # Starts programs, creating snake and displaying the score
    draw_snake(pixel_size, snake)
    return snake


# This is just to display messages, mainly the ending message ("You Lost")
def display_msg(msg, color):
    mesg = font_sty.render(msg, True, color)
    screen.blit(mesg, [scrn_width / 10, scrn_height / 2.5])


class Snake:
    xy_list: list
    length: int
    x1: int
    y1: int
    x1_change: int
    y1_change: int

    def __init__(self, x1, y1):
        self.xy_list = []
        self.length = 1
        self.x1 = x1
        self.y1 = y1
        self.x1_change = 0
        self.y1_change = 0


# This function is the MAIN one, where basically all the game is stored
def game_start():
    restart = False
    finished = False

    snake = Snake(scrn_width / 2, scrn_height / 2)

    # To randomly place the food wherever on the screen
    foodx = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
    foody = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0

    while not restart:

        # While the game is finished, it will tell the user the message and wait to see if they want to restart or not
        while finished:
            screen.fill(black)
            display_msg("YOU LOST! Press ENTER-Restart or DELETE-Quit", dark_red)
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

        for event in event_list:
            if event.type == pygame.QUIT:
                restart = True

        snake = update_snake(event_list, snake)

        # This is what ends the game if snake eats itself or goes off screen
        if snake.x1 >= scrn_width or snake.x1 < 0 or snake.y1 >= scrn_height or snake.y1 < 0:
            finished = True

        # "Food"/Apple color
        pygame.draw.rect(screen, red, [foodx, foody, pixel_size, pixel_size])

        snake_head = [snake.x1, snake.y1]
        for x in snake.xy_list[:-1]:
            if x == snake_head:
                finished = True

        display_score(snake.length - 1)

        pygame.display.update()

        # This adds the points and length to snake while moving the food randomly
        if (snake.x1 == foodx) and (snake.y1 == foody):
            foodx = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
            foody = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0
            snake.length += 1

        # This controls the snake speed
        clock.tick(speed)

        # Background color
        screen.fill(black)

    # When program finished, prints final score for user
    print("\n\nLast Score: " + str(snake.length - 1))

    # Quits the programs
    pygame.quit()
    quit()


# Starting the code
game_start()
