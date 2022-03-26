import random
import pygame

def load_dict_word(file_name):
    file = open(file_name, encoding='UTF-8')
    words = file.readlines()
    file.close()
    return [word[:5].upper() for word in words]

DICT_GUESSING = load_dict_word('portuguese_words.txt')
DICT_ANSWERS = load_dict_word('portuguese_words.txt')
ANSWER = random.choice(DICT_ANSWERS)

WIDTH = 500
HEIGHT = 600
margin = 10
T_margin = 100
B_margin = 90
LR_margin = 90

GREY = (70,70,80)
GREEN = (6,214,160)
YELLOW = (255,209,102)

input = ''
guesses = []
alphabet = "ABCDEFJGHIJKLMNOPQRSTUVXWYZ"
unguessed = alphabet
game_over = False

pygame.init()
pygame.font.init()
pygame.display.set_caption("Wordle")

SQ_size = (WIDTH-4*margin-2*LR_margin)//5
FONT = pygame.font.SysFont('free sans bold', SQ_size)
FONT_SMALL = pygame.font.SysFont('free sans bold', SQ_size//2)

def determine_unguessed_letters(guesses):
    guessed_letters = ''.join(guesses)
    unguessed_letters = ''
    for letter in alphabet:
        if letter not in guessed_letters:
            unguessed_letters = unguessed_letters + letter
    return unguessed_letters

def determine_color(guess, j):
    letter = guess[j]
    if letter == ANSWER[j]:
        return GREEN
    elif letter in ANSWER:
        n_target = ANSWER.count(letter)
        n_correct = 0
        n_occurrence = 0
        for i in range(5):
            if guess[i] == letter:
                if i<=j:
                    n_occurrence += 1
                if letter == ANSWER[i]:
                    n_correct += 1
        if n_target - n_correct - n_occurrence >= 0:
            return YELLOW
    return GREY

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# animation loop
animation = True
while animation:

    # background
    screen.fill('white')

    # draw unguessed letter
    letters = FONT_SMALL.render(unguessed, False, GREY)
    surface = letters.get_rect(center=(WIDTH//2, T_margin//2))
    screen.blit(letters, surface)

    # draw guesses
    y = T_margin
    for i in range(6):
        x = LR_margin
        for j in range(5):

            # square
            square = pygame.Rect(x, y, SQ_size, SQ_size)
            pygame.draw.rect(screen, GREY, square, width=2, border_radius=3)

            # letters/words that have already been guessed
            if i < len(guesses):
                color = determine_color(guesses[i],j)
                pygame.draw.rect(screen, color, square, border_radius=3)
                letter = FONT.render(guesses[i][j], False, (255,255,255))
                surface = letter.get_rect(center = (x+SQ_size//2, y+SQ_size//2))
                screen.blit(letter, surface)

            # user text input (next guess)
            if i == len(guesses) and j < len(input):
                letter = FONT.render(input[j], False, GREY)
                surface = letter.get_rect(center=(x + SQ_size // 2, y + SQ_size // 2))
                screen.blit(letter, surface)

            x += SQ_size + margin
        y += SQ_size + margin

    # show the correct answer after the game over
    if len( guesses) == 6 and guesses[5] != ANSWER:
        game_over = True
        letters = FONT.render(ANSWER, False, GREY)
        surface = letters.get_rect(center=(WIDTH//2, HEIGHT -B_margin//2 - margin))
        screen.blit(letters, surface)

    # update the screen
    pygame.display.flip()

    # track user interation
    for event in pygame.event.get():
        # closing the window
        if event.type == pygame.QUIT:
            animation = False

        # user presses key
        elif event.type == pygame.KEYDOWN:
            # escape key to quit the animation
            if event.key == pygame.K_ESCAPE:
                animation = False

            # backspace to correct user input
            if event.key == pygame.K_BACKSPACE:
                if len(input) > 0:
                    input = input [:len(input)-1]

            # return key to quit the animation
            elif event.key == pygame.K_RETURN:
                if len(input) == 5 and input in DICT_GUESSING:
                    guesses.append(input)
                    unguessed = determine_unguessed_letters(guesses)
                    input = ''
                    game_over = True if input == ANSWER else False
                    input = ''

            # space bar to restart
            elif  event.key == pygame.K_SPACE:
                game_over = False
                ANSWER = random.choice(DICT_ANSWERS)
                guesses = []
                unguessed = alphabet
                input = ''

            # regular text input
            elif len(input) < 5 and not game_over:
                input = input + event.unicode.upper()
                print(input)
