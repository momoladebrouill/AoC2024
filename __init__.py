
# aoc -e pour l'example

def occ(x,l):
    """Compte les occurences de x dans l **triée**"""
    n = 0
    for i in l:
        if i > x:
            return n
        elif i == x:
            n += 1
    return n

def day1(i):
    """ Jour 1 input -> s1,s2 """
    gl = []
    dl = []
    for l in i.split("\n"):
        g,d = l.split("   ")
        gl.append(int(g))
        dl.append(int(d))
    gl.sort()
    dl.sort()
    s1 = 0
    s2 = 0
    for a,b in zip(gl,dl):
        s1 += abs(a-b)
    for left in gl:
        s2 += left*occ(left,dl)
    return (s1,s2)

def is_safe(l):
    safe = True
    sign = l[0] - l[1]
    for i in range(len(l)-1):
        if l[i] == l[i+1] \
                or abs(l[i] - l[i+1]) > 3 \
                or (l[i] - l[i+1])*sign <= 0:
            safe = False
            break
    return safe

def day2(i):
    s1 = 0
    s2 = 0
    for l in i.split("\n"):
        l = l.split(" ")
        if not l:
            pass
        l = [int(e) for e in l]
        safer = False
        if is_safe(l):
            safer = True
        s1 += safer
        else:
            for i in range(len(l)):
                lp = l.copy()
                lp.pop(i)
                if is_safe(lp):
                    safer = True
                    break
        s2 += int(safer)
    return (s1,s2)
def day3():
    # cat input.txt | grep -oE "(do\(\)|don't\(\)|mul\([1-9][0-9]?[0-9]?,[1-9][0-9]?[0-9]?\))" > input2.txt
    mul = 1
    s1 = 0
    s2 = 0
    for line in f:
        if line == "do()\n":
            mul = 1
        elif line == "don't()\n":
            mul = 0
        else:
            line = line[4:-2]
            e = [int(e) for e in line.split(',')]
            s1 += e[0] * e[1]
            s2 += e[0] * e[1] * mul
    return s1,s2
def ppos(w,h):
    for x in range(w):
        for y in range(h):
            yield x,y

def add(pos,direc):
    return pos[0] + direc[0], pos[1] + direc[1]

def day4(i):
    word = "XMAS"
    grid = []
    for l in i.split("\n"):
        if l:
            grid.append(l)
    w = len(grid[0])
    h = len(grid)

    def get(cpos):
        x,y = cpos
        if 0<=x<w and 0<=y<h:
            return grid[y][x]
        return '.'
    dirs = [(-1,-1),(0,-1),(1,-1),
            (-1,0), (1,0),
            (-1,1),(0,1),(1,1)]

    c1 = 0
    c2 = 0

    for x,y in ppos(w,h):
        cpos = x,y
        good = False
        if get(cpos) == 'A':
            diag1 = set((get(add(cpos,(-1,-1))),get(add(cpos,(1,1)))))
            diag2 = set((get(add(cpos,(-1,1))),get(add(cpos,(1,-1)))))
            c2 += diag2 == diag1 == set(('M','S'))
        for direc in dirs:
            cpos = x,y
            good1 = True
            for char in word:
                if char != get(cpos):
                    good1 = False
                    break
                cpos = add(cpos,direc)
            c1 += good1
    return c1,c2


def solve(d,i):
    if d == 1:
        return day1(i)
    elif d == 2:
        return day2(i)
    elif d == 3:
        return day3(i)
    elif d == 4:
        return day4(i)
    else:
        return "Unknown day"

if __name__ == "__main__":
    f = open("../../aoctmp/input.txt")
    print(solve(4,f.read()))


