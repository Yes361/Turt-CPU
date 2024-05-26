from dataclasses import dataclass, field
from .symbols import Symbol


@dataclass
class ParserNode:
    type: any = None
    value: any = None
    children: list = field(default_factory=lambda: [])

    def __iter__(self):
        return iter(self.children)


@dataclass
class ParserType:
    source: any = None
    type: any = Symbol.token


class Parser:
    NULL = (None, 0, False)

    def __init__(self, lexer, rules):
        self.Lexer = lexer
        self.rules = rules["rules"]
        self.goal = rules["productionGoal"]

    @staticmethod
    def visualize_parse_tree(root, outFile=None):
        if root == None:
            return

        if outFile:
            outFile = open(outFile, "w")
        queue = [(root, 0)]
        while len(queue) > 0:
            node, depth = queue.pop()

            space = depth * " "
            if node.value:
                print(f"{space}|={node.type}: {node.value}", file=outFile)
            else:
                print(f"{space}|={node.type}", file=outFile)
            for i in range(len(node.children) - 1, -1, -1):
                queue.append((node.children[i], depth + 1))

    # def visualize_parse_tree(self, root, outFile=None):
    #     self.top_down_parse()

    def parse(self, text):
        return self.top_down_parse(self.goal, text)

    def top_down_parse(self, highest_level, text):
        self.tokens = self.Lexer.tokenize(text)
        root, _, _ = self.extract_grammar(highest_level, self.rules[highest_level])
        return root

    def extract_grammar(self, name, rules, startIndex=0):
        for rule in rules:
            node, index, ret = self.extract_rule(name, rule, startIndex)
            if ret:
                return node, index, ret
        return None, 0, False

    def find_matching_paren(self, rule, startIndex):
        parentheses = 1
        subset = []
        for part in rule[(startIndex + 1) :]:
            if part.type == Symbol.LPAREN:
                parentheses += 1
            elif part.type == Symbol.RPAREN:
                parentheses -= 1
            if parentheses == 0:
                break
            subset.append(part)
        return subset

    def greedy_match(self, current_rule, startIndex):
        offset = 0
        children = []
        while True:
            node, index, ret = self.extract_rule(
                None, current_rule, startIndex + offset
            )
            if not ret:
                return children, offset, ret
            offset += index
            children += node.children

    def extract_rule(self, name, rule, startIndex, prev_rule=[]):
        offset = 0
        idx = 0
        head = ParserNode(name)
        current_rule = prev_rule

        def next_part(idx):
            try:
                return rule[idx + 1].type
            except:
                return None

        ret = True
        dont_skip = True
        optional_flag = False
        while idx < len(rule):
            part = rule[idx]

            # TODO: Repeat has max-repeat options
            # TODO: Repeat 1+ or 0+ times
            match part.type:
                case Symbol.OPT:
                    optional_flag = True
                    idx += 1
                    continue
                case Symbol.OR:
                    if ret:
                        dont_skip = False
                        idx += 1
                        continue
                    ret = True
                    dont_skip = True
                    optional_flag = False
                case Symbol.REPEAT:
                    children, index, _ = self.greedy_match(
                        current_rule, startIndex + offset
                    )
                    offset += index
                    head.children += children
                case Symbol.LPAREN:
                    subset = self.find_matching_paren(rule, idx)
                    node, index, ret = self.extract_rule(
                        None, subset, startIndex + offset, prev_rule=current_rule
                    )
                    idx += len(current_rule := subset) + 1
                    if ret and dont_skip:
                        offset += index
                        head.children += node.children
                case Symbol.token:
                    token = self.tokens[startIndex + offset]
                    ret = token.type == part.source
                    if ret and dont_skip:
                        offset += 1
                        head.children.append(ParserNode(token.type, token.value))
                        current_rule = [part]
                case Symbol.nonterminal:
                    node, index, ret = self.extract_grammar(
                        part.source, self.rules[part.source], startIndex + offset
                    )
                    if ret and dont_skip:
                        offset += index
                        head.children.append(node)
                        current_rule = [part]

            if (
                not ret
                and not optional_flag
                and dont_skip
                and next_part(idx) not in [Symbol.OR]
            ):
                return None, 0, False
            dont_skip = True
            optional_flag = False
            idx += 1
        return head, offset, True

    def bottom_up_parse(self, tokens):
        pass


# TODO: Add Grammar Parser
standard_parser_rules = {
    "rules": {
        "statementList": [
            [
                ParserType(type=Symbol.LPAREN),
                ParserType(type=Symbol.OPT),
                ParserType("line-break"),
                ParserType("instruction", Symbol.nonterminal),
                ParserType(type=Symbol.RPAREN),
                ParserType(type=Symbol.REPEAT),
                # ParserType("statementList", Symbol.nonterminal),
            ],
            [],
        ],
        "instruction": [
            [
                # Symbol.LPAREN,
                ParserType("instruction"),
                ParserType("operand", Symbol.nonterminal),
                ParserType(","),
                ParserType("operand", Symbol.nonterminal),
                # Symbol.RPAREN,
                # Symbol.REPEAT
            ]
        ],
        "operand": [
            [ParserType("operand"), ParserType("indexOperand", Symbol.nonterminal)]
        ],
        "indexOperand": [
            [
                ParserType("["),
                ParserType(type=Symbol.LPAREN),
                ParserType("float", Symbol.nonterminal),
                ParserType(type=Symbol.RPAREN),
                ParserType("]"),
            ],
            [
                ParserType("["),
                ParserType("operand", Symbol.nonterminal),
                ParserType("]"),
            ],
            [
                ParserType("["),
                ParserType(type=Symbol.LPAREN),
                ParserType(type=Symbol.LPAREN),
                ParserType("operand", Symbol.nonterminal),
                ParserType("+"),
                ParserType(type=Symbol.RPAREN),
                ParserType(type=Symbol.OR),
                ParserType(type=Symbol.LPAREN),
                ParserType("operand", Symbol.nonterminal),
                ParserType("-"),
                ParserType(type=Symbol.RPAREN),
                ParserType(type=Symbol.RPAREN),
                ParserType(type=Symbol.REPEAT),
                ParserType("float", Symbol.nonterminal),
                ParserType("]"),
            ],
            # [
            #     ParserType("["),
            #     ParserType(type=Symbol.LPAREN),
            #     ParserType("operand", Symbol.nonterminal),
            #     ParserType("-"),
            #     ParserType(type=Symbol.RPAREN),
            #     # ParserType(type=Symbol.REPEAT),
            #     ParserType("float", Symbol.nonterminal),
            #     ParserType("]"),
            # ],
        ],
        # "random shit": [
        # ]
        "float": [[ParserType("number-literal")]],
    },
    "productionGoal": "statementList",
}