import pygame
import random

from pygame import QUIT
from enum import Enum


# Enumeration of Colors
class Color:
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 112)
    BLACK = (0, 0, 0)
    RED = (252, 58, 58)
    DARK_RED = (184, 0, 40)
    GREEN = (0, 158, 76) #46, 117, 46)
    BLUE = (0, 125, 184)
    DARK_GREEN = (34, 68, 61)
    PURPLE = (175, 116, 252)
    LIGHT_GREEN = (40, 250, 85)


# Enumeration of Cardinal Directions
class Direction(Enum):
    NOT_MOVING = -1
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3


# Snake class
class Snake:
    pixel_list: list  # List of pixel locations in the snake
    length: int  # Snake length
    head_x: int  # x-location of the head
    head_y: int  # y-location of the head
    direction: Direction  # Direction of snake movement

    # Initializer for snake class
    def __init__(self, head_x, head_y):
        self.pixel_list = []
        self.length = 1
        head_image = pygame.image.load("C:\\Users\\zoeye\\PycharmProjects\\IMG_1156.PNG").convert()
        # full_head_image = pygame.transform.scale(head_image, (head_x, head_y))
        self.head_x = round(head_x / pixel_size) * pixel_size
        self.head_y = round(head_y / pixel_size) * pixel_size
        full_head_image = pygame.transform.scale(head_image, (self.head_x, self.head_y))
        self.image = full_head_image
        self.direction = Direction.NOT_MOVING


# Initialize the program
pygame.init()

# Size of the pixel
pixel_size = 30

# Screen Dimensions
screen_width = 660
screen_height = 510

# Round screen dimension to even number of pixels
screen_pixels_x = round(screen_width / (2 * pixel_size)) * 2
screen_pixels_y = round(screen_height / (2 * pixel_size)) * 2
screen_width = screen_pixels_x * pixel_size
screen_height = screen_pixels_y * pixel_size

# Create the Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('RCHS SENIOR PROJECT - SNAKE GAME')


# Both of these create the clock_speed
clock = pygame.time.Clock()
clock_speed = 10

# Fonts for message and the score
font_msg = pygame.font.SysFont("twcen", 27)
font_score = pygame.font.SysFont("agencyfb", 40)


"""
Name: move_snake
Purpose: Moves snake based on input direction (N, E, S, W)
Parameters: new_direction (input) - the updated direction to move the snake
            snake (input/output) - snake object
                 direction      - current snake direction
                 head_x, head_y - head of snake
                 pixel_list     - list of snake pixels
                 length         - length of the snake in pixels         
"""
def move_snake(new_direction, snake):
    # These two variables will store the changes in the x and y dimensions
    x_delta = 0
    y_delta = 0

    # This moves the snake one pixel based on the direction
    if new_direction == Direction.WEST:
        x_delta = -pixel_size  # If direction is west, x changed by -1 pixel
    elif new_direction == Direction.EAST:
        x_delta = pixel_size  # If direction is east, x changed by 1 pixel
    elif new_direction == Direction.NORTH:
        y_delta = -pixel_size  # If direction is north, y changed by -1 pixel
    elif new_direction == Direction.SOUTH:
        y_delta = pixel_size  # If direction is south, y changed by 1 pixel

    # This is the changes in direction
    snake.head_x += x_delta
    snake.head_y += y_delta

    # This creates the "head" of the snake, appending the changes into the list of the "head"
    snake_head = [snake.head_x, snake.head_y]
    # screen.blit(snake.image, snake_head)
    snake.pixel_list.append(snake_head)  # Appends snake head to pixel list
    if len(snake.pixel_list) > snake.length:
        del snake.pixel_list[0]  # Deletes the tail of the snake

    # Draws the snake
    for pixel in snake.pixel_list:
        pygame.draw.rect(screen, Color.PURPLE, [pixel[0], pixel[1], pixel_size, pixel_size])

    # Updates direction
    snake.direction = new_direction

    return snake


"""
Name: game_start
Purpose: Starts the snake game itself
Parameters: None    
"""
def game_start():
    restart = False  # Will be used to show if game is over
    finished = False  # Used to show game quit (like by exiting the game, clicking the "X" in the window)
    max_score = 0;

    # Places the snake at the center of the screen at the start of the game
    snake = Snake(screen_width / 2, screen_height / 2)

    # To randomly place the apple wherever on the screen
    apple_x = random.randrange(0, screen_pixels_x) * pixel_size
    apple_y = random.randrange(0, screen_pixels_y) * pixel_size

    while not restart:  # While the game is going

        while finished:  # While it is not finished
            screen.fill(Color.BLACK)  # Colors the screen black

            # Display restart/quit message
            msg_rendered = font_msg.render("YOU LOST! Press ENTER-Restart or DELETE-Quit", True, Color.DARK_RED)
            screen.blit(msg_rendered, [screen_width / 9, screen_height / 2.5])
            current_score = snake.length - 1
            if current_score <= max_score:
                pass
            else:
                max_score = current_score

            # Display score throughout the game
            score_rendered = font_score.render("YOUR SCORE: " + str(snake.length - 1), True, Color.WHITE)
            screen.blit(score_rendered, [0, 0])
            pygame.display.update()

            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # User can leave game if press "esc" key
                        restart = True
                        finished = False
                    if event.key == pygame.K_DELETE:  # User can leave game if press "delete" key
                        restart = True
                        finished = False
                    if event.key == pygame.K_RETURN:  # User restarts game if press "enter" key
                        game_start()
                elif event.type == QUIT:  # User can leave game if press "X" on the screen (in the corner)
                    restart = True
                    finished = False

        # Gets what the user is currently doing and stores it into a list
        event_list = pygame.event.get()

        last_dir_key = []  # This will store the last direction key pressed
        for event in event_list:
            if event.type == pygame.QUIT:  # If "X" pressed in screen corner, can leave
                restart = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_a) or (event.key == pygame.K_d) or \
                        (event.key == pygame.K_w) or (event.key == pygame.K_s):
                    # If the left, right, up, or down key are pressed, become the last direction key
                    last_dir_key = event.key

        # Uses last direction key to move the snake using "move_snake"
        if last_dir_key == pygame.K_a:  # FIRST CALL
            snake = move_snake(Direction.WEST, snake)  # Moves the snake west/left
        elif last_dir_key == pygame.K_d:  # SECOND CALL
            snake = move_snake(Direction.EAST, snake)  # Moves the snake east/right
        elif last_dir_key == pygame.K_w:
            snake = move_snake(Direction.NORTH, snake)  # Moves the snake north/up
        elif last_dir_key == pygame.K_s:
            snake = move_snake(Direction.SOUTH, snake)  # Moves the snake south/down
        else:
            snake = move_snake(snake.direction, snake)
            # If no directions are given, it continues to move the snake in the last direction

        # This is what ends the game if snake goes off screen
        if snake.head_x < 0 or snake.head_x >= screen_width or \
                snake.head_y < 0 or snake.head_y >= screen_height:
            finished = True

        # Draw apple
        apple_image = pygame.image.load("C:\\Users\\zoeye\\PycharmProjects\\export6.png").convert()
        new_apple_image = pygame.transform.scale(apple_image, (round(pixel_size*1), round(pixel_size*1)))
        screen.blit(new_apple_image, (apple_x, apple_y))
        #pygame.draw.rect(screen, Color.RED, [apple_x, apple_y, pixel_size, pixel_size])

        # Checks all locations in the snake expect the head itself to check if it has eaten itself
        snake_head = [snake.head_x, snake.head_y]
        for pixel in snake.pixel_list[:snake.length - 1]:
            if pixel == snake_head:
                finished = True  # If it has, it ends the game.

        # Display current score
        score_rendered = font_score.render("YOUR SCORE: " + str(snake.length - 1), True, Color.WHITE)
        screen.blit(score_rendered, [0, 0])
        pygame.display.update()

        # Increases snake length and assigns a new apple to a random location
        if (snake.head_x == apple_x) and (snake.head_y == apple_y):
            apple_x = random.randrange(0, screen_pixels_x) * pixel_size
            apple_y = random.randrange(0, screen_pixels_y) * pixel_size
            snake.length += 1

        # This controls the snake clock_speed
        clock.tick(clock_speed)

        # Fills the screen with background color of black
        screen_image = pygame.image.load("C:\\Users\\zoeye\\PycharmProjects\\screen2.png").convert()
        screen_full_image = pygame.transform.scale(screen_image, (screen_width, screen_height))
        screen.fill(Color.BLACK)
        screen.blit(screen_full_image, (0, 0))


    # When program finished, prints final score for user (outside of the screen)
    print("\n//////////////////////////////////////////////////////////////////////////////////////////////"
          "\n\n<< ROUND HIGH SCORE: " + str(max_score) + " >>")

    # RCHS Ending Parting Message
    print("\nThis game was meant to serve as a memorabilia for my time at RCHS as I graduate in 2023."
          "\nTo recognize that, I end with this parting haiku poem: "
          "\n\n\tOur story begins"
          "\n\tHere at Richland Collegiate"
          "\n\tTwo years at college"
          "\n\t"
          "\n\tSo we were promised"
          "\n\tRCHS taught me stress"
          "\n\tMental exhaustion"
          "\n\t"
          "\n\tBut I learned a lot"
          "\n\tPlaying this long game of snake"
          "\n\tWith all of my classes"
          "\n\t"
          "\n\tChasing that apple"
          "\n\tOf the best grades and free money"
          "\n\tTo get that high score"
          "\n\t"
          "\n\tCompeting to win"
          "\n\tEven against college students"
          "\n\tBe the best of all"
          "\n\t"
          "\n\tI see now this was"
          "\n\tnever what I truly wanted"
          "\n\tI wanted a home"
          "\n\t"
          "\n\tAnd I found it here"
          "\n\tWith good friends and plenty of laughs"
          "\n\tAnd sweet memories"
          "\n\t"
          "\n\tThanks for helping me"
          "\n\tThrough this game of snake I played"
          "\n\tThat we have all played"
          "\n\t"
          "\n\tTo get where we are"
          "\n\tAnd make it through these two years"
          "\n\tAt RCHS"
          "\n\t"
          "\n\tSo here I say bye"
          "\n\tLeaving you with your high score"
          "\n\tAnd best wishes and luck"
          "\n\t"
          "\n\tFor your next few years"
          "\n\tAt your university"
          "\n\tThe future you to be"
          "\n\t<3")


    # Quits the programs
    pygame.quit()
    quit()


# Starts the game through game_start
game_start()
