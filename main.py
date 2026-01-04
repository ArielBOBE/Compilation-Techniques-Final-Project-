import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from lexer import Lexer
from parser import Parser
from code_gen import CodeGen
import re

class ChessCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Notation Compiler")
        self.root.geometry("900x700")
        
        # tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.single_mode_frame = ttk.Frame(self.notebook)
        self.pgn_mode_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.single_mode_frame, text="Single Move Compiler")
        self.notebook.add(self.pgn_mode_frame, text="PGN Game Compiler")
        
        # setup both modes
        self.setup_single_mode()
        self.setup_pgn_mode()
    
    def setup_single_mode(self):
        """Setup for single move compilation page"""
        # input
        input_frame = ttk.LabelFrame(self.single_mode_frame, text="Input", padding=10)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(input_frame, text="Chess Notation (SAN):").pack(anchor='w')
        self.single_input = ttk.Entry(input_frame, font=('Courier', 12))
        self.single_input.pack(fill='x', pady=5)
        self.single_input.insert(0, "")
        
        ttk.Button(input_frame, text="Compile", command=self.compile_single).pack(pady=5)
        
        # output
        output_header_frame = ttk.Frame(self.single_mode_frame)
        output_header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        ttk.Label(output_header_frame, text="Output", font=('TkDefaultFont', 10, 'bold')).pack(side='left', padx=5)
        
        self.single_output_mode = tk.StringVar(value="simple")
        ttk.Radiobutton(output_header_frame, text="Simple", variable=self.single_output_mode, 
                       value="simple", command=self.update_single_output).pack(side='left', padx=5)
        ttk.Radiobutton(output_header_frame, text="Verbose", variable=self.single_output_mode, 
                       value="verbose", command=self.update_single_output).pack(side='left', padx=5)
        
        output_frame = ttk.Frame(self.single_mode_frame, relief='solid', borderwidth=1)
        output_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.single_output_text = scrolledtext.ScrolledText(output_frame, font=('Courier', 11), 
                                                            wrap='word', height=3, state='disabled')
        self.single_output_text.pack(fill='x', padx=5, pady=5)
        
        # details section
        details_header_frame = ttk.Frame(self.single_mode_frame)
        details_header_frame.pack(fill='x', padx=10, pady=(10, 0))
        
        self.details_expanded = tk.BooleanVar(value=False)
        self.details_toggle_btn = ttk.Button(details_header_frame, text="▶ Details", 
                                            command=self.toggle_details)
        self.details_toggle_btn.pack(side='left', padx=5)
        
        self.details_frame = ttk.Frame(self.single_mode_frame)
        
        self.details_output = scrolledtext.ScrolledText(self.details_frame, font=('Courier', 9), 
                                                       wrap='word', height=20, state='disabled')
        self.details_output.pack(fill='both', expand=True, padx=5, pady=5)
        
        # store compiled data
        self.current_ast = None
    
    def toggle_details(self):
        """toggle the details section visibility"""
        if self.details_expanded.get():
            # collapse
            self.details_frame.pack_forget()
            self.details_toggle_btn.config(text="▶ Details")
            self.details_expanded.set(False)
            self.root.geometry("900x400")
        else:
            # expand
            self.details_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
            self.details_toggle_btn.config(text="▼ Details")
            self.details_expanded.set(True)
            self.root.geometry("900x700")
    
    def update_single_output(self):
        """update the output display based on mode toggle"""
        if not self.current_ast:
            return
        
        mode = self.single_output_mode.get()
        codegen = CodeGen(self.current_ast)
        
        if mode == "simple":
            output = codegen.generateSimple()
        else:
            output = codegen.generateVerbose()
        
        self.single_output_text.config(state='normal')
        self.single_output_text.delete('1.0', tk.END)
        self.single_output_text.insert('1.0', output)
        self.single_output_text.config(state='disabled')
    
    def setup_pgn_mode(self):
        """Setup the PGN file compilation mode"""
        # file select
        file_frame = ttk.LabelFrame(self.pgn_mode_frame, text="File Input", padding=10)
        file_frame.pack(fill='x', padx=10, pady=10)
        
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side='left', padx=5)
        
        ttk.Button(file_frame, text="Browse", command=self.browse_pgn).pack(side='left', padx=5)
        ttk.Button(file_frame, text="Process", command=self.compile_pgn).pack(side='left', padx=5)
        
        # output mode
        self.output_mode = tk.StringVar(value="simple")
        mode_frame = ttk.Frame(file_frame)
        mode_frame.pack(side='left', padx=20)
        ttk.Radiobutton(mode_frame, text="Simple", variable=self.output_mode, 
                       value="simple", command=self.refresh_pgn_output).pack(side='left', padx=5)
        ttk.Radiobutton(mode_frame, text="Verbose", variable=self.output_mode, 
                       value="verbose", command=self.refresh_pgn_output).pack(side='left', padx=5)
        
        # output section
        output_frame = ttk.LabelFrame(self.pgn_mode_frame, text="Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.pgn_output = scrolledtext.ScrolledText(output_frame, font=('Courier', 10), wrap='none')
        self.pgn_output.pack(fill='both', expand=True)
        
        self.pgn_file = None
        self.pgn_moves = []
    
    def compile_single(self):
        """compile a single chess move"""
        notation = self.single_input.get().strip()
        self.single_output_text.config(state='normal')
        self.details_output.config(state='normal')
        self.single_output_text.delete('1.0', tk.END)
        self.details_output.delete('1.0', tk.END)
        
        if not notation:
            self.single_output_text.insert('1.0', "enter a chess notation")
            self.single_output_text.config(state='disabled')
            self.details_output.config(state='disabled')
            return
        
        try:
            # compile through all stages
            lexer = Lexer(notation)
            tokens = lexer.tokenize()
            
            parser = Parser(tokens)
            ast_node = parser.parse()
            
            # store for toggle
            self.current_ast = ast_node
            
            # show output
            self.update_single_output()
            
            # populate details
            details = []
            details.append("=" * 70)
            details.append(f"Input: {notation}")
            details.append("=" * 70)
            
            # lexer
            details.append("\nStage 1: Lexical Analysis")
            details.append("-" * 70)
            details.append(f"Tokens: {tokens}")
            
            # parser
            details.append("\nStage 2: RDP Parsing")
            details.append("-" * 70)
            details.append(f"AST: {ast_node}")
            
            # ast fields
            details.append("\nStage 3: Semantic Analysis")
            details.append("-" * 70)
            codegen = CodeGen(ast_node)
            details.append(codegen.showAST())
            
            # output
            details.append("\nStage 4: Output")
            details.append("-" * 70)
            details.append("  Simple:")
            simple = codegen.generateSimple()
            details.append(f"    {simple}")
            details.append("")
            details.append("  Verbose:")
            verbose = codegen.generateVerbose()
            details.append(f"    {verbose}")
            
            details.append("\n" + "=" * 70)
            
            self.details_output.insert('1.0', '\n'.join(details))
            self.details_output.config(state='disabled')
            
        except Exception as e:
            self.single_output_text.insert('1.0', f"Error: {str(e)}")
            self.single_output_text.config(state='disabled')
            self.details_output.config(state='disabled')
            self.current_ast = None
    
    def browse_pgn(self):
        """Browse for a text file"""
        filename = filedialog.askopenfilename(
            title="Select Move File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if filename:
            self.pgn_file = filename
            import os
            self.file_label.config(text=f"{os.path.basename(filename)}")
    
    def parse_pgn_file(self, filename):
        """Parse PGN file and extract moves"""
        with open(filename, 'r') as f:
            content = f.read()
        
        # remove move numbers and game result
        content = re.sub(r'\d+\.+', '', content)
        content = re.sub(r'\s+(1-0|0-1|1/2-1/2)\s*$', '', content)
        
        # split into moves
        moves = content.split()
        moves = [move.strip() for move in moves if move.strip()]
        
        return moves
    
    def compile_pgn(self):
        """Compile entire PGN file"""
        if not self.pgn_file:
            self.pgn_output.config(state='normal')
            self.pgn_output.delete('1.0', tk.END)
            self.pgn_output.insert('1.0', "Select a file first")
            self.pgn_output.config(state='disabled')
            return
        
        try:
            self.pgn_moves = self.parse_pgn_file(self.pgn_file)
            self.refresh_pgn_output()
        except Exception as e:
            self.pgn_output.config(state='normal')
            self.pgn_output.delete('1.0', tk.END)
            self.pgn_output.insert('1.0', f"Error: {str(e)}")
            self.pgn_output.config(state='disabled')
    
    def refresh_pgn_output(self):
        """Refresh PGN output based on selected mode"""
        if not self.pgn_moves:
            return
        
        self.pgn_output.config(state='normal')
        self.pgn_output.delete('1.0', tk.END)
        mode = self.output_mode.get()
        
        # adjust column width based on mode
        white_col_width = 70 if mode == "verbose" else 50
        separator_pos = 80 if mode == "verbose" else 60
        
        output = []
        output.append(f"Total moves: {len(self.pgn_moves)}")
        output.append(f"Output mode: {mode}")
        output.append("")
        
        # column headers
        output.append(f"{'Move':<6} {'White':<{white_col_width}} | {'Black'}")
        output.append("-" * (separator_pos + 50))
        
        move_number = 1
        white_move = ""
        
        for i, move_notation in enumerate(self.pgn_moves):
            try:
                # compile move
                lexer = Lexer(move_notation)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast_node = parser.parse()
                codegen = CodeGen(ast_node)
                
                # get output based on mode
                if mode == "simple":
                    translation = codegen.generateSimple()
                else:
                    translation = codegen.generateVerbose()
                
                # format notation with translation
                move_text = f"{move_notation} - {translation}"
                
                if i % 2 == 0:
                    # white's move, store it
                    white_move = move_text
                else:
                    # black's move, print both
                    output.append(f"{move_number:<6} {white_move:<{white_col_width}} | {move_text}")
                    move_number += 1
                    white_move = ""
                    
            except Exception as e:
                move_text = f"{move_notation} - Error: {str(e)}"
                
                if i % 2 == 0:
                    white_move = move_text
                else:
                    output.append(f"{move_number:<6} {white_move:<{white_col_width}} | {move_text}")
                    move_number += 1
                    white_move = ""
        
        # if game ends on white's move
        if white_move:
            output.append(f"{move_number:<6} {white_move}")
        
        self.pgn_output.insert('1.0', '\n'.join(output))
        self.pgn_output.config(state='disabled')

def main():
    root = tk.Tk()
    app = ChessCompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
