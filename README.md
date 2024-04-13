# Breadcrumbs
A simple puzzle game based on WordNet's synsets, written in Python.

Players are given a starter word and a target word, with the goal being to draw a semantic path between the two:

```console
~~~~~~~~~~~NEW GAME~~~~~~~~~~~

Starter word: TOE
Target word: LOBBY

Enter your next move (or ! to erase your last move):

TOE
 ↓
FOOT
 ↓
FLOOR
 ↓
LOBBY

Congratulations! You reached the target word in 3 moves!

```

## Implementation

The repository includes:
* the **driver file** (breadcrumbs.py)
* two **class files** (relation_set.py and wordnet_game.py) and
* **lists of word pairs** (word_pair_x_away.txt)

The driver file contains code for the game logic. The wordnet_game file contains the WordnetGame class, which represents the game board. The relation_set file contains the RelationSet class, which is used to validate moves.

## WordnetGame

An object of this class represents the state of an active gameboard.

It takes a list of word pairs as input and selects a random pair for the starter word and target word.
Its methods can then be used to validate or erase moves, display the current game board, and display the game's instructions.

### erase_move()

* Removes last word from `so_far`
* Updates `current_word` and `relation_set` accordingly

### accept_move()

* Appends whatever is stored in `next_word` to `so_far`
* Sets the value of `current_word` to `next_word`
* Updates `relation_set` accordingly

### display()

* Displays game board

### show_instructions()

* Displays current game's instructions to user, including `starter_word` and `target_word`


## RelationSet

An object of this class is a set of all Wordnet Synsets and sub-Synsets of a given word within a user-defined amount of layers.

A new RelationSet object takes two inputs: a word (as a string) and an integer, which represents the layers of sub-relations to be retrieved.

When an instance is created, the related terms are immediately retrieved by calling the private methods within the class.

### includes()

* The user can call the public method ```includes()``` with another word as an argument to return a Boolean value: `True` if the RelationSet includes any Synset of this word, `False` if it doesn't.

```python
>>> dog_set = RelationSet('dog', layers=2)
>>> dog_set.includes('canine')
True
```

## Word pairs

Just .txt files with pairs of words to be randomly selected when a new game is initialized.