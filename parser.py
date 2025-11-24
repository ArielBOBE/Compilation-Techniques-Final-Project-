# Parser Class for Parsing using RDP and LL(1) Techniques

# <move>		::= <castle> | <pawn_move> | <piece_move>
# <castle>		::= "O-O" | "O-O-O"
# <piece_move> 	::= <piece> <disambig> <capture> <square> <check>
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

from token import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor_pos = 0 # pointer

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
        raise SyntaxError(f"Expected {token_type}, got {current_token.type}")

    def parseMove(self):
        current_token = self.lookAhead()

        if current_token.type in ["CASTLE_KINGSIDE", "CASTLE_QUEENSIDE"]:
            return self.parseCastle()
        if current_token.type == "PIECE":
            return self.parsePieceMove()

    def parseCastle(self):
        current_token = self.lookAhead()
        if current_token.content == "O-O":
            self.match("CASTLE_KINGSIDE") # move cursor up 
            return {"type": "castle", "side": "king"} 
        elif current_token.content == "O-O-O":
            self.match("CASTLE_QUEENSIDE")
            return {"type": "castle", "side": "queen"}
        raise SyntaxError(f"Expected CASTLE_KINGSIDE or CASTLE_QUEENSIDE, goit {current_token.type}")
    
    def parsePieceMove(self):
        current_token = self.match("PIECE")

        next = self.lookAhead()
        # checking for disambig
        if next.type in ["FILE", "RANK"]:
            pass

        