
class Grammar:

    def __init__(self, N, E, P, S):
        self.N = N
        self.E = E
        self.P = P
        self.S = S

    @staticmethod
    def parseOneLine(line):
        return [i.strip() for i in line.strip().split(':=')[1].strip()[1:-1].strip().split(',')]

    @staticmethod
    def rulesParsing(rules):
        index = 1
        res = {}
        for r in rules:
            print(r)
            left, right = r.split('->')
            left = left.strip()
            right = [value.strip() for value in right.split('|')]

            for value in right:
                if left in res.keys():
                    res[left].append((value, index))
                else:
                    res[left] = [(value, index)]
                index += 1

        return res

    @staticmethod
    def ReadFromFile(file):

        with open(file, 'r') as f:
            N = Grammar.parseOneLine(f.readline())
            E = Grammar.parseOneLine(f.readline())
            S = f.readline().split(":=")[1].strip()
            P = Grammar.rulesParsing(
                Grammar.parseOneLine(''.join([line for line in f])))

            return Grammar(N, E, P, S)

    def splitRight(self, p):
        return p.split(' ')

    def isNonTerminal(self, t):
        return t in self.N

    def isTerminal(self, t):
        return t in self.E

    def getProductionsFor(self, nonT):
        if not self.isNonTerminal(nonT):
            raise Exception('Productions are only for non terminal')
        for key in self.P.keys():
            if key == nonT:
                return self.P[key]

    def getProductionForIndex(self, index):
        for key, value in self.P.items():
            for v in value:
                if v[1] == index:
                    return key, v[0]

    def __str__(self):
        return 'N = { ' + ', '.join(self.N) + ' }\n' \
               + 'E = { ' + ', '.join(self.E) + ' }\n' \
               + 'P = { ' + ', '.join([' -> '.join(prod) for prod in self.P]) + ' }\n' \
               + 'S = ' + str(self.S) + '\n'
