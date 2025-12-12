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
    
    def parse(self):
        move = self.parseMove()

        current_token = self.lookAhead()
        if current_token.type != "EOF":
            self.raiseError(f"Unexpected token after move, expected EOF")

        return move
    
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
        elif current_token.type in ["SQUARE", "FILE"]:
            return self.parsePawnMove()
        else:
            self.raiseError(f"Unexpected token at start of move: {current_token.type}")

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
        next_token = self.lookAhead()

        disambig = None
        square = None

        # checking for disambig
        if next_token.type in ["FILE", "RANK"]:
            disambig = self.match(next_token.type)
            next_token = self.lookAhead()
        elif next_token.type == "SQUARE":
            # if the token is SQUARE, it could either be
            # DISAMBIG or the final SQAURE
            # checking if there's another square after capture to decide that
            temp_pos = self.cursor_pos
            first_square = self.match("SQUARE")
            next_token = self.lookAhead()

            # if there is capture after the square, meanss that this first_square is a disambig
            if next_token.type == "CAPTURE":
                disambig = first_square
                self.match("CAPTURE")
                next_token = self.lookAhead()
                
                # takes the actual destination square
                if next_token.type() == "SQUARE":
                    square = self.match("SQUARE")
                    next_token = self.lookAhead()
                else:
                    self.raiseError(f"Expected destination SQUARE after capture")
            else:
                # if no capture, then the first_square is the destination
                square = first_square

        #  chechking for capture if not already handled above
        capture = False
        # handles direct capture without anny disambig.. i.e. Nxe5
        if not square and next_token.type == "CAPTURE":
            self.match("CAPTURE")
            capture = True
            next_token = self.lookAhead()
        # handles captures that follow after a file/rank disambig.. i.e. Nfxe5 or R4xd4
        elif disambig and next_token.type == "CAPTURE":
            self.match("CAPTURE")
            capture = True
            next_token = self.lookAhead()
        else:
            # if there was a disambig and it was a square, then it's a guaranteed capture
            capture = (disambig is not None and disambig.type == "SQUARE") 
        
        # checking for square if not already matched
        if not square:
            if next_token.type == "SQUARE":
                square = self.match("SQUARE")
                next_token = self.lookAhead()
            else:
                self.raiseError(f"Expected SQUARE after piece move")
        
        # checking for check/checkmate
        check = None
        checkmate = False
        if next_token.type == "CHECK":
            self.match("CHECK")
            check = True
        elif next_token.type == "CHECKMATE":
            self.match("CHECKMATE")
            checkmate = True
        
        return {
            "type"      : "piece_move",
            "piece"     : piece.content,
            "disambig"  : disambig.content if disambig else None,
            "capture"   : capture, 
            "square"    : square.content,
            "check"     : check,
            "checkmate" : checkmate

        }
    
    def parsePawnMove(self):
        next_token = self.lookAhead()

        # takes into account pawn captures
        file = None
        capture = False

        #regular pawn move
        square = None
        promotion = None
        check = None

        # pawn capture parsing
        if next_token.type == "FILE":
            file = self.match("FILE")
            next_token = self.lookAhead()

            # if the move starts with JUST a file, its guaranteed to be a capturing move
            if next_token.type == "CAPTURE":
                self.match("CAPTURE")
                capture = True
                next_token = self.lookAhead()

        # regular pawnw movement parsing
        if next_token.type == "SQUARE":
            square = self.match("SQUARE")
            next_token = self.lookAhead()
        else:
            self.raiseError(f"Expected SQUARE in pawn move, got {next_token.type}")

        if next_token.type == "PROMOTION_SYMBOL":
            self.match("PROMOTION_SYMBOL")
            promotion = self.match("PIECE") # promotion piece
            next_token = self.lookAhead()

        # checks for checkmate or check
        check = None
        checkmate = False
        if next_token.type == "CHECK":
            self.match("CHECK")
            check = True
        elif next_token.type == "CHECKMATE":
            self.match("CHECKMATE")
            checkmate = True

        return {
            "type"      : "pawn_move",
            "file"      : file.content if file else None,
            "capture"   : capture,
            "square"    : square.content,
            "promotion" : promotion.content if promotion else None,
            "check"     : check,
            "checkmate" : checkmate
        }

