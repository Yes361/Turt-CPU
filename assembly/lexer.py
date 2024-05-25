from dataclasses import dataclass, field
from symbols import Symbol
import logging
import re


@dataclass
class TokenRule:
    rule: any
    type: any
    valueExtractor: callable = None


@dataclass
class Token:
    type: any = None
    value: any = None
    line: int = None
    col: int = None

@dataclass
class Lexer:
    rules: any
    text: str = None
    index: int = 0
    current_token: any = field(default_factory=lambda: Token(type=Symbol.EMPTY))
    prev_token: any = None

    def extract_token(self, text: str, index: int) -> tuple:
        try:
            for query in self.rules:
                if value := query.rule.match(text[index:]):
                    token = value.group()
                    index += len(token)
                    if query.type:
                        if query.valueExtractor:
                            token = query.valueExtractor(token)
                        return Token(query.type, token), index
                    else:
                        return self.extract_token(text, index)
        except:
            pass
        return Token(Symbol.EOF), index

    def tokenize(self, text: str) -> list:
        tokens = []
        index = 0
        token = Token()
        try:
            while token.type != Symbol.EOF:
                token, index = self.extract_token(text, index)
                tokens.append(token)

            if index < len(text):
                raise Exception('Text hasn\'t been fully parsed')
        except Exception as e:
            logging.exception(e)
        finally:
            return tokens

    def get_next_token(self) -> any:
        if not self.current_token:
            return None
        self.current_token, self.index = self.extract_token(self.text, self.index)
        if self.current_token.type == Symbol.EOF:
            self.current_token = None
            return Token(Symbol.EOF)
        return self.current_token
    
    def get_current_token(self) -> Token:
        return self.current_token
    
    def consume_token(self, type=None, value=None) -> Token:
        try:
            if self.index == 0:
                self.get_next_token()
            if self.current_token == None:
                return None
            if (self.current_token.value == value or value == None) and (self.current_token.type == type or type == None):
                token = self.current_token
                self.get_next_token()
                return token
        except Exception as e:
            print(e)
        return None
        
    def __setattr__(self, name: str, value: any) -> None:
        if name == 'current_token' and name in self.__dict__:
            self.__dict__['prev_token'] = self.__dict__[name]
        self.__dict__[name] = value
        if name == 'text':
            self.reset()
            
        
    def reset(self) -> None:
        self.index = 0
        self.current_token = Token(type=Symbol.EMPTY)
        self.get_next_token()

    def __iter__(self) -> any:
        self.reset()
        return self

    def __next__(self) -> Token:
        if token := self.current_token:
            self.get_next_token()
            return token
        raise StopIteration
    

standard_lexer_rules = [
    TokenRule(re.compile(r"[ \t]+"), None),
    TokenRule(re.compile(r"\/\/(.*?)(?=\r?\n|$)"), None),
    TokenRule(re.compile(r"\/\*.*\*\/", re.DOTALL), None),
    TokenRule(re.compile(r"\r?\n"), "line-break"),
    TokenRule(re.compile(r"\"[^\"\r\n]+\""), "string-literal", lambda x: x[1:-1]),
    TokenRule(re.compile(r"\'[^\'\r\n]+\'"), "string-literal", lambda x: x[1:-1]),
    TokenRule(
        re.compile(r"-?[ ]*[0-9]+\.?[0-9]*(?![a-zA-Z$_])"),
        "number-literal",
        lambda x: float(x.replace(' ', '')),
    ),
    TokenRule(re.compile(r"call|halt|move|movc|mov|add|sub|shr|cmp|out|in|je|jne|jmp|mvsp|ret"), "instruction"),
    TokenRule(re.compile(r"sp|reg|ram"), "operand"),
    TokenRule(re.compile(r"\["), "["),
    TokenRule(re.compile(r"\]"), "]"),
    TokenRule(re.compile(r","), ","),
    TokenRule(re.compile(r"\+"), "+"),
    TokenRule(re.compile(r"-"), "-"),
    TokenRule(re.compile(r"\*"), "*"),
    TokenRule(re.compile(r'\.'), '.'),
    TokenRule(re.compile(r"[a-zA-Z$_][a-zA-Z0-9$_]*"), "identifier"),
]