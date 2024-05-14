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
def create_snake(pixel_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, green, [x[0], x[1], pixel_size, pixel_size])


# This is just to display messages, mainly the ending message ("You Lost")
def display_msg(msg, color):
    mesg = font_sty.render(msg, True, color)
    screen.blit(mesg, [scrn_width / 10, scrn_height / 2.5])


# This function is the MAIN one, where basically all the game is stored
def game_start():
    restart = False
    finished = False

    x1 = scrn_width / 2
    y1 = scrn_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    snake_length = 1

    # To randomly place the food wherever on the screen
    foodx = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
    foody = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0

    while not restart:

        # While the game is finished, it will tell the user the message and wait to see if they want to restart or not
        while finished == True:
            screen.fill(black)
            display_msg("YOU LOST! Press ENTER-Restart or DELETE-Quit", dark_red)
            display_score(snake_length - 1)
            pygame.display.update()

            # Allows user to leave if they press "esc" button or "QUIT" or "DELETE"
            # Replay if "ENTER" key pressed
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        restart = True
                        finished = False
                    if event.key == pygame.K_BACKSPACE:
                        restart = True
                        finished = False
                    if event.key == pygame.K_RETURN:
                        game_start()
                elif event.type == QUIT:
                    restart = True
                    finished = False

        # Repetition of if you click the corner "X", you can leave
        # Establishes directions for all the arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -pixel_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = pixel_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -pixel_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = pixel_size
                    x1_change = 0

        # This is the changes in direction
        x1 += x1_change
        y1 += y1_change

        # This is what ends the game if snake eats itself or goes off screen
        if x1 >= scrn_width or x1 < 0 or y1 >= scrn_height or y1 < 0:
            finished = True

        # "Food"/Apple color
        pygame.draw.rect(screen, red, [foodx, foody, pixel_size, pixel_size])

        # This creates the "head" of the snake
        HeadOfSnake = []
        HeadOfSnake.append(x1)
        HeadOfSnake.append(y1)
        snake_List.append(HeadOfSnake)
        if len(snake_List) > snake_length:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == HeadOfSnake:
                finished = True

        # Starts programs, creating snake and displaying the score
        create_snake(pixel_size, snake_List)
        display_score(snake_length - 1)

        pygame.display.update()

        # This adds the points and length to snake while moving the food randomly
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, scrn_width - pixel_size) / 10.0) * 10.0
            foody = round(random.randrange(0, scrn_height - pixel_size) / 10.0) * 10.0
            snake_length += 1

        # This controls the snake speed
        clock.tick(speed)

        # Background color
        screen.fill(black)

    # When program finished, prints final score for user
    print("\n\nLast Score: " + str(snake_length - 1))

    # Quits the programs
    pygame.quit()
    quit()

# Starting the code
game_start()
