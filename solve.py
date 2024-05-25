orderPos = [23, 14, 7, 18, 12, 1, 28, 15, 26, 0, 5, 21, 27, 3, 11, 24, 13, 2, 8, 22, 6, 10, 29, 19, 17, 9, 20, 4, 16, 25,]
pixels = [1, 1, 1, 3, 1, 1, 1, 2, 1, 4, 1, 1, 1, 2, 3, 1, 1, 3, 1, 1, 2, 1, 3, 1, 1, 2, 3, 1, 1, 2, 2, 3, 1, 1, 2, 2, 2, 4, 1, 3, 1, 2, 1, 1, 1, 4, 1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 4, 1, 2, 1, 3, 1, 2, 1, 2, 1, 4, 1, 2, 1, 2, 1, 4, 1, 2, 1, 2, 3, 1, 2, 3, 1, 2, 2, 1, 1, 4, 1, 2, 2, 1, 1, 4, 1, 2, 2, 1, 1, 4, 1, 2, 2, 1, 1, 4, 1, 2, 2, 1, 1, 4, 1, 2, 2, 1, 3, 1, 2, 2, 1, 2, 4, 1, 2, 2, 1, 2, 4, 1, 2, 2, 1, 2, 4, 1, 2, 2, 3, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 1, 4, 1, 2, 2, 2, 3, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 1, 2, 2, 2, 2, 4, 3, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 4, 2, 1, 1, 3, 2, 1, 1, 2, 1, 4, 2, 1, 1, 2, 3, 2, 1, 1, 2, 2, 4, 2, 1, 1, 2, 2, 4, 2, 1, 1, 2, 2, 4, 2, 1, 1, 2, 2, 4, 2, 1, 1, 2, 2, 4, 2, 1, 3, 2, 1, 2, 1, 1, 4, 2, 1, 2, 1, 3, 2, 1, 2, 1, 2, 4, 2, 1, 2, 1, 2, 4, 2, 1, 2, 3, 2, 1, 2, 2, 3, 2, 1, 2, 2, 2, 4, 2, 1, 2, 2, 2, 4, 2, 3, 2, 2, 1, 1, 3, 2, 2, 1, 1, 2, 4, 2, 2, 1, 1, 2, 4, 2, 2, 1, 3, 2, 2, 1, 2, 1, 4, 2, 2, 1, 2, 3, 2, 2, 1, 2, 2, 4, 2, 2, 1, 2, 2, 4, 2, 2, 1, 2, 2, 4, 2, 2, 3, 2, 2, 2, 1, 3, 2, 2, 2, 3, 2, 2, 2, 2, 1, 4, 2, 2, 2, 2, 1, 4, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 4, 0, ]
ram = ["_"] * 30
r519 = 0


def solve(offset, ind, check):
    global r519
    if r519 == 424:
        exit(0)
    if pixels[r519] == 4:
        r519 += 1
        return
    prev = ind
    ind = (ind - 1) >> 1
    ramIndex = orderPos.index(ind + offset)
    if pixels[r519] == 1:
        r519 += 1
        solve(offset, ind, check)
    elif pixels[r519] == 2:
        r519 += 1
        solve(offset + ind + 1, prev - ind - 1, check)
    elif pixels[r519] == 3:
        ram[ramIndex] = chr(check)
        r519 += 1
        print("".join(ram))
    return


for i in range(43, 122):
    solve(0, 30, i)

print("".join(ram))

"""
From PAINFULLY gathering what I could about the assembly program
I can conclude that I am probably an idiot with a low attention span
and that I need to steer this program into the correct check

I will use r519 to denote the correct index in ram with 95 offset
There are 4 possible routes:

sp[1] == 0. r519 must equal 4

if ram[(sp[1] - 1) >> 1 + sp[0]] <= sp[2]:
    if ram[(sp[1] - 1) >> 1 + sp[0]] => sp[2]:
        r519 must equal 3
        ret
    else:
        r519 must equal 2
        magic
        recurse
        ret
else:
    r519 must equal 1
    recurse
    ret

This is pretty clever, lets define 
sp[3] = (sp[1] - 1) >> 1
index = ram[sp[3] + sp[0]]
bool a = index <= sp[2]
bool b = index => sp[2]

Truth table (a, b, operation):
True, True, equal
True, False, less than
False, True, greater than
False, False, greater than

Therefore, sp[1] == 0, r519 = 4
when index == sp[2], r519 = 3
when index < sp[2], r519 = 2
when index > sp[2], r519 = 1

Furthermore, when index < sp[2] 
sp[1] = sp[1] - sp[3] - 1
sp[0] = sp[3] + 36
These values are passed to a new function call

This process is repeated in a loop for (122 - 43) cycles
It probably should end when r519 == (0, 0, 0) (525 - 519 = 6, 6th last index in RAM)

30 -> 14 -> 6 -> 2 -> 0

Demonstration
when sp[2] == 43
index > sp[2]
index > sp[2]
index > sp[2]
index == sp[2]
when sp[2] == 44
index > sp[2]
index > sp[2]
index > sp[2]
index < sp[2]

Ok I solved it, and it only took so long because I was indexing
orderPos for just the ind (sp[3]) rather than ind + offset (sp[3] + sp[0])
So kill me now  

Overall, maybe this algorithm was some kind of implementation of a binary search, I mean it did use the length of the flag, and
progressively divided by 2. And based on whether or not the current index was greater or equal to it would perform some action.
It would only return when sp[1] = 0 or pixels[r519] == 3.

Shit they're after me. This is my last entry. BYE.
 -RAIYAN i
"""
