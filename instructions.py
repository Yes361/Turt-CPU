from enum import Enum, auto

class Opcode:
    BLANK = (255, 255, 255)
    MOV = (220, 252, 0)
    MOVC = (252, 188, 0)
    ADD = (64, 224, 208)
    SUB = (156, 224, 188)
    SHR = (100, 148, 236)
    CMP = (252, 124, 80)
    JMP = (220, 48, 96)
    CALL = (252, 0, 252)
    RET = (128, 0, 128)
    EXIT = (0, 252, 0)
    ERROR = (252, 0, 0)
    SP = (204, 204, 252)
    OUT = (12, 204, 204)
    IN = (252, 128, 204)
    MOVE = (204, 128, 0)
    
class Operand(Enum):
    IMM = auto()
    REG = auto()
    RAM = auto()
    SP = auto()