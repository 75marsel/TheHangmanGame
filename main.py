import pygame
import math
import random
import sys




pygame.init() # initialize pygame
WIDTH, HEIGHT = 900, 800 
app = pygame.display.set_mode((WIDTH, HEIGHT)) # sets the screen with the given width and height
bg = pygame.image.load("assets/images/background/bg.png") # loads the background image
pygame.display.set_caption("Hangman Game") # sets the title of the window

RADIUS = 24 # radius per element
LETTER_GAP = 15 # gap of each letter
letters = [] # current letters in game session
start_x = round((WIDTH - (RADIUS * 2 + LETTER_GAP) * 13) / 2)
start_y = 600
A_ASCII = 65
for i in range(26):
    x = start_x + LETTER_GAP * 2 + ((RADIUS * 2 + LETTER_GAP) * (i % 13))
    y = start_y + ((i // 13) * (LETTER_GAP + RADIUS * 2))
    letters.append([x, y, chr(A_ASCII + i), True])

# fonts for the game
LETTER_FONT = pygame.font.Font('assets/font/Chalkiez-Regular.ttf', 40)
WORD_FONT = pygame.font.Font('assets/font/Chalkiez-Regular.ttf', 60)
TITLE_FONT = pygame.font.Font('assets/font/Chalkiez-Regular.ttf', 70)
HINT_FONT = pygame.font.Font('assets/font/Chalkiez-Regular.ttf', 30)
LETTER_FONT_US = pygame.font.SysFont('comicsans', 40)
WORD_FONT_US = pygame.font.SysFont('comicsans', 40)
TITLE_FONT_US = pygame.font.SysFont('comicsans', 40)

# load images needed (hangman)
images = []
for i in range(7):
    image = pygame.image.load("assets/images/sprites/"+ str(i) + ".png")
    images.append(image)

hangman_status = 0 # what is the current status of the hangman, directly proportional to the image list
hintlist = open("assets/words/hints.txt").read().splitlines()
wordlist = open("assets/words/words.txt").read().splitlines() # loads the words to be used by the game
word = random.choice(wordlist) # randomly selects one 
current_guess = [] # list as current guess

#enable hints
hints = False

# resets the data
def reset():
    global hangman_status, word, hints, letters
    hints = False
    current_guess.clear()
    hangman_status = 0
    letters.clear()
    for i in range(26):
        x = start_x + LETTER_GAP * 2 + ((RADIUS * 2 + LETTER_GAP) * (i % 13))
        y = start_y + ((i // 13) * (LETTER_GAP + RADIUS * 2))
        letters.append([x, y, chr(A_ASCII + i), True])
    word = random.choice(wordlist)

def update_game_screen():
    app.blit(bg, (0, 0))
    
    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, (255,255,255))
    app.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    # draw word
    display_word = ""
    for letter in word:
        if letter in current_guess:
            display_word += letter + " "
        else:
            if letter == " ":
                display_word += "-"
            else:
                display_word += "_ "
    
    split_word = display_word.split("-")
    split_height = 320
    for s in split_word:
        text = WORD_FONT.render(s, 1, (255,255,255))
        app.blit(text, (WIDTH/2 - text.get_width()/2, split_height))
        split_height += 80

    # draw avaialbel letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.rect(app, (255,255,255), (x-20, y-20, 54, 40), 2)
            text = LETTER_FONT.render(ltr, 1, (255,255,255))
            app.blit(text, (x - text.get_width()/2+6, y - text.get_height()/2))
    
    # check for hints
    if hints:
        pygame.display.set_caption("Hangman Game: You need hints?")
        display_hint_window()
    else:
        pygame.display.set_caption("Hangman Game: By Gappi, Jeric Marcel L.")
        # display tooltip hint
        hint_tip = HINT_FONT.render("PRESS H FOR HINTS!", 1, (255,255,255))
        app.blit(hint_tip, (WIDTH/2 - hint_tip.get_width()/2, y - hint_tip.get_height()/2+80))
        
    app.blit(images[hangman_status], (WIDTH/2-100, (text.get_width()/2)+100))
    pygame.display.update()


def display_hint_window():
    text = HINT_FONT.render("HINT: ", 1, (255,255,255))
    app.blit(text, (x + text.get_width()-870, y - text.get_height()/2+80))
    current_hint = hintlist[wordlist.index(word)]
    text = HINT_FONT.render(current_hint, 1, (255,255,255))
    app.blit(text, (100, y - text.get_height()/2+80))

# displays the win or lost screen
def display_msg_screen(message, mode=0):
    pygame.time.delay(2000)
    app.blit(bg, (0, 0))

    text = WORD_FONT.render(message, 1, (255,255,255))
    app.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2-160 - text.get_height()/2))
    if mode == 1:
        text = WORD_FONT.render("Correct Word: ", 1, (255,255,255))
        app.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
        text = WORD_FONT.render(word, 1, (255,255,255))
        app.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2+80 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    global hangman_status, hints

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    hints = not hints
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            current_guess.append(ltr)
                            if ltr not in word:
                                prev_stat = hangman_status
                                if prev_stat+2 == hangman_status:
                                    hangman_status -= 1
                                if prev_stat+3 == hangman_status:
                                    hangman_status -= 2
                                if prev_stat+4 == hangman_status:
                                    hangman_status -= 3
                                if prev_stat+6 == hangman_status:
                                    hangman_status -= 5
                                if hangman_status + 1 <= 6:
                                    hangman_status += 1
                                elif hangman_status > 6:
                                    hangman_status -= 1
        
        update_game_screen()
        win = True
        for letter in word:
            if letter not in current_guess and letter != " ":
                win = False
                break
        
        if win:
            display_msg_screen("YOU WIN! :D")
            reset()
            run = False
            break

        if hangman_status == 6:
            display_msg_screen("YOU LOST! :(", 1)
            reset()
            run = False
            break
    

def title_screen():
    play_game = True
    while play_game:
        app.blit(bg, (0, 0))
        title_text = TITLE_FONT.render("Hangman Game by Jeric Marcel", 1, (255,255,255))
        app.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 200))
        text = LETTER_FONT.render("Left Click to Start!", 1, (0,0,255))
        app.blit(text, (WIDTH / 2 - text.get_width() / 2, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                pygame.event.clear()
                break



if __name__ == "__main__":
    while True:
        title_screen()
