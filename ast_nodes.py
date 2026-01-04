# AST Node Classes for Chess Notation Parser

class ChessASTNode:
    """Parent Node Class for all Chess AST nodes"""
    def __repr__(self):
        # build list of "attribute=value" strings for all instance variables
        attribute_list = [f"{name}={value!r}" for name, value in self.__dict__.items()]
        
        # join with commas
        attributes_str = ', '.join(attribute_list)
        
        # return as: ClassName(attr1=val1, attr2=val2, ...)
        class_name = self.__class__.__name__
        return f"{class_name}({attributes_str})"


class MoveNode(ChessASTNode):
    """Parent Node class for all move types"""
    pass


class CastleNode(MoveNode):
    """Represents a castling move"""
    def __init__(self, side, check=False, checkmate=False):
        self.side = side  # "king" or "queen"
        self.check = check
        self.checkmate = checkmate


class PieceMoveNode(MoveNode):
    """Represents a piece move (Knight, Bishop, Rook, Queen, King)"""
    def __init__(self, piece, square, disambig=None, capture=False, check=False, checkmate=False):
        self.piece = piece
        self.square = square
        self.disambig = disambig
        self.capture = capture
        self.check = check
        self.checkmate = checkmate


class PawnMoveNode(MoveNode):
    """Represents a pawn move"""
    def __init__(self, square, file=None, capture=False, promotion=None, check=False, checkmate=False):
        self.square = square
        self.file = file  # pawn captures (e.g., exd5)
        self.capture = capture
        self.promotion = promotion
        self.check = check
        self.checkmate = checkmate
