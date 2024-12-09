
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
        if not safer:
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
    """ itérateur sur les positions de la grille """
    for x in range(w):
        for y in range(h):
            yield x,y

def add(pos,direc):
    """ ajoute direc à pos (vecteurs) """
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

def day5(i):
    s1 = 0
    s2 = 0

    rules,lists = i.split("\n\n")

    updates = lists.split("\n")
    updates = [e.split(',') for e in updates if e]

    rules = rules.split("\n")
    rules = [r.split("|") for r in rules]
    islessthan = {}

    for a,b in rules:
        if a in islessthan:
            islessthan[a].append(b)
        else:
            islessthan[a] = [b]

    def compare(a,b):
        if a in islessthan[b] :
            return -1
        return 1

    def isordered(l):
        for i in range(len(l)):
            for j in range(i+1,len(l)):
                if compare(l[i],l[j]) == -1:
                    return False
        return True

    def middle(l):
        return l[int(len(l)/2)]

    for update in updates:
        if isordered(update):
            s1 += int(middle(update))
        else:
            update = sorted(update,key=cmp_to_key(compare))
            s2 += int(middle(update))

    return s1,s2

def day6(i):
    s = 0
    t = []
    f = i.split('\n')
    for line in f:
        if line:
            t.append(list(line))
    w = len(t[0])
    h = len(t)

    def get(cpos):
        x,y = cpos
        if 0<=x<w and 0<=y<h:
            return t[y][x]
        return 'F'

    def tset(cpos,v):
        x,y = cpos
        t[y][x] = v

    initpos = (0,0)
    for cpos in ppos(w,h):
        if get(cpos) == '^':
            initpos = cpos
    direcs = [(0,-1),(1,0),(0,1),(-1,0)]

    # Part 1
    positions = set()
    l = 0
    i = 0
    loop = False
    pos = initpos
    while get(pos) != 'F':
        positions.add(pos)
        npos = add(pos,direcs[i])
        if get(npos) == '#':
            i = (i+1) % 4
        else:
            pos = npos
    s1 = len(positions)

    # Part 2
    s2 = 0
    for change in ppos(w,h):
        if get(change) == '#':
            continue
        tset(change,'#')
        # redémarrer le parcours dans cette nouvelle map
        positions = set()
        i = 0
        loop = False
        pos = initpos
        while get(pos) != 'F' and not loop:
            npos = add(pos,direcs[i])
            if get(npos) == '#':
                i = (i+1) % 4
            else:
                pos = npos
            if (pos,i) in positions:
                loop = True
            else:
                positions.add((pos,i))
        s2 += loop
        tset(change,'.')
    return s1,s2
def day9(i):
    s = 0
    carte = []
    file = True
    ID = 0
    paquets_vides = []
    paquets_pleins = []
    class Data:
        def __init__(self,ID,qqty):
            self.ID = ID
            self.qqty = qqty
        def __repr__(self):
            return "ID : "+self.ID+" QQTY : "+str(self.qqty)
    class Vide:
        def __init__(self,q,prec):
            self.qqty = q
            self.prec = prec
        def __repr__(self):
            return 'vide :'+str(self.qqty)

    for c in i[:-1]:
        qqty = int(c)
        if file:
            e = Data(str(ID),qqty)
            carte.append(e)
            paquets_pleins.append(e)
            ID += 1
        else:
            e = Vide(qqty,str(ID))
            carte.append(e)
            paquets_vides.append(e)
        file = not file
    print(carte)
    paquets_pleins.reverse()
    def remplissage():
        current_vide = paquets_vides[0]
        current_data = paquets_pleins[0]
        while current_vide.prec != current_data.ID:
            # q : la quantité transférée
            if current_vide.qqty >= current_data.qqty:
                # si on a plus de place, on met tout
                q = current_data.qqty
            else:
                # sinon, on bourre ce qu'il reste
                q = current_vide.qqty
            if q:
                current_vide.qqty -= q
                current_data.qqty -= q
                yield Data(current_data.ID,q)
            if current_vide.qqty == 0:
                paquets_vides.pop(0)
                if paquets_vides:
                    current_vide = paquets_vides[0]
                yield 'Nouveau Pas'
            if current_data.qqty == 0:
                paquets_pleins.pop(0)
                if paquets_pleins:
                    current_data = paquets_pleins[0]

        if current_vide.qqty >= current_data.qqty:
            # si on a plus de place, on met tout
            q = current_data.qqty
        else:
            # sinon, on bourre ce qu'il reste
            q = current_vide.qqty
        if q:
            current_vide.qqty -= q
            current_data.qqty -= q
            yield Data(current_data.ID,q)
        yield 'Nouveau Pas'
        

    rempli = remplissage()
    flag = True
    newmap = []
    for elem in carte:
        if type(elem) == type(Data("r",1)) and elem.qqty:
            newmap.append(elem)
        else:
            try:
                e = next(rempli)
            except StopIteration:
                flag = False
            while e!="Nouveau Pas" and flag:
                newmap.append(e)
                try:
                    e = next(rempli)
                except StopIteration:
                    flag = False
        if not flag:
            break
    print(newmap)
    total = sum(e.qqty for e in newmap)
    i = 0
    itr = iter(newmap)
    c = next(itr)
    while i < total:
        s += int(c.ID) * i
        i += 1
        c.qqty -= 1
        if c.qqty == 0:
            try:
                c = next(itr)
            except StopIteration:
                break
    return s


def solve(d,i):
    if d == 1:
        return day1(i)
    elif d == 2:
        return day2(i)
    elif d == 3:
        return day3(i)
    elif d == 4:
        return day4(i)
    elif d == 5:
        return day5(i)
    elif d == 6:
        return day6(i)
    else:
        return "Unknown day"

