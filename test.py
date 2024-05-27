from assembly import Lexer, standard_lexer_rules

# print(Lexer(rules=standard_lexer_rules).tokenize(text='`'))


for token in Lexer(standard_lexer_rules, text='mov'):
    print(token)