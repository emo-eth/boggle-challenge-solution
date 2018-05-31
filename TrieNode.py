class TrieNode():
    
    def __init__(self, chars=None, prefix=''):
        self.children = [None] * 26
        self.word = False
        if chars is not None:
            self.insert(chars, prefix)

    def insert(self, chars, prefix=''):
        if len(chars) > 0:
            # This messiness is necessary to handle non-alpha characters
            index = None
            i = -1
            while index is None:
                i += 1
                index = self.convert_char_to_index(chars[i])
            if self.children[index] is None:
                self.children[index] = TrieNode(chars[1:], prefix + chars[i])
            else:
                self.children[index].insert(chars[1:], prefix + chars[i])
        else:
            self.word = True

    def search(self, chars):
        if len(chars) == 0 and self.word:
            return True
        elif len(chars) == 0 and not self.word: 
            return False
        else:
            index = self.convert_char_to_index(chars[0])
            if self.children[index] is None: 
                return False
            else:
                return self.children[index].search(chars[1:])

    def valid_prefix(self, chars):
        if len(chars) == 0:
            return True if any(self.children) else False
        else:
            index = self.convert_char_to_index(chars[0])
            if self.children[index] is None: 
                return False
            else:
                self.children[index].valid_prefix(chars[1:])

    def convert_char_to_index(self, char):
        """ Accepts [a-zA-Z]. Otherwise returns false. """
        if char.isalpha() and char.istitle():
            return ord(char) - 65
        elif char.isalpha() and not char.istitle():
            return ord(char) - 97
        return None