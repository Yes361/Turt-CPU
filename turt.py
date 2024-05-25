import turtle
from PIL import Image
from assembly import instructions
Opcode = instructions.Opcode

def hexToRgb(hx):
    return (int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16))


# Get the canvas color at |turt|'s position.
def getColor(turt):
    x = int(turt.pos()[0])
    y = -int(turt.pos()[1])
    canvas = turtle.getcanvas()
    ids = canvas.find_overlapping(x, y, x, y)
    for index in ids[::-1]:
        color = canvas.itemcget(index, "fill")
        if color and color[0] == "#":
            return hexToRgb(color)
    return (255, 255, 255)


# Draw the image file from |path| with |turt|
def drawImg(path, turt):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    turt.pendown()
    for yy in range(h):
        for xx in range(w):
            turt.pencolor(px[xx, yy])
            turt.forward(5)
        turt.penup()
        turt.back(w * 5)
        turt.right(90)
        turt.forward(5)
        turt.left(90)
        turt.pendown()
    turt.penup()
    turt.left(90)
    turt.forward(h * 5)
    turt.right(90)
    return w, h

turtle.Screen().colormode(255)
turtle.tracer(0, 0)

pTurt = turtle.Turtle()
pTurt.pensize(5)
pTurt.penup()
pTurt.back(12 * 5)
pTurt.pendown()

mTurt = None

def loadM(flag, file='m.png'):
    global mTurt
    mTurt = turtle.Turtle()
    mTurt.speed(0)
    mTurt.pensize(5)
    mTurt.penup()
    mTurt.forward(12 * 5)
    w, h = drawImg(file, mTurt)
    mTurt.pendown()
    for i in range(len(flag)):
        mTurt.pencolor((ord(flag[i]), 0, 0))
        mTurt.forward(5)
        if (i + 1) % w == 0:
            mTurt.penup()
            mTurt.back(w * 5)
            mTurt.right(90)
            mTurt.forward(5)
            mTurt.left(90)
            mTurt.pendown()
    mTurt.penup()
    mTurt.back(10 * 5)
    mTurt.left(90)
    mTurt.forward(5)
    mTurt.right(90)

def readM(a):
    mTurt.forward((a % 25) * 5)
    mTurt.right(90)
    mTurt.forward((a // 25) * 5)
    c = getColor(mTurt)
    mTurt.right(90)
    mTurt.forward((a % 25) * 5)
    mTurt.right(90)
    mTurt.forward((a // 25) * 5)
    mTurt.right(90)
    return c


def writeM(a, c):
    mTurt.right(90)
    mTurt.forward((a // 25) * 5)
    mTurt.left(90)
    mTurt.forward((a % 25) * 5)
    mTurt.pencolor(c)
    mTurt.pendown()
    mTurt.forward(0)
    mTurt.penup()
    mTurt.left(90)
    mTurt.forward((a // 25) * 5)
    mTurt.left(90)
    mTurt.forward((a % 25) * 5)
    mTurt.left(180)


sTurt = None


def loadS():
    global sTurt
    sTurt = turtle.Turtle()
    sTurt.speed(0)
    sTurt.pensize(5)
    sTurt.penup()
    sTurt.left(90)
    sTurt.forward(50 * 5)
    sTurt.left(90)
    sTurt.forward(4 * 5)
    sTurt.left(90)
    sTurt.pencolor((255, 128, 128))
    sTurt.pendown()
    sTurt.forward(120 * 5)
    sTurt.penup()


def readS(a):
    sTurt.forward(a * 5)
    c = getColor(sTurt)
    sTurt.back(a * 5)
    return c


def writeS(a, c):
    sTurt.forward(a * 5)
    sTurt.pencolor(c)
    sTurt.pendown()
    sTurt.forward(0)
    sTurt.penup()
    sTurt.back(a * 5)


rTurt = None


def loadR():
    global rTurt
    rTurt = turtle.Turtle()
    rTurt.speed(0)
    rTurt.pensize(5)
    rTurt.penup()
    rTurt.forward(20 * 5)
    rTurt.left(90)
    rTurt.forward(40 * 5)
    rTurt.right(90)
    sTurt.pencolor((0, 0, 0))
    for i in range(3):
        for j in range(3):
            rTurt.pendown()
            rTurt.forward(0)
            rTurt.penup()
            rTurt.forward(2 * 5)
        rTurt.back(6 * 5)
        rTurt.right(90)
        rTurt.forward(2 * 5)
        rTurt.left(90)
    rTurt.left(90)
    rTurt.forward(6 * 5)
    rTurt.right(90)


def readR(n):
    rTurt.forward((n % 3) * 10)
    rTurt.right(90)
    rTurt.forward((n // 3) * 10)
    c = getColor(rTurt)
    rTurt.right(90)
    rTurt.forward((n % 3) * 10)
    rTurt.right(90)
    rTurt.forward((n // 3) * 10)
    rTurt.right(90)
    return c


def writeR(n, c):
    rTurt.forward((n % 3) * 10)
    rTurt.right(90)
    rTurt.forward((n // 3) * 10)
    rTurt.pencolor(c)
    rTurt.pendown()
    rTurt.forward(0)
    rTurt.penup()
    rTurt.right(90)
    rTurt.forward((n % 3) * 10)
    rTurt.right(90)
    rTurt.forward((n // 3) * 10)
    rTurt.right(90)


cTurt = None


def loadC(file='c.png'):
    global cTurt
    cTurt = turtle.Turtle()
    cTurt.speed(0)
    cTurt.pensize(5)
    cTurt.penup()
    cTurt.left(90)
    cTurt.forward(50 * 5)
    cTurt.right(90)
    drawImg(file, cTurt)


def getRNum(colorOrInt):
    if type(colorOrInt) == tuple:
        colorOrInt = colorOrInt[0]
    return (colorOrInt - 20) // 40


def read(op, isR, isP, isC):
    if isP:
        return readPVal(op, isR, isC)
    elif isR:
        return readRVal(getRNum(op))
    elif isC:
        return readC(op)
    raise BaseException("invalid insn")

def readPVal(op, isS, isC):
    a = readPA(op, isC)
    if isS:
        return readC(readS(a))
    else:
        return readC(readM(a))

def readPA(op, isC):
    if isC:
        return readC(op)
    a = 0
    if op[0] != 0:
        a = readRVal(getRNum(op[0]))
    if op[1] != 0:
        a += readRVal(getRNum(op[1]))
    a += readOneByteC(op[2])
    return a

def readRVal(rNum):
    return readC(readR(rNum))


def write(op, val, isR, isP, isC):
    if isP:
        writePVal(op, val, isR, isC)
    elif isR:
        writeRVal(getRNum(op), val)
    else:
        raise BaseException("invalid insn")

def writeRVal(rNum, val):
    writeR(rNum, cToColor(val))

def writePVal(op, val, isS, isC):
    a = readPA(op, isC)
    if isS:
        writeS(a, cToColor(val))
    else:
        writeM(a, cToColor(val))





def readC(op):
    c = op[0] + (op[1] << 8) + (op[2] << 16)
    if c >= (256**3) // 2:
        c = -((256**3) - c)
    return c


def readOneByteC(val):
    if val > 256 // 2:
        return -(256 - val)
    return val


def cToColor(val):
    if val < 0:
        val = 256**3 + val
    return [val % 256, (val >> 8) % 256, (val >> 16) % 256]


def getGridOperand(rgb, isC, withVal):
    if isC:
        return readC(rgb)

    GridString = ""
    immediateValue = readOneByteC(rgb[2])
    if rgb[0] != 0:
        GridString = f"reg[{getRNum(rgb[0])}]"
        if rgb[1] != 0:
            GridString += " + "
    if rgb[1] != 0:
        GridString += f"reg[{getRNum(rgb[1])}]"

    regOffset = rgb[0] != 0 or rgb[1] != 0

    if immediateValue != 0 or not regOffset:
        if regOffset:
            if immediateValue > 0:
                GridString += " + "
            else:
                GridString += " - "
        GridString += f"{abs(immediateValue)}"

    if withVal:
        GridString += f"={readPA(rgb, isC)}"
    return GridString


def operandType(isR, isP, isC, operand, isRead, withVal, outputAscii=False):
    if isP:
        imm = getGridOperand(operand, isC, False)
        addr = readPA(operand, isC)
        if isR:
            output = readC(readS(addr))
            val = f"={output}" if withVal else ""
            # ascii = chr(output) if outputAscii else ""
            return f"sp[{imm}]{val}" # {ascii}
        else:
            output = readC(readM(addr))
            val = f"={output}" if withVal else ""
            # ascii = chr(output) if outputAscii else ""
            return f"ram[{imm}]{val}" # {ascii}
    elif isR:
        index = getRNum(operand)
        output = readRVal(index)
        val = f"={output}" if withVal else ""
        # ascii = chr(output) if outputAscii else ""
        return f"reg[{index}]{val}" # {ascii}
    elif isC and isRead:
        return readC(operand)


def printALUoperands(
    opcode, operand1, operand2, isR1, isP1, isC1, isR2, isP2, isC2, withVal=False
):
    secondOperand = (
        getGridOperand(operand2, isC2, withVal)
        if opcode == (252, 188, 0)
        else operandType(isR2, isP2, isC2, operand2, True, withVal)
    )
    return f"{operandType(isR1, isP1, isC1, operand1, True, withVal)}, {secondOperand}"


def determineJump(isR1, isP1, isR2, isP2):
    if (isR1 and isP1) or (isR1 and isR2 and isP2):
        return "jmp"
    if isR1 and isR2:
        return "je or jle"
    if isR1 and isP2:
        return "je or jge"
    if isR2:
        return "jle"
    if isP2:
        return "jge"
    if isR1:
        return "je"
    if isP1:
        return "jne"


def getCoords():
    x = round((cTurt.pos()[0] - sx) / 15)
    y = round((sy - cTurt.pos()[1]) / 5)
    return f"[{x}, {y}]"


def printInstruction(opcode, operand1, operand2):
    return f"opcode: {opcode} operands: {operand1}, {operand2}"


def memoryDump(file=None, infile='c.png'):
    if file != None:
        file = open(file, "w")

    im = Image.open(infile).convert("RGB")
    w, h = im.size
    px = im.load()
    for x in range(0, w, 3):
        for y in range(h):
            color0 = px[x, y]
            color1 = px[x + 1, y]
            color2 = px[x + 2, y]

            if (
                color0 == Opcode.BLANK
                and color1 == Opcode.BLANK
                and color2 == Opcode.BLANK
            ):
                break

            cmpcolor = (color0[0] & 0xFC, color0[1] & 0xFC, color0[2] & 0xFC)
            isR1 = color0[0] & 1 != 0
            isP1 = color0[1] & 1 != 0
            isC1 = color0[2] & 1 != 0
            isR2 = color0[0] & 2 != 0
            isP2 = color0[1] & 2 != 0
            isC2 = color0[2] & 2 != 0

            print(color0, file=file)
            print(printInstruction(cmpcolor, color1, color2), file=file)
            print(isR1, isP1, isC1, isR2, isP2, isC2, file=file)
            print(f"[{x // 3}, {y}]", end=" ", file=file)

            if cmpcolor == Opcode.EXIT:
                print("correct flag!", file=file)
            elif cmpcolor == Opcode.ERROR:
                print("wrong flag :C", file=file)
            elif cmpcolor == Opcode.SP:
                index = readC(color1)
                direction = "i" if index > 0 else "d"
                print(f"sp{direction} {abs(index)}", file=file)
            elif cmpcolor == Opcode.MOVE:
                print(
                    f'MOVE {printALUoperands(cmpcolor, color1, color2, isR1, isP1, isC1, isR2, isP2, isC2)}',
                    file=file,
                )
            elif cmpcolor == Opcode.IN:
                print(f"in {operandType(isR1, isP1, isC1, color1, True, withVal=False)}", file=file)
            elif cmpcolor == Opcode.OUT:
                print(f"out {operandType(isR1, isP1, isC1, color1, True, withVal=False)}", file=file)
            # ALU (Arithmetic Logic Unit)
            elif (
                cmpcolor == Opcode.MOV
                or cmpcolor == Opcode.MOVC
                or cmpcolor == Opcode.ADD
                or cmpcolor == Opcode.SUB
                or cmpcolor == Opcode.SHR
                or cmpcolor == Opcode.CMP
            ):
                # mov
                if cmpcolor == Opcode.MOV or cmpcolor == Opcode.MOVC:
                    print("mov", end=" ", file=file)
                # add
                elif cmpcolor == Opcode.ADD:
                    print("add", end=" ", file=file)
                # sub
                elif cmpcolor == Opcode.SUB:
                    print("sub", end=" ", file=file)
                # shr
                elif cmpcolor == Opcode.SHR:
                    print("shr", end=" ", file=file)
                # cmp
                elif cmpcolor == Opcode.CMP:
                    print("cmp", end=" ", file=file)

                print(
                    printALUoperands(
                        cmpcolor, color1, color2, isR1, isP1, isC1, isR2, isP2, isC2
                    ),
                    file=file,
                )
            # jmp
            elif cmpcolor == Opcode.JMP:
                fwd = readC(color1)
                print(f"{determineJump(isR1, isP1, isR2, isP2)} {(fwd)}", file=file)
            # call
            elif cmpcolor == Opcode.CALL:
                print(f"call [{(x + color1[0]) // 3}, {y - color1[1]}]", file=file)
            elif cmpcolor == Opcode.RET:
                print(f"ret {readC(color1)}", file=file)
            else:
                raise BaseException("unknown: %s" % str(cmpcolor))

            print("", file=file)

def get_input(msg):
    while True:
        try:
            val = input(msg)
            if len(val) == 1 and not val.isdigit():
                return ord(val)
            return int(val)
        except:
            print('Invalid input.')

def run(file=None):
    if file != None:
        file = open(file, "w")

    global sx, sy
    sx, sy = cTurt.pos()

    while True:
        color0 = getColor(cTurt)
        cmpcolor = (color0[0] & 0xFC, color0[1] & 0xFC, color0[2] & 0xFC)
        cTurt.forward(5)
        color1 = getColor(cTurt)
        cTurt.forward(5)
        color2 = getColor(cTurt)
        cTurt.back(2 * 5)
        isR1 = color0[0] & 1 != 0
        isP1 = color0[1] & 1 != 0
        isC1 = color0[2] & 1 != 0
        isR2 = color0[0] & 2 != 0
        isP2 = color0[1] & 2 != 0
        isC2 = color0[2] & 2 != 0

        print(printInstruction(cmpcolor, color1, color2), file=file)
        print(isR1, isP1, isC1, isR2, isP2, isC2, file=file)
        print(getCoords(), end=" ", file=file)

        # Halt Conditions
        if cmpcolor == Opcode.EXIT:
            print("correct flag!", file=file)
            exit(0)
        elif cmpcolor == Opcode.ERROR:
            print("wrong flag :C", file=file)
            exit(0)
        # Increment Stack Pointer
        elif cmpcolor == Opcode.MOVE:
            fwd = read(color1, isR1, isP1, isC1)
            angle = read(color2, isR2, isP2, isC2)
            print(fwd, angle, pTurt.pos())
            pTurt.pendown()
            pTurt.pencolor((0, 255, 0))
            pTurt.forward(fwd * 5)
            pTurt.left(angle)
            pTurt.penup()
            print(
                f'MOVE {printALUoperands(cmpcolor, color1, color2, isR1, isP1, isC1, isR2, isP2, isC2)}',
                file=file,
            )
        elif cmpcolor == Opcode.SP:
            index = readC(color1)
            sTurt.forward(index * 5)
            direction = "increment" if index > 0 else "decrement"
            print(f"sp {direction} {abs(index)}", file=file)
        elif cmpcolor == Opcode.IN:
            val = get_input('gimme that input dawg: ')
            write(color1, val, isR1, isP1, isC1)
            print(f"in {operandType(isR1, isP1, isC1, color1, True, withVal=True)}", file=file)
        elif cmpcolor == Opcode.OUT:
            print(f"out {operandType(isR1, isP1, isC1, color1, True, withVal=True, outputAscii=True)}", file=file)
            print(f"out {operandType(isR1, isP1, isC1, color1, True, withVal=True, outputAscii=True)}")
        # ALU (Arithmetic Logic Unit)
        elif (
            cmpcolor == Opcode.MOV
            or cmpcolor == Opcode.MOVC
            or cmpcolor == Opcode.ADD
            or cmpcolor == Opcode.SUB
            or cmpcolor == Opcode.SHR
            or cmpcolor == Opcode.CMP
        ):
            
            alu_op_repr = printALUoperands(cmpcolor, color1, color2, isR1, isP1, isC1, isR2, isP2, isC2, True)            
            # Allow mov operations for offset register value
            if cmpcolor == Opcode.MOVC:
                val2 = readPA(color2, isC2)
            else:
                val2 = read(color2, isR2, isP2, isC2)

            # mov
            if cmpcolor == Opcode.MOV or cmpcolor == Opcode.MOVC:
                print("mov", end=" ", file=file)
                write(color1, val2, isR1, isP1, isC1)
            # add
            elif cmpcolor == Opcode.ADD:
                print("add", end=" ", file=file)
                val1 = read(color1, isR1, isP1, isC1)
                write(color1, val1 + val2, isR1, isP1, isC1)
            # sub
            elif cmpcolor == Opcode.SUB:
                print("sub", end=" ", file=file)
                val1 = read(color1, isR1, isP1, isC1)
                write(color1, val1 - val2, isR1, isP1, isC1)
            # shr
            elif cmpcolor == Opcode.SHR:
                print("shr", end=" ", file=file)
                val1 = read(color1, isR1, isP1, isC1)
                write(color1, val1 >> val2, isR1, isP1, isC1)
            # cmp
            elif cmpcolor == Opcode.CMP:
                print("cmp", end=" ", file=file)
                val1 = read(color1, isR1, isP1, isC1)
                # Set Comparison Flags
                writeRVal(6, 16581630 if (val1 == val2) else 0)
                writeRVal(7, 16581630 if (val1 < val2) else 0)
                writeRVal(8, 16581630 if (val1 > val2) else 0)

            print(alu_op_repr, file=file)
        # jmp
        elif cmpcolor == Opcode.JMP:
            e = readRVal(6)
            l = readRVal(7)
            g = readRVal(8)
            fwd = readC(color1)
            if (isR1 and e) or (isP1 and not e) or (isR2 and l) or (isP2 and g):
                cTurt.right(90)
                cTurt.forward((fwd - 1) * 5)
                cTurt.left(90)
            print(f"{determineJump(isR1, isP1, isR2, isP2)} {(fwd)}", file=file)
            # else:
            #     print("nop", file=file)
        # call
        elif cmpcolor == Opcode.CALL:
            sTurt.back(5)
            writeS(0, (color1[0], color1[1], 127))
            cTurt.forward(color1[0] * 5)
            cTurt.left(90)
            cTurt.forward((color1[1] + 1) * 5)

            cTurt.forward(-5)
            print(f"call {getCoords()}", file=file)
            cTurt.forward(5)
            cTurt.right(90)
        elif cmpcolor == Opcode.RET:
            cTurt.left(90)
            cTurt.forward(readC(color1) * 5)
            cTurt.left(90)
            cTurt.forward(readS(0)[0] * 5)
            cTurt.left(90)
            cTurt.forward(readS(0)[1] * 5)
            cTurt.left(90)
            sTurt.forward(5)
            print(f"ret {readC(color1)}", file=file)
        else:
            raise BaseException(f"{getCoords()} unknown: %s" % str(cmpcolor))

        print("", file=file)
        cTurt.right(90)
        cTurt.forward(5)
        cTurt.left(90)


# flag = input("Flag: ")
# if len(flag) != 35:
#     print("Wrong len :(")
#     exit(0)

flag = 'a' * 35

loadM(flag, file=r'C:\Users\NAZRU\CS projects\Turtle CTF\m.png')
loadS()
loadR()
loadC(r'C:\Users\NAZRU\CS projects\Turtle CTF\files\smthn.png')

# memoryDump(file=r'C:\Users\NAZRU\CS projects\Turtle CTF\files\memory.txt', infile='c.png')
run(r"files/process.txt")
