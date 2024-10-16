import pygame
import sys
import pandas as pd

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Who Wants to Be a Millionaire")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

# Load a custom font
font = pygame.font.Font(None, 48)  # For menu
game_font = pygame.font.Font(None, 36)  # For game text

# Load the background image and scale it to the screen size
background_image = pygame.image.load("./utils/img/start_background.jpg")  # Replace with your image file
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Sample DataFrame with custom questions, options, and answers
df = pd.read_csv("./utils/db/questions.csv")

# Track the current question index
current_question_index = 0
# Variable to store the feedback message
feedback_message = ""


# Function to display text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
    return text_rect


# Function to draw a button with text on top
def draw_button(text, rect_color, text_color, x, y, w, h):
    pygame.draw.rect(screen, rect_color, (x, y, w, h))
    return draw_text(text, game_font, text_color, screen, x + w // 2, y + h // 2)


# Function to draw the current question and options with buttons
def draw_current_question(screen, question_index):
    question = df["Question"].iloc[question_index]
    draw_text(question, game_font, WHITE, screen, WIDTH // 2, HEIGHT // 10)

    # Draw options as buttons
    options = ["Option_A", "Option_B", "Option_C", "Option_D"]
    button_height = 60
    button_width = 500
    button_x = WIDTH // 2 - button_width // 2

    button_y_start = HEIGHT // 2 - 100
    for i, option in enumerate(options):
        option_text = f"{chr(65 + i)}) {df[option].iloc[question_index]}"  # A), B), C), D)
        draw_button(option_text, GRAY, WHITE, button_x, button_y_start + i * (button_height + 20), button_width,
                    button_height)


# Function to display feedback
def draw_feedback_message(screen, message):
    draw_text(message, game_font, WHITE, screen, WIDTH // 2, HEIGHT - 50)


# Menu function
def menu_loop():
    while True:
        screen.blit(background_image, (0, 0))  # Draw background
        draw_text("Who Wants to Be a Millionaire", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

        # Create Start Game and Exit buttons
        start_button = draw_text("Start Game", font, GREEN, screen, WIDTH // 2, HEIGHT // 2)
        exit_button = draw_text("Exit", font, GREEN, screen, WIDTH // 2, HEIGHT // 2 + 100)

        pygame.display.flip()

        # Event handling for menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    print("Starting Game!")
                    game_loop()  # Start the game
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()


# Game loop function
def game_loop():
    global current_question_index, feedback_message
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw the current question and options
        draw_current_question(screen, current_question_index)
        draw_feedback_message(screen, feedback_message)

        pygame.display.flip()

        # Event handling for game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                # Check for option clicks (using the same button positions)
                options = ["Option_A", "Option_B", "Option_C", "Option_D"]
                button_y_start = HEIGHT // 2 - 100
                button_height = 60
                button_width = 500
                button_x = WIDTH // 2 - button_width // 2

                for i in range(4):  # Four options (A, B, C, D)
                    option_rect = pygame.Rect(button_x, button_y_start + i * (button_height + 20), button_width,
                                              button_height)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        print(f"You clicked on: {chr(65 + i)}")
                        if chr(65 + i) == df["CorrectAnswer"].iloc[current_question_index]:  # Check if correct
                            feedback_message = "Correct answer!"
                        else:
                            feedback_message = "Incorrect answer. Game Over!"
                            pygame.quit()
                            sys.exit()

                        # Move to the next question
                        current_question_index += 1
                        # Check if we reached the end of questions
                        if current_question_index >= len(df):
                            print("Game Over! You've answered all questions.")
                            pygame.quit()
                            sys.exit()
