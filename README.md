# **Chess Notation Compiler**

Parses Chess Notation to Natural Language

Grammar is as follows:
```
<move>		        ::= <castle> | <pawn_move> | <piece_move>
<castle>		    ::= "O-O" | "O-O-O"
<piece_move> 	    ::= <piece> <disambig> <capture> <square> <check>
<pawn_move>	        ::= <file> <pawn_move_tail>
<pawn_move_tail>	::= <rank> <promotion> <check>
                        | <capture> <square> <promotion> <check>
<disambig>		    ::= <file> <disambig_tail> | <rank> | ε
<disambig_tail>	    ::= <rank> | ε
<capture> 		    ::= "x" | ε
<promotion> 		::= "=" <piece> | ε
<check>		        ::= "+" | "#" | ε
<square>		    ::= <file> <rank>
<file> 			    ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h"
<rank> 		        ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
<piece> 		    ::= "N" | "B" | "R" | "Q" | "K" 
```

Example:

1. "Qxe5+" → Queen takes at e5 and results in a check
2. "b7#" → Pawn moves to b7 and results in a checkmate
3. "Nf3" → Knight moves to f3

---
## Lexical Analyzer

Lexeme → TOKEN Pairing:
1.   Pieces :
> 1.   K → KING
> 2.   Q → QUEEN
> 3.   R → ROOK
> 4.   B → BISHOP
> 5.   N → KNIGHT
2.   File Letter :
> a, b, c, d, e, f, g, h → FILE, used in `<square>` and `<disamb>`
3.   Rank Digits :
> 1, 2, 3, 4, 5, 6, 7, 8 → RANK, used in `<square>` and `<disamb>`
4.   Capture :
> 1.   `x` → CAPTURE
5.   Check :
> 1.   `+` → CHECK
> 2.   `#` → CHECKMATE
6.   Promotion:
> 1.   `=` → PROMOTION_SYMBOL
7.   Castling:
> 5.   O-O   → CASTLE_KINGSIDE
> 6.   O-O-O → CASTLE_QUEENSIDE
8. End of File
> EOF

