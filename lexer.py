# Lexer Class for Tokenizing Input Strings (Chess notation)
'''
Lexeme → TOKEN Pairing:
1. Pieces :
    1.   K → KING
    2.   Q → QUEEN
    3.   R → ROOK
    4.   B → BISHOP
    5.   N → KNIGHT
2. File Letter :
    a, b, c, d, e, f, g, h → FILE, used in `<square>` and `<disamb>`
3. Rank Digits :
    1, 2, 3, 4, 5, 6, 7, 8 → RANK, used in `<square>` and `<disamb>`
4. Capture :
    1.   `x` → CAPTURE
5. Check :
    1.   `+` → CHECK
    2.   `#` → CHECKMATE
6. Promotion:
    1.   `=` → PROMOTION_SYMBOL
7. Castling:
    1.   O-O   → CASTLE_KINGSIDE
    2.   O-O-O → CASTLE_QUEENSIDE
8. End of File
    "" → EOF

Returns a list of Token objects from input string.
'''
class Lexer:
    pass