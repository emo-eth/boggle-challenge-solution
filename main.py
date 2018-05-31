import random
import json
import pickle
from pathlib import Path

from TrieNode import TrieNode


def generate_board(length):
    """
    This function generates a square board, with each "space" within the
    board containing a lowercase letter from the English language.

    @param length: an integer representing the length and width of the
                   board.
    @returns: a two-dimensional array representing the board.
    """
    board = []
    for x in range(length):
        row = []
        for y in range(length):
            char = chr(random.randint(97, 122))
            row.append(char)
        board.append(row)
    return board


def build_dictionary_trie():
    """
    Builds a trie from dictionary data and pickles it for future usage.

    @returns: TrieNode instance representing root node of trie.
    """
    trie = TrieNode()
    with open('words_dictionary.json') as file:
        english_dict = json.load(file)
    for word in english_dict:
        trie.insert(word)
    with open('dictionary_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return trie


def load_trie():
    """
    Either loads trie data from a pickle file if said file already 
    exists, or builds and returns a new trie.

    @returns: TrieNode instance representing root node of trie.
    """
    trie_pickle_file = Path("dictionary_trie.pickle")
    if trie_pickle_file.exists():
        print("\nReading pickled trie data...")
        with open(trie_pickle_file, 'rb') as handle:
            return pickle.load(handle)
    else:
        print("\nNo pickled data exists. Building new trie...")
        return build_dictionary_trie()


def search_board(board):
    """
    This is the "kickoff" function which starts the recursive algorithm
    from each position on the board, collecting valid words along the
    way.

    @param board: a two-dimensional array representing the board.
    @returns: a list of valid words found in the board.
    """
    dict_trie = load_trie()
    valid_words = set()
    for row in range(len(board)):
        for col in range(len(board)):
            current_pos = (row, col)
            recursive_search(board, current_pos, [], valid_words, dict_trie)
    return valid_words


def recursive_search(board, current_pos, visited, valid_words, dict_trie):
    """
    Recursively searches through the board for valid english words.

    @param board: a two-dimensional array representing the board.
    @param current_pos: a tuple representing the coordinates of the
                        currently examined node.
    @param visited: a list of tuples representing coordinates that have
                    already been visited.
    @param valid_words: a list of the valid words that have been found.
    @param dict_trie: a trie constructed from the english dictionary.
    @returns: None.
    """
    new_visited = visited[:]
    new_visited.append(current_pos)
    if len(new_visited) > 2:
        word = convert_coordinates_to_word(board, new_visited)
        if dict_trie.search(word) and word not in valid_words:
            valid_words.add(word)
        elif not dict_trie.valid_prefix(word):
            return
    row = current_pos[0]
    col = current_pos[1]
    max_val = len(board) - 1
    positions = {
        'top':          { 'can_visit': row > 0, 
                          'coords': (row - 1, col) 
                        },
        'top_right':    { 'can_visit': row > 0 and col < max_val,
                          'coords': (row - 1, col + 1) 
                        },
        'right':        { 'can_visit': col < max_val,
                          'coords': (row, col + 1) 
                        },
        'bottom_right': { 'can_visit': row < max_val and col < max_val,
                          'coords': (row + 1, col + 1) 
                        },
        'bottom':       { 'can_visit': row < max_val,
                          'coords': (row + 1, col) 
                        },
        'bottom_left':  { 'can_visit': row < max_val and col > 0,
                          'coords': (row + 1, col - 1) 
                        },
        'left':         { 'can_visit': col > 0,
                          'coords': (row, col - 1) 
                        },
        'top_left':     { 'can_visit': col > 0 and row > 0,
                          'coords': (row - 1, col - 1) 
                        }
    }
    for position in positions.values():
        if position['can_visit'] and position['coords'] not in new_visited:
            recursive_search(board, position['coords'], new_visited, 
                             valid_words, dict_trie)


def convert_coordinates_to_word(board, visited):
    """
    Converts a list of tuple coordinates (held in the visited list) into 
    a string by looking up the characters on the board.

    @param board: a two-dimensional array representing the board.
    @param visited: a list of tuples representing coordinates that have
                    already been visited.
    """
    letters = []
    for tup in visited:
        row = tup[0]
        col = tup[1]
        letters.append(board[row][col])
    return ''.join(letters)


def pretty_print_board(board):
    """
    Prints the board in a way that actually somewhat resembles a board.

    @param board: a two-dimensional array representing the board.
    @returns: None.
    """
    for row in board:
        for val in row:
            print(f' {val} ', end='')
        print()


if __name__ == '__main__':
    import sys

    length = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    board = generate_board(length)
    print('\ngame board:\n')
    pretty_print_board(board)
    found_values = search_board(board)
    print('\nfound words:\n')
    print(found_values)