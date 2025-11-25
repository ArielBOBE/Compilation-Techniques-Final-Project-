# Lexer Class for Tokenizing Input Strings (Chess notation)
'''
Lexeme → TOKEN Pairing:
1. Pieces :
    K, Q, R, B, N → PIECE
2. File Letter :
    a, b, c, d, e, f, g, h → FILE, used in `<square>` and `<disamb>`
3. Rank Digits :
    1, 2, 3, 4, 5, 6, 7, 8 → RANK, used in `<square>` and `<disamb>`
4. Square:
    [a-h][1-8] → SQUARE
5. Capture :
    1.   `x` → CAPTURE
6. Check :
    1.   `+` → CHECK
    2.   `#` → CHECKMATE
7. Promotion:
    1.   `=` → PROMOTION
8. Castling:
    1.   O-O   → CASTLE_KINGSIDE
    2.   O-O-O → CASTLE_QUEENSIDE
9. End of File
    "" → EOF

Returns a list of Token objects from input string.
'''
from token import Token

class Lexer:
    def __init__(self, inputString):
        self.input_string   = inputString
        self.cursor_pos     = 0
        self.tokens         = []
        self.VALID_PIECES   = {'K', 'Q', 'B', 'N', 'R'}                 # set of valid piece characters
        self.VALID_FILES    = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}  # set of valid piece characters
        self.VALID_RANKS    = {'1', '2', '3', '4', '5', '6', '7', '8'}  # set of valid rank characters
        self.CAPTURE        = {'x'}                                     # capture symbol
        self.CHECK          = {'+', '#'}                                # set of check related symbols
        self.PROMOTION      = {'='}                                     # promotion symbol
    
    # Helper function to raise error
    def raiseError(self, message):
        raise ValueError(f'{self.cursor_pos}: {message}')
    
    # Helper function for reading input string
    def tokenize(self):
        s = self.input_string
        n = len(s)

        while self.cursor_pos < n:
            char = s[self.cursor_pos]

            # Castling
            if char == 'O':
                if s[self.cursor_pos:self.cursor_pos+3] == 'O-O':
                    # checks for Queen/Kingside castling
                    if s[self.cursor_pos:self.cursor_pos+5] == 'O-O-O':
                        self.tokens.append(Token('CASTLE_QUEENSIDE','O-O-O' ))
                        self.cursor_pos += 5
                    else:
                        self.tokens.append(Token('CASTLE_KINGSIDE','O-O' ))
                        self.cursor_pos += 3

                # If char is just 'O' alone, raise error
                else:
                    self.raiseError("Found 'O' without following '-O' or '-O-O'.")

            # Pieces
            if char in self.VALID_PIECES:
                self.tokens.append(Token('PIECE', char))
                self.cursor_pos += 1
                continue

            # Files
            if char in self.VALID_FILES:
                # look ahead for to check for rank
                if self.cursor_pos + 1 < n:
                    nxt = s[self.cursor_pos + 1]

                    # Square
                    if nxt in self.VALID_RANKS:
                        square = char + nxt
                        self.tokens.append(Token('SQUARE', square))
                        self.cursor_pos += 2
                        continue
                    
                    # File used for disambiguation or pawn movement
                    else:
                        self.tokens.append(Token('FILE', char))
                        self.cursor_pos += 1
                        continue

            # Ranks
            if char in self.VALID_RANKS:
                self.tokens.append(Token('RANK', char))
                self.cursor_pos += 1
                continue

            # Captures
            if char in self.CAPTURE:
                self.tokens.append(Token('CAPTURE', char))
                self.cursor_pos += 1
                continue

            # Promotion
            if char in self.PROMOTION:
                self.tokens.append(Token('PROMOTION', char))
                self.cursor_pos += 1
                continue

            # Checks
            if char in self.CHECK:
                if char == '+':
                    self.tokens.append(Token('CHECK', char))
                if char == '#':
                    self.tokens.append(Token('CHECKMATE', char))
                self.cursor_pos += 1

            # Unhandled characters
            if char.isspace():
                self.cursor_pos += 1 
                continue

        # End of File
        self.tokens.append(Token('EOF', ''))

        return self.tokens