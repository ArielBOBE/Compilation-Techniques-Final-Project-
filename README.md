# **Chess Notation Compiler**

A compiler which translates Standard Algebraic Notation (SAN) chess moves into natural language. Made as a final project for Compilation Techniques course, demonstrating lexical analysis, syntax parsing, AST generation, and code generation.

## **Features**

- **Complete Compilation Pipeline**: Lexer → Parser → AST → Code Generator
- **Interactive GUI**: 
  - Single Move Compiler with complete compilation details
  - PGN Game Compiler for batch processing with White/Black output
- **Comprehensive Move Support**: Piece moves, pawn moves, castling, captures, promotions, checks, checkmates, and disambiguation

## **Installation & Usage**

### Prerequisites
- Python 3.14 or higher
- tkinter

### Running the Application

```bash
python main.py
```

### Using the GUI

**Single Move Compiler Page:**
1. Enter a chess move in Standard Algebraic Notation like `Nf3`, `exd5`, `O-O`or `e8=Q+`.
2. Click "Compile" to process the move
3. Toggle between Simple/Verbose output modes
4. Expand "Compilation Details" to view all 4 stages:
   - Stage 1: Tokens (lexical analysis)
   - Stage 2: Parse Tree
   - Stage 3: Abstract Syntax Tree (AST)
   - Stage 4: Output

**PGN Game Compiler Page:**
1. Click "Browse" to select a PGN text file
2. View moves in a two-column format (White | Black)
3. Toggle Simple/Verbose mode to adjust output detail

### Example Inputs

- `Nf3` - Knight moves to f3
- `Qxe5+` - Queen captures on e5, check
- `exd5` - e-pawn captures on d5
- `O-O` - Kingside castling
- `e8=Q#` - Pawn promotes to Queen on e8, checkmate
- `Nbd7` - Knight from b-file moves to d7 (disambiguation)

## **Grammar Specification**

Grammar is as follows:
```
<move>          ::= <castle> | <pawn_move> | <piece_move>
<castle>        ::= ("O-O" | "O-O-O") <check>
<piece_move>    ::= <piece> <disambig> <capture> <square> <check>
<pawn_move>     ::= <square> <promotion> <check>
                  | <file> <capture> <square> <promotion> <check>
<disambig>      ::= <file> | <rank> | <square> | ε
<capture>       ::= "x" | ε
<promotion>     ::= "=" <piece> | ε
<check>         ::= "+" | "#" | ε
<square>        ::= <file> <rank>
<file>          ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h"
<rank>          ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
<piece>         ::= "N" | "B" | "R" | "Q" | "K"
```

Example:

1. "Qxe5+" → Queen takes at e5 and results in a check
2. "b7#" → Pawn moves to b7 and results in a checkmate
3. "Nf3" → Knight moves to f3

---
## Lexical Analyzer

Lexeme → TOKEN Pairing:
1.   Pieces :
>    K, Q, R, B, N → PIECE
2.   File Letter :
> a, b, c, d, e, f, g, h → FILE, used in `<square>` and `<disamb>`
3.   Rank Digits :
> 1, 2, 3, 4, 5, 6, 7, 8 → RANK, used in `<square>` and `<disamb>`
4.   Capture :
> `x` → CAPTURE
5.   Check :
> 1.   `+` → CHECK
> 2.   `#` → CHECKMATE
6.   Promotion:
> `=` → PROMOTION_SYMBOL
7.   Castling:
> 1.   `O-O`   → CASTLE_KINGSIDE
> 2.   `O-O-O` → CASTLE_QUEENSIDE
8. End of File
> `EOF`

---

## **Project Structure**

```
├── main.py              # GUI application
├── lexer.py             # Lexical analyzer (tokenization)
├── parser.py            # Recursive descent parser
├── ast_nodes.py         # AST node class definition and hierarchy
├── code_gen.py          # Code generator (AST to natural language)
├── token.py             # Token class definition
├── test_files/          # Sample PGN files for testing
│   ├── pgn_test1.txt
│   ├── pgn_test2.txt
│   └── pgn_test3.txt
└── README.md
```

## **Architecture**

The compiler follows a traditional multi-stage compiler pipeline:

1. **Lexical Analysis** (`lexer.py`): Converts input string into tokens
2. **Syntax Analysis & AST Generation** (`parser.py`): Builds abstract syntax tree using recursive descent parsing with LL(1) grammar
3. **Code Generation** (`code_gen.py`): Translates AST into natural language output

### AST Node Hierarchy
```
ChessASTNode (base)
└── MoveNode (abstract)
    ├── CastleNode
    ├── PieceMoveNode
    └── PawnMoveNode
```

## **Testing**

Sample PGN files are provided in `test_files/` directory for batch testing the compiler with full games.