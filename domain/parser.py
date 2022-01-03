from copy import deepcopy


class Parser:

    def __init__(self, g):
        self.grammar = g
        self.table = {}
        self.firstS = {i: set() for i in self.grammar.N}
        self.followS = {i: set() for i in self.grammar.N}
        self.generateFirst()
        self.generateFollow()
        self.generateTable()

    def Loop(self, initial, items, additional):
        copy = initial
        for i in range(len(items)):
            if self.grammar.isNonTerminal(items[i]):
                copy = copy.union(
                    entry for entry in self.firstS[items[i]] if entry != 'E')
                if 'E' in self.firstS[items[i]]:
                    if i < len(items) - 1:
                        continue
                    copy = copy.union(additional)
                    break
                else:
                    break
            else:
                copy = copy.union({items[i]})
                break

        return copy

    def generateFirst(self):
        ok = False
        for key, value in self.grammar.P.items():
            for v in value:
                v = self.grammar.splitRight(v[0])
                copy = self.firstS[key]
                copy = copy.union(self.Loop(copy, v, ['E']))

                if len(self.firstS[key]) != len(copy):
                    self.firstS[key] = copy
                    ok = True

        while ok:
            ok = False
            for key, value in self.grammar.P.items():
                for v in value:
                    v = self.grammar.splitRight(v[0])
                    copy = self.firstS[key]
                    copy = copy.union(self.Loop(copy, v, ['E']))

                    if len(self.firstS[key]) != len(copy):
                        self.firstS[key] = copy
                        ok = True

    def generateFollow(self):
        self.followS[self.grammar.S].add('E')
        ok = False
        for key, value in self.grammar.P.items():
            for v in value:
                v = self.grammar.splitRight(v[0])
                for i in range(len(v)):
                    if not self.grammar.isNonTerminal(v[i]):
                        continue
                    copy = self.followS[v[i]]
                    if i < len(v) - 1:
                        copy = copy.union(
                            self.Loop(copy, v[i + 1:], self.followS[key]))
                    else:
                        copy = copy.union(self.followS[key])

                    if len(self.followS[v[i]]) != len(copy):
                        self.followS[v[i]] = copy
                        ok = True
        while ok:
            ok = False
            for key, value in self.grammar.P.items():
                for v in value:
                    v = self.grammar.splitRight(v[0])
                    for i in range(len(v)):
                        if not self.grammar.isNonTerminal(v[i]):
                            continue
                        copy = self.followS[v[i]]
                        if i < len(v) - 1:
                            copy = copy.union(
                                self.Loop(copy, v[i + 1:], self.followS[key]))
                        else:
                            copy = copy.union(self.followS[key])

                        if len(self.followS[v[i]]) != len(copy):
                            self.followS[v[i]] = copy
                            ok = True

    def generateTable(self):
        nonterminals = self.grammar.N
        terminals = self.grammar.E

        for key, value in self.grammar.P.items():
            # value = (right, count)
            rowSymbol = key  # A
            for v in value:
                rule = self.grammar.splitRight(v[0])  # alpha
                index = v[1]
                for columnSymbol in terminals + ['E']:  # coloana/ a
                    pair = (rowSymbol, columnSymbol)   # M(A, a)
                    # rule 1 part 1
                    if rule[0] == columnSymbol and columnSymbol != 'E':
                        self.table[pair] = v
                    elif rule[0] in nonterminals and columnSymbol in self.firstS[rule[0]]:
                        if pair not in self.table.keys():
                            self.table[pair] = v
                        else:
                            print(self.table)
                            print(pair)
                            print("Not LL(1).")
                            assert False
                    else:
                        if rule[0] == 'E':
                            for i in self.followS[rowSymbol]:
                                if i == 'E':
                                    i = '$'
                                self.table[(rowSymbol, i)] = v
                        else:
                            # rule 1 part 2
                            firsts = set()
                            for symbol in self.grammar.P[rowSymbol]:
                                if symbol in nonterminals:
                                    firsts = firsts.union(
                                        self.firstSet[symbol])
                            if 'E' in firsts:
                                for i in self.followSet[rowSymbol]:
                                    if i == 'E':
                                        i = '$'
                                    if (rowSymbol, i) not in self.table.keys():
                                        self.table[(rowSymbol, i)] = v
        # rule 2
        for t in terminals:
            self.table[(t, t)] = ('pop', -1)

        # rule 3
        self.table[('$', '$')] = ('acc', -1)

    def evaluateSeq(self, sequence):
        r = self.grammar.splitRight(sequence)
        s = [self.grammar.S, '$']
        output = ""
        while s[0] != '$' and r:
            print(r, s)
            if r[0] == s[0]:
                r = r[1:]
                s.pop(0)
            else:
                x = r[0]
                a = s[0]
                if (a, x) not in self.table.keys():
                    return None
                else:
                    s.pop(0)
                    right, index = self.table[(a, x)]
                    right = self.grammar.splitRight(right)
                    for i in range(len(right) - 1, -1, -1):
                        if right[i] != 'E':
                            s.insert(0, right[i])
                    output += str(index) + " "
            print(output)
        if s[0] == '$' and r:
            return None
        elif not r:
            while s[0] != '$':
                a = s[0]
                if (a, '$') in self.table.keys():
                    output += str(self.table[(a, '$')][1]) + " "
                s.pop(0)
            return output
