# Boggle Solution

## Installation

This script doesn't require any installation. Just download it and it should work right out of the box!

## Usage

Run the following

```bash
python3 main.py
```

If you'd like you can also specify an integer value when invoking from the
command line. This will set the dimensions of the game board.

```bash
python3 main.py 20
```

## Analysis

The crux of this solution is that it uses a trie built from the english
dictionary to facilitate quick lookup for character strings. This approach
greatly enhances the underlying DFS algorithm, because it enables very
efficient lookup as to whether or not a given prefix will lead to any words,
vastly reducing the number of character combinations which need to be checked.

Of course, building the trie can itself be time expensive, so instead of
rebuilding the trie from scratch every time, the trie is pickled upon
construction. On subsequent runs, the program will rebuild the trie from
its pickled state.