
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
    s = 0
    for l in i.split("\n"):
        l = l.split(" ")
        if not l:
            pass
        l = [int(e) for e in l]
        safer = False
        if is_safe(l):
            safer = True
        else:
            for i in range(len(l)):
                lp = l.copy()
                lp.pop(i)
                if is_safe(lp):
                    safer = True
                    break
        s += int(safer)
    return (0,s)
def day3():
    # cat input.txt | grep -oE "(do\(\)|don't\(\)|mul\([1-9][0-9]?[0-9]?,[1-9][0-9]?[0-9]?\))" > input2.txt
    mul = 1
    s=0
    for line in f:
        if line == "do()\n":
            mul = 1
        elif line == "don't()\n":
            mul = 0
        else:
            line = line[4:-2]
            e = [int(e) for e in line.split(',')]
            s += e[0] * e[1] * mul

    return s

def solve(d,i):
    if d == 1:
        return day1(i)
    elif d == 2:
        return day2(i)
    elif d == 3:
        return day3(i)
    else:
        return "Unknown day"


