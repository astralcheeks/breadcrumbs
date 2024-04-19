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

## Background
This game served as the final project for **LING 498: Computational Methods in Linguistics** at Concordia University.

The goals for this project were:
* to test WordNet's ability to capture semantic relationships
* to gain experience working in Python and NLTK
* to build a fun semantic game for my friends to play

## Implementation

You must have both Python and a copy of WordNet installed to run this game.

The repository includes:
* the **driver file** (breadcrumbs.py)
* two **class files** (relation_set.py and wordnet_game.py) and
* files containing **lists of word pairs** (word_pair_x_away.py)

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

* Displays state of the game board

### show_instructions()

* Displays current game's instructions to user, including `starter_word` and `target_word`


## RelationSet

An object of this class is a set of all Wordnet Synsets and sub-Synsets of a given word within a user-defined amount of layers.



A new RelationSet object takes two inputs: a word (as a string) and an integer, which represents the layers of sub-relations to be retrieved.

When an instance is created, the related terms are immediately retrieved by calling the private methods within the class.

### includes()

* Can be called with another word as an argument to return a Boolean value: \
`True` if the RelationSet includes any Synset of this word, `False` if it doesn't

```python
>>> dog_set = RelationSet('dog', layers=2)
>>> dog_set.includes('canine')
True
```

## Word pairs

Just .txt files with pairs of words to be randomly selected when a new game is initialized.

Each file was obtained using a simple script that retained the top 10 000 words in the Brown corpus, then found pairs of words that were of   certain distance from each other according to WordNet's `shortest_path_distance` method.

## Issues/Todo

### 1. Instantly solveable games

Since RelationSet checks word relations recursively, the minimum amount of moves required to win any given game should, in theory, be the shortest path distance between the words divided by the number of layers in the RelationSet.

In practice, this hasn't always been the case. Sometimes games are even instantly solveable. A new script might be necessary to generate word pairs that are guaranteed to be a certain number of moves away from each other.

### 2. Web implementation

Although outside the scope of the class, I would like to deploy a web version of the game at some point, maybe using Flask. I've seen a few third-party JavaScript APIs for WordNet floating around on GitHub, which could eliminate the need for a backend.
