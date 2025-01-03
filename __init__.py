
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
    def repres(carte):
        for elem in carte:
            if type(elem) == Vide:
                print("."*elem.qqty,end="")
            else:
                print(elem.ID*elem.qqty,end="")
        print()

    for c in i:
        if c != '\n':
            qqty = int(c)
        if file:
            e = Data(str(ID),qqty)
            carte.append(e)
            paquets_pleins.append(e)
            ID += 1
        elif qqty!=0:
            e = Vide(qqty,str(ID))
            carte.append(e)
            paquets_vides.append(e)
        file = not file

    print(carte)
    repres(carte)
    paquets_pleins.reverse()
    for elem in paquets_pleins:
        for i in range(len(carte)):
            if carte[i] == elem:
                break
            if type(carte[i]) == Vide and carte[i].qqty >= elem.qqty:
                carte[i].qqty -= elem.qqty
                carte.insert(i,Data(elem.ID,elem.qqty))
                elem.ID = str(0)
                break
    print(carte)
    mul = 0
    for elem in carte:
        if type(elem) == Vide:
            mul += elem.qqty
        else:
            for i in range(elem.qqty):
                s += mul*int(elem.ID)
                mul += 1

    return s

def day10(i):
    s1 = 0
    s2 = 0
    t = []
    for line in i.split('\n'):
        if line:
            t.append(line)
    w = len(t[0])
    h = len(t)

    def get(t,pos):
        x,y = pos
        if 0<=x<w and 0<=y<h:
            return t[y][x]
        else:
            return "-1"

    def around(pos):
        neigh = [(-1,0),(1,0),(0,-1),(0,1)]
        for n in neigh:
            yield add(pos,n)

    def reacheable(pos,ind):
        """ renvoie la liste des chemins atteignant un 9 """
        if ind == 9:
            return [[pos]]
        else:
            paths = []
            for pos in around(pos):
                if int(get(t,pos)) == ind+1:
                    l = reacheable(pos,ind+1)
                    for elem in l:
                        elem.append(pos)
                    paths += l
            return paths

    for pos in ppos(w,h):
        if get(t,pos) == '0':
            r = reacheable(pos,0)
            s1 += len(set([e[0] for e in r]))
            s2 += len(r)
    return s1,s2

def get(t,d,bord,pos):
    w,h = bord
    x,y = pos
    if 0<=x<w and 0<=y<h:
        return t[y][x]
    return d

def setpos(t,bord,pos,v):
    w,h = bord
    x,y = pos
    if 0<=x<w and 0<=y<h:
        t[y][x] = v
    

def add(pos,direc):
    return pos[0] + direc[0], pos[1] + direc[1]

def aroundd(pos):
    neigh = [((-1,0),'g'),((1,0),'d'),((0,-1),'h'),((0,1),'b')]
    for n,ori in neigh:
        yield add(pos,n),ori


def day12(f):
    s1 = 0
    s2 = 0
    t = []
    flag = [] # visitied
    for line in f.split('\n'):
        if line:
            t.append(line)
            flag.append([False for _ in line])
    w = len(t[0])
    h = len(t)
    gett = lambda pos : get(t,'.',(w,h),pos)
    getf = lambda pos : get(flag,False,(w,h),pos)
    setf = lambda pos,value : setpos(flag,(w,h),pos,value)
    regions = set()
    def explore(pos,typ,visited,ori):
        if gett(pos) != typ:
            return set(),[(ori,pos)]
        else:
            region = set([pos])
            perimeter = []
            setf(pos,True)
            visited.add(pos)
            for npos,ori in aroundd(pos):
                if npos not in visited:
                    nregion,nperi = explore(npos,typ,visited,ori)
                    region = region.union(nregion)
                    perimeter += nperi
            return region,perimeter
    def different(positions,close):
        suggestions = []
        for pos in positions:
            found = False
            for sugg in suggestions:
                if any(close(pos,sugg_pos) for sugg_pos in sugg):
                    sugg.append(pos)
                    found = True
            if found == False:
                suggestions.append([pos])
        return len(suggestions)


    for pos in ppos(w,h):
        if getf(pos):
            continue
        typ = gett(pos)
        region, borders = explore(pos,typ,set(),'')
        bspec = {'h':[],'g':[],'b':[],'d':[]}
        for ori,pos in borders: 
            bspec[ori].append(pos)
        nfaces = 0
        for key in bspec:
            if key in 'gd':
                # si c'est un truc au dessus ou au dessous
                bspec[key].sort(key = lambda pos:pos[1])
                close = lambda pos,sugg : sugg == add(pos,(0,-1)) or sugg == add(pos,(0,1))
            else:
                # si c'est un truc à gauche ou à droite
                bspec[key].sort(key = lambda pos:pos[0])
                close = lambda pos,sugg : sugg == add(pos,(-1,0)) or sugg == add(pos,(1,0))
            nfaces += different(bspec[key],close)
        s1 += len(region) * len(border)
        s2 += len(region) * nfaces
    return s1,s2




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
    elif d == 9:
        return day9(i)
    elif d == 10:
        return day10(i)
    elif d == 12:
        return day12(i)
    else:
        return "Unknown day"

