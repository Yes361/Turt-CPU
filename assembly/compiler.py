from parse import Parser, standard_parser_rules
from lexer import Lexer, standard_lexer_rules
import logging

class Compiler:
    def __init__(self, lexer_rules=None, parser_rules=None):
        self.Lexer = Lexer(lexer_rules)
        self.Parser = Parser(self.Lexer, parser_rules)
    
    def error(self, error_msg):
        logging.exception(error_msg)
    
    def return_raw_tokens(self, text):
        return self.Lexer.tokenize(text)
    
    def process_parse(self, root, raw_tokens, text):
        Parser.visualize_parse_tree(root)

    def compile(self, text=None, infile=None):
        if infile:
            text = open(infile, "r").read()

        root = self.Parser.parse(text)
        self.process_parse(root, self.return_raw_tokens(text), text)

    def parse(self, raw_tokens, text, outfile):
        print(raw_tokens)
    
    def compile_without_parse(self, text=None, infile=None, outfile=None):
        if infile:
            text = open(infile, "r").read()

        self.parse(self.return_raw_tokens(text), text=text, outfile=outfile)


if __name__ == "__main__":
    compiler = Compiler(standard_lexer_rules, standard_parser_rules)
    # compiler.Lexer.tokenize()
    dir = r'C:\Users\NAZRU\CS projects\Turtle CTF\files\functions.txt'
    compiler.compile_without_parse(infile=dir)