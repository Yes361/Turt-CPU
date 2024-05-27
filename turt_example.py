from assembly import Compiler, standard_lexer_rules, standard_parser_rules
from dataclasses import dataclass, field
from instructions import Opcode, Operand
from PIL import Image
import argparse


@dataclass
class turtleOperand:
    operand: any = None
    index: tuple = (255, 255, 255)
    flags: tuple = (False, False, False)

    @staticmethod
    def imm_convert_to_rgb(imm) -> tuple:
        imm = int(imm)
        if imm < 0:
            imm += 256**3
        return (imm & 0x0000FF, (imm & 0x00FF00) >> 8, (imm & 0xFF0000) >> 16)

    @staticmethod
    def convert_one_byte(imm) -> int:
        if imm < 0:
            imm += 256
        return int(imm)

    @staticmethod
    def convert_to_reg(val) -> tuple:
        r = int(val * 40 + 20)
        return (r, r, r)

    @staticmethod
    def convert_reg_int(val) -> int:
        return int(val * 40 + 20)

    @staticmethod
    def convert_index_tuple(indexA, indexB, imm) -> tuple:
        r = turtleOperand.convert_reg_int(indexA) if indexA != None else 0
        g = turtleOperand.convert_reg_int(indexB) if indexB != None else 0
        b = turtleOperand.convert_one_byte(imm) if imm != None else 0
        return (r, g, b)


@dataclass
class turtleInstruction:
    pos: tuple = (0, 0)
    rgb: tuple = (0, 0, 0)
    opcode: tuple = (0, 0, 0)
    operandA: turtleOperand = field(default_factory=lambda: turtleOperand())
    operandB: turtleOperand = field(default_factory=lambda: turtleOperand())


class TurtleCompiler(Compiler):

    def parse(self, raw_tokens, text, outfile=None):
        self.x, self.y = 0, 0
        self.labels = {}
        self.instructions = []
        self.Lexer.text = text
        self.Lexer.get_next_token()
        while True:

            if self.consume_directive():
                pass
            elif inst := self.consume_instruction():
                self.instructions.append(inst)

            if not self.Lexer.consume_token(value="\n"):
                break

        self.convert_to_img(outfile)

    def convert_to_img(self, outfile=None):
        # TODO: this is a hotfix
        if len(self.instructions) == 0:
            return
        
        image = Image.new("RGB", (51, 102), "white")

        for inst in self.instructions:
            x, y = inst.pos
            image.putpixel((x * 3, y - 1), inst.rgb)
            image.putpixel((x * 3 + 1, y - 1), inst.operandA.index)
            image.putpixel((x * 3 + 2, y - 1), inst.operandB.index)

        if outfile:
            image.save(outfile)

    def consume_directive(self):
        if self.Lexer.consume_token(value=".") and (
            token := self.Lexer.consume_token(type="identifier")
        ):
            if pos := self.consume_loc():
                self.x, self.y = pos
                self.labels[token.value] = pos
            else:
                self.labels[token.value] = (self.x, self.y)
        return False

    def consume_instruction(self):
        operandA = turtleOperand()
        operandB = turtleOperand()
        opcode = None
        rgb = (255, 255, 255)

        instructions = [
            "out",
            "in",
            "move",
            "mov",
            "halt",
            "sub",
            "jmp",
            "jne",
            "add",
            "movc",
            "cmp",
            "shr",
            "call",
            "je",
            "jge",
            "jle",
            "ret",
            "mvsp",
        ]
        current_token = self.Lexer.get_current_token()
        if not current_token or current_token.value not in instructions:
            return None

        self.Lexer.get_next_token()

        match current_token.value:
            case "out":
                operandA = self.consume_operand()
                flagA = operandA.flags
                opcode = Opcode.OUT
                rgb = (
                    opcode[0] | flagA[0],
                    opcode[1] | flagA[1],
                    opcode[2] | flagA[2],
                )
                self.y += 1
            case "je" | "jge" | "jle" | "jmp" | "jne":
                opcode = Opcode.JMP
                rgb, operandA = self.consume_jmp(current_token.value)
            case "mvsp":
                imm = self.consume_imm()
                opcode = Opcode.SP
                rgb = opcode
                self.y += 1
                operandA = turtleOperand(
                    Operand.IMM, index=turtleOperand.imm_convert_to_rgb(imm)
                )
            case "shr":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.SHR
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "move":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.MOVE
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "call":
                x, y = self.consume_loc()
                opcode = Opcode.CALL
                rgb = opcode
                operandA = turtleOperand(Operand.IMM, index=(int(x), int(y), 0))
                self.y += 1
            case "ret":
                opcode = Opcode.RET
                rgb = opcode
                imm = self.consume_imm()
                operandA = turtleOperand(
                    Operand.IMM, index=turtleOperand.imm_convert_to_rgb(imm)
                )
                self.y += 1
            case "in":
                operandA = self.consume_operand()
                flagA = operandA.flags
                opcode = Opcode.IN
                rgb = (
                    opcode[0] | flagA[0],
                    opcode[1] | flagA[1],
                    opcode[2] | flagA[2],
                )
                self.y += 1
            case "mov":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.MOV
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "halt":
                self.y += 1
                opcode = Opcode.EXIT
                rgb = Opcode.EXIT
            case "sub":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.SUB
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "add":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.ADD
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "movc":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.MOVC
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1
            case "cmp":
                operandA = self.consume_operand()
                flagA = operandA.flags
                self.Lexer.consume_token(value=",")
                operandB = self.consume_operand()
                flagB = operandB.flags

                opcode = Opcode.CMP
                rgb = (
                    opcode[0] | flagA[0] | flagB[0] << 1,
                    opcode[1] | flagA[1] | flagB[1] << 1,
                    opcode[2] | flagA[2] | flagB[2] << 1,
                )
                self.y += 1

        return turtleInstruction(
            pos=(self.x, self.y),
            rgb=rgb,
            opcode=opcode,
            operandA=operandA,
            operandB=operandB,
        )

    def consume_jmp(self, type):
        imm = self.consume_imm()
        if imm == None:
            if label := self.Lexer.consume_token(type="identifier"):
                destination = self.labels[label.value]
                imm = destination[1] - self.y
        opcode = Opcode.JMP
        self.y += 1
        if type == "je":
            rgb = (opcode[0] | 1, opcode[1], opcode[2])
        elif type == "jge":
            rgb = (opcode[0], opcode[1] | 2, opcode[2])
        elif type == "jle":
            rgb = (opcode[0] | 2, opcode[1], opcode[2])
        elif type == "jmp":
            rgb = (opcode[0] | 1 | 2, opcode[1] | 1 | 2, opcode[2] | 0 | 0)
        elif type == "jne":
            rgb = (opcode[0] | 0 | 0, opcode[1] | 1 | 0, opcode[2] | 0 | 0)
        operandA = turtleOperand(
            Operand.IMM, index=turtleOperand.imm_convert_to_rgb(imm)
        )
        return rgb, operandA

    def consume_loc(self):
        if self.Lexer.consume_token(value="["):
            x = self.consume_imm()
            self.Lexer.consume_token(value=",")
            y = self.consume_imm()
            self.Lexer.consume_token(value="]")
            return int(x), int(y)
        return None

    def return_operand_type(self, operand):
        if operand.value == "reg":
            return Operand.REG, (True, False, False)
        if operand.value == "ram":
            return Operand.RAM, (False, True, False)
        if operand.value == "sp":
            return Operand.SP, (True, True, False)

    def consume_operand(self):
        if operand := self.Lexer.consume_token(type="operand"):
            self.Lexer.consume_token(type="[")
            operand, flags = self.return_operand_type(operand)

            og_index = self.consume_imm()
            if og_index != None:
                if operand == Operand.REG:
                    index = turtleOperand.convert_to_reg(og_index)
                elif operand == Operand.RAM:
                    index = turtleOperand.imm_convert_to_rgb(og_index)
                elif operand == Operand.SP:
                    index = turtleOperand.imm_convert_to_rgb(og_index)
                self.Lexer.consume_token(type="]")

                operandB = self.consume_suffix()
                imm = self.consume_imm()

                if operandB or imm != None:
                    return turtleOperand(
                        operand,
                        turtleOperand.convert_index_tuple(og_index, operandB, imm),
                        flags=flags,
                    )

                return turtleOperand(operand, index, flags=(flags[0], flags[1], True))

            operandA = self.consume_simple_operand()
            operandB = self.consume_suffix()
            imm = self.consume_imm()
            self.Lexer.consume_token(type="]")
            return turtleOperand(
                operand,
                turtleOperand.convert_index_tuple(operandA, operandB, imm),
                flags=flags,
            )

        value = self.consume_imm()
        if value != None:
            return turtleOperand(
                operand=Operand.IMM,
                index=turtleOperand.imm_convert_to_rgb(value),
                flags=(False, False, True),
            )
        return None

    def consume_simple_operand(self):
        if token := self.Lexer.consume_token(type="operand"):
            self.Lexer.consume_token(type="[")
            index = self.consume_imm()
            self.Lexer.consume_token(type="]")
            return int(index)
        return None

    def consume_suffix(self):
        if self.Lexer.consume_token(value="+"):
            return self.consume_simple_operand()
        return None

    def consume_imm(self):
        self.Lexer.consume_token(value="+")
        if token := self.Lexer.consume_token(type="number-literal"):
            return token.value
        return None


def compile(infile, outfile):
    compiler = TurtleCompiler(standard_lexer_rules, standard_parser_rules)
    compiler.compile_without_parse(infile=infile, outfile=outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="kill me")
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()
    compile(args.infile, args.outfile)
