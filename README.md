# wordnet-game
A simple puzzle game based on WordNet's synsets, written in Python.

The repository includes the driver file (wordnet_game.py), a class file (relation_set.py) and a list of word pairs (word_pair.py).

The driver file contains code for the game logic, while the class file contains the RelationSet class, which is used to validate moves.

RelationSet:

-An object of this class is a set of all Wordnet Synsets and sub-Synsets of a given word within a user-defined amount of layers.

-A new object takes two inputs: a word (as a string) and an integer, which represents the layers of sub-relations to be retrieved.

-When an instance is created, the related terms are immediately retrieved by calling the private methods within the class.

-The user can call the public method "includes" with another word as an argument to return a Boolean value: True if the RelationSet includes any Synset of this word, False if it doesn't.
