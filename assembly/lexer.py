from .symbols import Symbol
from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class Rule:
    rule: any
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
    last_new_line: int = 0
    _current_token: any = field(default_factory=lambda: Token())
    
    def error(self, text: str, index: int, msg: str) -> None:
        raise Exception(msg)

    def extract_token(self, text: str, index: int, last_new_line: int = 0) -> tuple:
        if text:
            new_line = re.compile(r'\r?\n')
            if new_line.match(text[index:]):
                last_new_line = index
            lines = len(new_line.findall(text[:index])) + 1
            
            for query in self.rules:
                if value := query.rule.match(text[index:]):
                    token = value.group()
                    token_length = len(token)
                    
                    if not query.type:
                        return self.extract_token(text, index + token_length, last_new_line)
                    if query.valueExtractor:
                        token = query.valueExtractor(token)
                    return Token(query.type, token, lines, col=index - last_new_line, start=index, end=index + token_length, length=token_length), index + token_length, last_new_line
        
        if index < len(text):
            self.error(text, index, 'bruh.')
        return Token(Symbol.EOF), index, last_new_line

    def tokenize(self, text: str) -> any:
        tokens = []
        index = 0
        token = Token()
        last_new_line = 0
        while token.type != Symbol.EOF:
            token, index, last_new_line = self.extract_token(text, index, last_new_line)
            tokens.append(token)
        return tokens

    def get_next_token(self) -> Token:
        self._current_token, self.index, self.last_new_line = self.extract_token(self.text, self.index, self.last_new_line)
        return self._current_token
    
    def get_current_token(self) -> Token:
        return self._current_token
    
    def expect_next_token(self, type: any = None, value: any = None):
        if not self._current_token:
            return False
        return (self._current_token.value == value or value == None) and (self._current_token.type == type or type == None)
    
    def consume_token(self, *args, **kwargs) -> Token:
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
        self.last_new_line = 0
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