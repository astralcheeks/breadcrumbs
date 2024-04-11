# Wordnet Game
A simple puzzle game based on WordNet's synsets, written in Python.

The repository includes the **driver file** (wordnet_game.py), 2 **class files** (relation_set.py and wordnet_game.py) and **lists of word pairs** (word_pair_x_away.py).

The driver file contains code for the game logic. The wordnet_game file contains the WordnetGame class, which represents the game board. The relation_set file contains the RelationSet class, which is used to validate moves.


**WordnetGame**:

An object of this class represents the state of an active gameboard.

It takes a list of word pairs as input and selects a random pair for the starter word and target word.
Its methods can then be used to validate or erase moves, display the current game board, and display the game's instructions.


**RelationSet**:

An object of this class is a set of all Wordnet Synsets and sub-Synsets of a given word within a user-defined amount of layers.

A new RelationSet object takes two inputs: a word (as a string) and an integer, which represents the layers of sub-relations to be retrieved.

When an instance is created, the related terms are immediately retrieved by calling the private methods within the class.

The user can call the public method *includes* with another word as an argument to return a Boolean value: *True* if the RelationSet includes any Synset of this word, *False* if it doesn't.
