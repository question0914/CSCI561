import copy
import random
import multiprocessing

AND = "&"
OR = "|"
NOT = "~"
END = "Terminal"

with open("input.txt", "r")as infile:
    data = infile.read()

line = data.splitlines()


# Initialize guests number and table number
M = int(line[0].split()[0])
N = int((line[0].split())[1])

# Initialize Xmn
X = list()
for i in range(0, M):
    for j in range(0, N):
        X.append("X"+str(i+1)+"_"+str(j+1))

# Knowledge base
KB = list()

# Clauses for each guest a, the assignment should be at only one table
for i in range(0,M):
    cnf = ""
    for j in range(0,N):
        if j < N-1:
            l = "X"+str(i+1)+"_"+str(j+1)+OR
        else:
            l = "X" + str(i + 1) + "_" + str(j + 1)
        cnf=cnf+l
    KB.append(cnf)

for i in range(0,M):
    for j in range(0,N):
        for m in range(j+1,N):
            l = NOT+"X"+str(i+1)+"_"+str(j+1)+OR+NOT+"X"+str(i+1)+"_"+str(m+1)
            KB.append(l)

# Clause for friends and enemy
for i in range(1, len(line)):
    a = line[i].split()[0]
    b = line[i].split()[1]
    relation = line[i].split()[2]
    if relation == "F":
        for m in range(0,N):
            for n in range(0,N):
                if m != n:
                    l = NOT+"X"+a+"_"+str(m+1)+OR+NOT+"X"+b+"_"+str(n+1)
                KB.append(l)
    if relation == "E":
        for m in range(0, N):
            l = NOT + "X" + a + "_" + str(m + 1) + OR + NOT + "X" + b + "_" + str(m + 1)
            KB.append(l)


# Concatenate elements in the set
def concatenate(s):
    if len(s) == 0:
        return s
    if len(s) == 1:
        return s[0]
    l = ""
    for i in range(0, len(s) - 1):
        l = l + s[i] + OR
    l = l + s[len(s) - 1]
    return str(l)


# Remove duplicate elements from seq. Assumes hashable elements.
def unique(seq):
    return list(set(seq))


# Return a copy of seq (or string) with all occurs of item removed.
def removeall(item, seq):
    if isinstance(seq, str):
        return seq.replace(item, '')
    else:
        return [x for x in seq if x != item]


# Split the clause to literal
def disjuncts(clause):
    l = clause.split(OR)
    return l


# Return  clauses that can be obtained by resolving clauses ci and cj
def pl_resolve(ci, cj):
    clauses = []
    for di in disjuncts(ci):
        for dj in disjuncts(cj):
            if di == NOT+dj or NOT+di == dj:
                a = removeall(di, disjuncts(ci))
                b = removeall(dj, disjuncts(cj))
                if len(a) == 1 and len(b) == 1 and (a[0] == NOT+b[0] or NOT+a[0] == b[0]):
                    return []
                dnew = unique(a+b)
                if len(dnew) == 0:
                    return END
                c = concatenate(copy.deepcopy(dnew))
                clauses.append(c)
    return clauses


def pl_resolution(KB):
    clauses = copy.deepcopy(KB)
    new = set()
    temp = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if END in resolvents:
                return False
            for i in range(0,len(resolvents)):
                temp.add((resolvents[i]))
            new.update(temp)
        if new.issubset(set(clauses)):
            return True

        for c in new:
            if c not in clauses:
                clauses.append(c)


# Separate literal from clause
def separate(clause):
    list = clause.split(OR)
    for i in range(0,len(list)):
        if list[i][0] == NOT:
            list[i] = list[i][1:]
    return list


# Return true with probability p.
def probability(p):
    return p > random.uniform(0.0, 1.0)

# get value, True =1, False = 0
def getValue(a):
    if a:
        return 1
    else:
        return 0


# Check if a clause is true
def check(clause, model):
    list = clause.split(OR)
    value = 0
    for l in list:
        if l[0] == NOT:
            value += getValue((not model[l[1:]]))
        else:
            value += getValue(model[l])
    if value > 0:
        return True
    else:
        return False


# return the flipped symbol which maximize the satisfied clauses
def maximizetrue(model, clauses):
    sym = ""
    MAX = 0
    for x in X:
        satisfied = []
        model[x] = not model[x]
        for clause in clauses:
            if check(clause, model):
                satisfied.append(clause)
        if len(satisfied) > MAX:
            MAX = len(satisfied)
            sym = x
    return sym


# walkSat
def walkSAT(clauses, p, max_flips):
    model = dict([(s, random.choice([True, False])) for s in X])
    for i in range(max_flips):
        satisfied, unsatisfied = [], []
        for clause in clauses:
            if check(clause, model):
                satisfied.append(clause)
            else:
                unsatisfied.append(clause)
        if not unsatisfied:  # if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(separate(clause))
        else:
            sym = maximizetrue(copy.deepcopy(model), clauses)
        model[sym] = not model[sym]
    return False

# Main
if __name__ == "__main__":
    log = list()
    p = multiprocessing.Process(target=pl_resolution, name="PL", args=(KB,))
    p.start()
    p.join(20)
    if p.is_alive():
        result = True
        p.terminate()
        p.join()
    else:
        result = pl_resolution(KB)
    if result == False:
        log.append("no")
    else:
        model = walkSAT(KB, 0.9, 10000)
        if model != False:
            log.append("yes\n")
            for x in X:
               if model[x] == True:
                  l = x.split("_")
                  a = l[0][1:]
                  b = l[1]
                  log.append(a+" "+b+"\n")
        else:
            log.append("no")
    with open("output.txt", "w")as outfile:
        for l in log:
           outfile.write(str(l))



