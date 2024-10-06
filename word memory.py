import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Memory Game")

# Set up font and colors
font = pygame.font.Font(None, 36)  # Smaller font size for the words
small_font = pygame.font.Font(None, 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Larger word pool (more than 100 words)
word_pool = [
    "PYTHON", "MEMORY", "GAME", "DEVELOPER", "PROGRAMMING", "CHALLENGE", "ALGORITHM",
    "FUNCTION", "VARIABLE", "STRING", "LOOP", "OBJECT", "CLASS", "METHOD", "DEBUGGING",
    "COMPUTER", "KEYBOARD", "SCREEN", "CONDITION", "INPUT", "OUTPUT", "SYNTAX", "ERROR",
    "MODULE", "PACKAGE", "IMPORT", "EXCEPTION", "LIST", "TUPLE", "DICTIONARY", "SET", 
    "DATA", "INDEX", "FOR", "WHILE", "IF", "ELSE", "ELIF", "TRUE", "FALSE", "NONE", 
    "RETURN", "PRINT", "INT", "FLOAT", "BOOL", "STRING", "COMMENT", "BLOCK", "INDENTATION",
    "RECURSION", "STACK", "QUEUE", "PRIORITY", "SEARCH", "SORT", "MERGE", "SPLIT", 
    "BINARY", "TREE", "GRAPH", "NODE", "EDGE", "VERTEX", "DFS", "BFS", "INHERITANCE", 
    "POLYMORPHISM", "ENCAPSULATION", "ABSTRACTION", "INTERFACE", "IMPLEMENTATION", 
    "CONSTRUCTOR", "DESTRUCTOR", "ARGUMENT", "PARAMETER", "CALL", "REFERENCE", "POINTER", 
    "ARRAY", "ELEMENT", "INDEXING", "SLICE", "MAP", "FILTER", "REDUCE", "GENERATOR", 
    "DECORATOR", "LAMBDA", "ASYNC", "AWAIT", "THREAD", "PROCESS", "CONCURRENCY", "PARALLELISM", 
    "DATABASE", "SQL", "NOSQL", "QUERY", "JOIN", "TABLE", "ROW", "COLUMN", "SCHEMA", 
    "NORMALIZATION", "TRANSACTION", "COMMIT", "ROLLBACK"
]

# Number of words to display in the game
WORDS_TO_DISPLAY = 30

# Timer for how long the word list is shown
DISPLAY_TIME = 120  # 2 minutes in seconds

# Function to display text on the screen
def draw_text(text, font, color, x, y, center=True):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_obj, text_rect)

# Function to display a button ( a lot of tutorials went into this D: )
def draw_button(text, x, y, w, h, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, GREEN, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    draw_text(text, small_font, WHITE, x + w / 2, y + h / 2)

# Function to compare the input words with the original list
def compare_words(user_words, correct_words):
    score = 0
    for word in user_words:
        if word.upper() in correct_words:
            score += 1
    return score

# Main game function
def word_memory_game():
    running = True
    game_state = "showing"
    start_time = time.time()
    user_input = ""
    user_words = []
    score = 0

    # Randomly select 30 words from the larger word pool
    displayed_words = random.sample(word_pool, WORDS_TO_DISPLAY)

    while running:
        screen.fill(WHITE)

        if game_state == "showing":
            # Time remaining
            elapsed_time = time.time() - start_time
            remaining_time = DISPLAY_TIME - int(elapsed_time)

            # Display word list in two columns and countdown timer
            column1_x = WIDTH // 4
            column2_x = 3 * WIDTH // 4
            for i, word in enumerate(displayed_words):
                if i < WORDS_TO_DISPLAY // 2:
                    draw_text(word, font, BLACK, column1_x, 50 + i * 20, center=True)  # First column
                else:
                    draw_text(word, font, BLACK, column2_x, 50 + (i - WORDS_TO_DISPLAY // 2) * 20, center=True)  # Second column

            draw_text(f"Time left: {remaining_time} seconds", small_font, BLACK, WIDTH // 2, HEIGHT - 50)

            if remaining_time <= 0:
                game_state = "typing"
                user_input = ""
                user_words = []

        elif game_state == "typing":
            # Display instructions and input box for the player to type words
            draw_text("Type words you remember and press DONE", small_font, BLACK, WIDTH // 2, 50)
            draw_text(user_input, font, BLACK, WIDTH // 2, HEIGHT // 2)

            # DONE button
            draw_button("DONE", WIDTH // 2 - 50, HEIGHT - 100, 100, 50, RED, lambda: set_state_done(displayed_words))

        elif game_state == "done":
            # Show score
            draw_text(f"You remembered {score} out of {WORDS_TO_DISPLAY} words!", font, BLACK, WIDTH // 2, HEIGHT // 2)
            draw_text("Press ESC to exit or Enter to play again", small_font, BLACK, WIDTH // 2, HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "typing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    user_words.append(user_input.upper())
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode.upper()

            if game_state == "done" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reset for a new game
                    game_state = "showing"
                    start_time = time.time()
                    displayed_words = random.sample(word_pool, WORDS_TO_DISPLAY)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()

    pygame.quit()

# Function to transition to the "done" state and calculate score
def set_state_done(correct_words):
    global score, user_words
    score = compare_words(user_words, correct_words)
    game_state = "done"

# Run the game
word_memory_game()