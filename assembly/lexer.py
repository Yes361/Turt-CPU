from .symbols import Symbol
from .exceptions import LexerError
from dataclasses import dataclass, field
from typing import List
import re

@dataclass
class Rule:
    regex: any
    type: any
    valueExtractor: callable = None

@dataclass
class Token:
    type: any = Symbol.EMPTY
    value: any = None
    line: int = 0
    col: int = 0
    start: int = 0
    end: int = 0
    length: int = 0

@dataclass
class Lexer:
    rules: any
    text: str = None
    index: int = 0
    _current_token: any = field(default_factory=lambda: Token())
    
    def error(self, text: str, index: int, msg: str) -> None:
        raise LexerError(msg)
    
    def extract_col(self, text: str, index: int) -> tuple:
        lines = 0
        Match = None
        for Match in re.finditer(r'\r?\n', text[:index]):
            lines += 1
        last_new_line = Match.span()[0] if Match else 0
            
        return last_new_line, lines

    def extract_token(self, text: str, index: int) -> tuple:
        if not text:
            return Token(Symbol.EOF), 0
        
        last_new_line, lines = self.extract_col(text, index)
        
        for query in self.rules:
            if value := query.regex.match(text[index:]):
                token_value = value.group()
                token_length = len(token_value)
                
                if not query.type:
                    return self.extract_token(text, index + token_length)
                if query.valueExtractor:
                    token_value = query.valueExtractor(token_value)
                token =  Token(query.type, token_value, lines, index - last_new_line, index, index + token_length, token_length)
                return token, index + token_length
        
        if index < len(text):
            self.error(text, index, 'bruh.')
        return Token(Symbol.EOF), 0

    def tokenize(self, text: str) -> List[Token]:
        tokens = []
        index = 0
        token = Token()
        while token.type != Symbol.EOF:
            token, index = self.extract_token(text, index)
            tokens.append(token)
        return tokens

    def get_next_token(self) -> Token:
        self._current_token, self.index = self.extract_token(self.text, self.index)
        return self._current_token
    
    def get_current_token(self) -> Token:
        return self._current_token
    
    def expect_next_token(self, type: any = None, value: any = None) -> bool:
        if not self._current_token:
            return False
        return (self._current_token.value == value or value == None) and (self._current_token.type == type or type == None)
    
    def consume_token(self, *args, **kwargs) -> Token:
        # if self.index == 0:
        #     self.get_next_token()
        if self.expect_next_token(*args, **kwargs):
            token = self._current_token
            self.get_next_token()
            return token
        return None
        
    def __setattr__(self, name: str, value: any) -> None:
        self.__dict__[name] = value
        if name == 'text':
            self.reset()
        
    def reset(self) -> None:
        self.index = 0
        self._current_token = Token()

    def __iter__(self) -> any:
        self.reset()
        return self

    def __next__(self) -> Token:
        if self._current_token.type == Symbol.EOF:
            raise StopIteration
        return self.get_next_token()
    

standard_lexer_rules = [
    Rule(re.compile(r"[ \t]+"), None),
    Rule(re.compile(r"\/\/(.*?)(?=\r?\n|$)"), None),
    Rule(re.compile(r"\/\*.*\*\/", re.DOTALL), None),
    Rule(re.compile(r"\r?\n"), "line-break"),
    Rule(re.compile(r"\"[^\"\r\n]+\""), "string-literal", lambda x: x[1:-1]),
    Rule(re.compile(r"\'[^\'\r\n]+\'"), "string-literal", lambda x: x[1:-1]),
    Rule(
        re.compile(r"-?[ ]*[0-9]+\.?[0-9]*(?![a-zA-Z$_])"),
        "number-literal",
        lambda x: float(x.replace(' ', '')),
    ),
    Rule(re.compile(r"call|halt|move|movc|mov|add|sub|shr|cmp|out|in|je|jne|jmp|mvsp|ret"), "instruction"),
    Rule(re.compile(r"sp|reg|ram"), "operand"),
    Rule(re.compile(r"\["), "["),
    Rule(re.compile(r"\]"), "]"),
    Rule(re.compile(r","), ","),
    Rule(re.compile(r"\+"), "+"),
    Rule(re.compile(r"-"), "-"),
    Rule(re.compile(r"\*"), "*"),
    Rule(re.compile(r'\.'), '.'),
    Rule(re.compile(r"[a-zA-Z$_][a-zA-Z0-9$_]*"), "identifier"),
]