from wordnet_game import WordnetGame

# Creates word list from file
def get_word_list(word_list_file):
    word_list = [line.upper().split() for line in open((word_list_file), 'r')]
    return word_list

# Executes if mood is invalid
def move_is_invalid(game):
    print('Invalid move, please try again :(\n')
    game.display()

# Executes if mood is valid
def move_is_valid(game):
    game.accept_move()
    print('Nice one :D\n')
    game.display()
    return game

# Validates current move
def validate_move(game):
    if game.relation_set.includes(game.next_word):
        return move_is_valid(game)
    else:
        move_is_invalid(game)
        return game

# Erases last move if possible
def validate_erase_move(game):
    if len(game.so_far) != 1:
        print(f'Last move erased: {game.current_word}\n')
        game.erase_move()
    else:
        print('Cannot erase initial word!\n')
    return game

# Gets user input until a valid input is found
def get_user_input(game):
    while True:
        user_input = input().upper()
        print('\n')
        if user_input == '!':
            game = validate_erase_move(game)
        elif user_input != game.current_word and user_input not in game.so_far:
            game.next_word = user_input
            break
        game.display()
    return game

# Performs current round
def play_round(game):
    game = get_user_input(game)
    game = validate_move(game)
    return game

# Main game loop for current game
def game_loop(game):
    game.show_instructions()
    while game.target_word not in game.so_far:
        game = play_round(game) 
    return game.so_far

# Initializes new game
def new_game(word_list):
    game = WordnetGame(word_list)
    print('\n~~~~~~~~~~~NEW GAME~~~~~~~~~~~\n')
    finished_game = game_loop(game)
    print(f"\nCongratulations! You reached the target word in {len(finished_game) - 1} moves!\n\n\n")

# Start program
def start():
    word_list_file = 'word_pairs_10_away'
    word_list = get_word_list(word_list_file)
    while True:
        new_game(word_list)

start()