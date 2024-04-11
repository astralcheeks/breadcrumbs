import random
from relation_set import RelationSet

class WordnetGame():
    """"
    An object of this class represents the state of an active WordNet game.

    When a new game instance is created, a list of words must be provided. The
    constructor then selects two random words from the list and assigns them to
    the starter and target words for the current game.
    
    The current word is set to the starter word, and the next word has a default
    value of None until updated to some valid user input. The so_far method is just
    the game board (moves accepted so far) and contains the starter word by default.
    """
    def __init__(self, word_list: list):
        """
        Sets up a new game and initializes parameters.

        Args:
            word_list (list):
                The list of word pairs used to generate the starter word
                and target word for each new game.
        """
        pair = random.choice(word_list)
        self.starter_word = pair[0]
        self.target_word = pair[1]
        self.current_word = self.starter_word
        self.next_word = None
        self.so_far = [self.starter_word]
        self.__update_relation_set()

    def __update_relation_set(self):
        """"
        Updates RelationSet to current word.
        """
        self.relation_set = RelationSet(self.current_word, layers=2)

    def erase_move(self):
        """
        Erases last move.
        """
        self.so_far.remove(self.current_word)
        self.current_word = self.so_far[-1]
        self.__update_relation_set()

    def accept_move(self):
        """
        Updates game to reflect user's latest move.
        """
        self.so_far.append(self.next_word)
        self.current_word = self.next_word
        self.__update_relation_set()
        
    def display(self):
        """
        Displays the game board.
        """
        for item in self.so_far:
            print(f'{item} \n ↓')

    def show_instructions(self):
        """
        Displays instructions to user.
        """
        print(f'Starter word: {self.starter_word}')
        print(f'Target word: {self.target_word}\n')
        print(f'Enter your next move (or ! to erase your last move):\n\n{self.current_word}\n ↓')