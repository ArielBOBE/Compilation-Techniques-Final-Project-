# Parser Class for Parsing using RDP and LL(1) Techniques
# X next to thing denots finished
# <move>		::= <castle> | <pawn_move> | <piece_move>
# <castle>X		::= "O-O" | "O-O-O"
# <piece_move>X ::= <piece> <disambig> <capture> <square> <check>
# <pawn_move> 	::= <square> <promotion> <check>
# 			     | <file> <capture> <square> <promotion> <check>
# <disambig> 	::= <file> | <rank> | <square> | ε
# <capture> 	::= "x" | ε
# <promotion> 	::= "=" <piece> | ε
# <check>		::= "+" | "#" | ε
# <square>		::= <file> <rank>
# <file> 		::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h"
# <rank> 		::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
# <piece> 		::= "N" | "B" | "R" | "Q" | "K"

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
3. Square:
    SQUARE
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

from token import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor_pos = 0 # pointer


    def raiseError(self, message):
        current_token = self.lookahead()
        token_info = f" at position {self.cursor_pos}"
        if current_token != ("EOF", None):
            token_info += f" (token: {current_token.type} = '{current_token.content}')"
        raise SyntaxError(message + token_info)

    def getTokens(self):
        return self.tokens 
    
    def lookAhead(self):
        if self.cursor_pos < len(self.tokens): # looks ahead only if available
            return self.tokens[self.cursor_pos]
        else:
            return ("EOF", None)
        
    # if current token matches the expected type, move cursor up and return token
    def match(self, token_type):
        current_token = self.lookAhead()

        if current_token.type == token_type:
            self.cursor_pos += 1
            return current_token
        self.raiseError(f"Expected {token_type}, got {current_token.type}")

    def parseMove(self):
        current_token = self.lookAhead()

        if current_token.type in ["CASTLE_KINGSIDE", "CASTLE_QUEENSIDE"]:
            return self.parseCastle()
        elif current_token.type == "PIECE":
            return self.parsePieceMove()

    def parseCastle(self):
        current_token = self.lookAhead()
        if current_token.content == "O-O":
            self.match("CASTLE_KINGSIDE") # move cursor up 
            return {"type": "castle", "side": "king"} 
        elif current_token.content == "O-O-O":
            self.match("CASTLE_QUEENSIDE")
            return {"type": "castle", "side": "queen"}
        self.raiseError(f"Expected CASTLE_KINGSIDE or CASTLE_QUEENSIDE, got {current_token.type}")
    
    def parsePieceMove(self):
        piece = self.match("PIECE")
        next = self.lookAhead()

        disambig = None
        # checking for disambig
        if next.type in ["FILE", "RANK", "SQUARE"]:
            disambig = self.match(next.type)
        
        # checking for capture
        capture = False
        if self.lookAhead().type == "CAPTURE":
            self.match("CAPTURE")
            capture = True
        
        # checking for square
        square = ""
        if next.type == "SQUARE":
            square = self.match("SQUARE")
        
        # checking for check/checkmate
        check = None
        if next.type in ["CHECK", "CHECKMATE"]:
            check = self.match(next.type)
        
        return {"piece": piece.content, "disambig": disambig.content, "capture": capture, "square": square.content, "check": check.content}