with open(r'asm/helloworld.txt', 'w') as f:
    msg = 'Hello World'
    for char in msg:
        f.write(f'mov reg[0], {ord(char)}\n')
        f.write(f'out reg[0]\n\n')
    f.write(f'halt')