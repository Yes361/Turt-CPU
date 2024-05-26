from .lexer import TokenRule
from .parse import ParserType
from .compiler import Compiler
import re

grammarLexerRules = [
    TokenRule(re.compile(r"[ \t]+"), None),
    TokenRule(re.compile(r"/\/\/(.*?)(?=\r?\n|$)/"), None),
    TokenRule(re.compile(r"\/\*.*\*\/", re.DOTALL), None),
    TokenRule(re.compile(r"\r?\n"), "line-break"),
    TokenRule(re.compile(r":"), ":"),
    TokenRule(re.compile(r"\+"), "+"),
    TokenRule(re.compile(r"\|"), "|"),
    TokenRule(re.compile(r"[a-zA-Z$_][a-zA-Z0-9$_]*"), "identifier"),
]

parserAssemblyRules = {"rules": {
    'statementList': [
        [ParserType('identifier')]
    ]
},
'productionGoal': "statementList"
}

# lexer = Lexer(grammarLexerRules)
# parser = Parser(lexer, parserAssemblyRules)
# root = parser.top_down_parse("rule", file="asm.txt")


class GrammarCompiler(Compiler):
    pass


if __name__ == '__main__':
    c = GrammarCompiler(grammarLexerRules, parserAssemblyRules)
    c.compile(infile=r'files/grammar.txt')