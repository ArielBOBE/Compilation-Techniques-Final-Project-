# Code Generator - Translates AST Nodes to Natural Language (English Sentences)
from ast_nodes import CastleNode, PieceMoveNode, PawnMoveNode

class CodeGen:
    def __init__(self, ast_node):
        self.ast_node = ast_node
        
        # piece names mapping
        self.piece_names = {
            'N': 'Knight',
            'B': 'Bishop',
            'R': 'Rook',
            'Q': 'Queen',
            'K': 'King'
        }
    
    def showAST(self):
        """Shows  AST in a readable format"""
        lines = []
        lines.append("Fields:")
        
        if isinstance(self.ast_node, CastleNode):
            lines.append(f"  side = {self.ast_node.side}")
            lines.append(f"  check = {self.ast_node.check}")
            lines.append(f"  checkmate = {self.ast_node.checkmate}")
        
        elif isinstance(self.ast_node, PieceMoveNode):
            piece_name = self.piece_names.get(self.ast_node.piece, self.ast_node.piece)
            lines.append(f"  piece = {piece_name} (translated from {self.ast_node.piece})")
            lines.append(f"  square = {self.ast_node.square}")
            lines.append(f"  disambig = {self.ast_node.disambig}")
            lines.append(f"  capture = {self.ast_node.capture}")
            lines.append(f"  check = {self.ast_node.check}")
            lines.append(f"  checkmate = {self.ast_node.checkmate}")
        
        elif isinstance(self.ast_node, PawnMoveNode):
            lines.append(f"  square = {self.ast_node.square}")
            lines.append(f"  file = {self.ast_node.file}")
            lines.append(f"  capture = {self.ast_node.capture}")
            if self.ast_node.promotion:
                piece_name = self.piece_names.get(self.ast_node.promotion, self.ast_node.promotion)
                lines.append(f"  promotion = {piece_name} (translated from {self.ast_node.promotion})")
            else:
                lines.append(f"  promotion = {self.ast_node.promotion}")
            lines.append(f"  check = {self.ast_node.check}")
            lines.append(f"  checkmate = {self.ast_node.checkmate}")
        
        return '\n'.join(lines)
    
    def generateVerbose(self):
        """Generate detailed English description"""
        if isinstance(self.ast_node, CastleNode):
            return self.generateCastleVerbose(self.ast_node)
        elif isinstance(self.ast_node, PieceMoveNode):
            return self.generatePieceMoveVerbose(self.ast_node)
        elif isinstance(self.ast_node, PawnMoveNode):
            return self.generatePawnMoveVerbose(self.ast_node)
        else:
            raise ValueError(f"Invalid AST node type: {type(self.ast_node)}")
    
    def generateSimple(self):
        """Generate simple English sentence"""
        if isinstance(self.ast_node, CastleNode):
            return self.generateCastleSimple(self.ast_node)
        elif isinstance(self.ast_node, PieceMoveNode):
            return self.generatePieceMoveSimple(self.ast_node)
        elif isinstance(self.ast_node, PawnMoveNode):
            return self.generatePawnMoveSimple(self.ast_node)
        else:
            raise ValueError(f"Invalid AST node type: {type(self.ast_node)}")
    
    def generateCastleVerbose(self, node):
        """Generates detailed description for castling"""
        parts = []
        
        if node.side == "king":
            parts.append("king castles on kingside")
        elif node.side == "queen":
            parts.append("king castles on queenside")
        
        if node.checkmate:
            parts.append("resulting in checkmate")
        elif node.check:
            parts.append("resulting in check")
        
        return ', '.join(parts)
    
    def generatePieceMoveVerbose(self, node):
        """Generate detailed description for piece moves"""
        parts = []
        
        piece_name = self.piece_names.get(node.piece, node.piece).lower()
        parts.append(f"{piece_name} moves to {node.square}")
        
        if node.disambig:
            parts.append(f"from {self.formatSquare(node.disambig)}")
        
        if node.capture:
            parts.append("captures")
        
        if node.checkmate:
            parts.append("resulting in checkmate")
        elif node.check:
            parts.append("resulting in check")
        
        return ', '.join(parts)
    
    def generatePawnMoveVerbose(self, node):
        """Generate detailed description for pawn moves"""
        parts = []
        
        parts.append(f"pawn moves to {node.square}")
        
        if node.file:
            parts.append(f"from {node.file}-file")
        
        if node.capture:
            parts.append("captures")
        
        if node.promotion:
            piece_name = self.piece_names.get(node.promotion, node.promotion).lower()
            parts.append(f"promotes to {piece_name}")
        
        if node.checkmate:
            parts.append("resulting in checkmate")
        elif node.check:
            parts.append("resulting in check")
        
        return ', '.join(parts)
    
    def generateCastleSimple(self, node):
        """Generate simple English for castling moves"""
        if node.side == "king":
            sentence = "Castle kingside"
        elif node.side == "queen":
            sentence = "Castle queenside"
        else:
            sentence = "Castle"
        
        # check/checkmate suffix
        sentence = self.addCheckSuffix(sentence, node.check, node.checkmate)
        return sentence
    
    def generatePieceMoveSimple(self, node):
        """Generate simple English for piece moves"""
        # starting with piece name
        piece_name = self.piece_names.get(node.piece, node.piece)
        sentence = piece_name
        
        # add disambig if available
        if node.disambig:
            sentence += f" from {self.formatSquare(node.disambig)}"
        
        # add "capture" or "moves to"
        if node.capture:
            sentence += f" captures on {self.formatSquare(node.square)}"
        else:
            sentence += f" to {self.formatSquare(node.square)}"
        
        # add check/checkmate suffix
        sentence = self.addCheckSuffix(sentence, node.check, node.checkmate)
        return sentence
    
    def generatePawnMoveSimple(self, node):
        """Generate simple English for pawn moves"""
        sentence = "Pawn"
        
        # add file for captures
        if node.file:
            sentence += f" on {node.file}-file"
        
        # add "captures" or "moves to"
        if node.capture:
            sentence += f" captures on {self.formatSquare(node.square)}"
        else:
            sentence += f" to {self.formatSquare(node.square)}"
        
        # add promotion
        if node.promotion:
            promotion_piece = self.piece_names.get(node.promotion, node.promotion)
            sentence += f" and promotes to {promotion_piece}"
        
        # add check/checkmate suffix
        sentence = self.addCheckSuffix(sentence, node.check, node.checkmate)
        return sentence
    
    def formatSquare(self, square):
        """Formats square notation"""
        if not square:
            return ""
        
        # handling just file/rank (disambig)
        if len(square) == 1:
            if square in 'abcdefgh':
                return f"{square}-file"
            else:
                return f"rank {square}"
        
        # full square notation
        return square
    
    def addCheckSuffix(self, sentence, check, checkmate):
        """Add check or checkmate suffix to sentence"""
        if checkmate:
            return sentence + ", checkmate"
        elif check:
            return sentence + ", check"
        else:
            return sentence
