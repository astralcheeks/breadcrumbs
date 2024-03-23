import random
from relation_set import RelationSet

def get_word_list(word_list_file):
    word_list = [line.upper().split() for line in open((word_list_file), 'r')]
    return word_list

# Prints current game
def print_game(current_game):
    for item in current_game:
        print(f'{item} \n ↓')

# Executes if mood is invalid
def move_is_invalid(current_game):
    print('Invalid move, please try again :(\n')
    print_game(current_game)

# Executes if mood is valid
def move_is_valid(current_game, next_word):
    current_game.append(next_word)
    print('Nice one :D\n')
    print_game(current_game)
    return current_game, next_word

# Validates current move
def validate_move(current_relation_set, current_word, next_word, current_game):
    if current_relation_set.includes(next_word):
        return move_is_valid(current_game, next_word)
    else:
        move_is_invalid(current_game)
        return current_game, current_word
        
# Erases last move
def erase_move(current_game, current_word):
    print(f'Last move erased: {current_word}\n')
    current_game.remove(current_word)
    current_word = current_game[-1]
    current_relation_set = RelationSet(current_word, limit=2)
    return current_game, current_word, current_relation_set

# Checks that the last move can be erased
def validate_erase_move(current_game, current_word, current_relation_set):
    if len(current_game) != 1:
        current_game, current_word, current_relation_set = erase_move(current_game, current_word)
    else:
        print('Cannot erase initial word!\n')
    return current_game, current_word, current_relation_set

# Gets user input until a valid input is found
def get_user_input(current_game, current_word):
    current_relation_set = RelationSet(current_word, limit=2)
    while True:
        user_in = input().upper()
        print('\n')
        if user_in == '!':
            current_game, current_word, current_relation_set = validate_erase_move(current_game, current_word, current_relation_set)
        elif user_in != current_word and user_in not in current_game:
            next_word = user_in
            break
        print_game(current_game)
    return current_game, current_word, next_word, current_relation_set

# Performs current round
def play_round(current_game, current_word):
    current_game, current_word, next_word, current_relation_set = get_user_input(current_game, current_word)
    current_game, current_word = validate_move(current_relation_set, current_word, next_word, current_game)
    return current_game, current_word

# Displays game instructions
def display_instructions(starter_word, target_word):
    print(f'Starter word: {starter_word}')
    print(f'Target word: {target_word}\n')
    print(f'Enter your next move (or ! to erase your last move):\n\n{starter_word}\n ↓')

# Intializes game for new game
def intialize_game(starter_word):
    current_game = [starter_word]
    return current_game

# Main game loop for current game
def game_loop(starter_word, current_word, target_word):
    current_game = intialize_game(starter_word)
    display_instructions(starter_word, target_word)
    while target_word not in current_game:
        current_game, current_word = play_round(current_game, current_word) 
    return current_game

# Generates a pair of random words from wordlist used in current game
def get_game_words(word_list):
    pair = random.choice(word_list)
    starter_word = pair[0]
    target_word = pair[1]
    current_word = starter_word
    return starter_word, current_word, target_word

# Initializes new game
def new_game(word_list):
    print('\n~~~~~~~~~~~NEW GAME~~~~~~~~~~~\n')
    starter_word, current_word, target_word = get_game_words(word_list)
    finished_game = game_loop(starter_word, current_word, target_word)
    print(f"\nCongratulations! You reached the target word in {len(finished_game) - 1} moves!\n\n\n")

# Start program
def start():
    word_list_file = 'word_pairs_6_away'
    word_list = get_word_list(word_list_file)
    while True:
        new_game(word_list)

start()