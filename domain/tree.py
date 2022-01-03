class Node:
    def __init__(self, val, c, rs):
        self.val = val
        self.c = c
        self.rs = rs

    def __str__(self):
        return "({}, {}, {})".format(self.val, self.c, self.rs)


class Tree:
    def __init__(self, grammar):
        self.root = None
        self.grammar = grammar
        self.crt = 1
        self.ws = ""
        self.indexInTreeSequence = 1

    def buildTree(self, ws):
        print(ws)
        print(len(ws))
        self.ws = ws
        nonterminal, rhs = self.grammar.getProductionForIndex(int(self.ws[0]))
        self.root = Node(nonterminal, None, None)
        self.root.c = self.buildRecursiveTree(self.grammar.splitRight(rhs))
        return self.root

    def buildRecursiveTree(self, currentTransition):
        if (self.indexInTreeSequence == len(self.ws) and currentTransition == ['E']):
            pass
        elif currentTransition == [] or self.indexInTreeSequence >= len(self.ws):
            return None
        # ws = 1213....
        # print("ws: " + ws)
        # print("rhs: " + str(rhs))
        currentSymbol = currentTransition[0]
        if currentSymbol in self.grammar.E:
            node = Node(currentSymbol, None, None)
            print("current val: " + node.val)
            print("finished terminal branch")
            node.rs = self.buildRecursiveTree(currentTransition[1:])
            return node
        elif currentSymbol in self.grammar.N:
            transitionNumber = self.ws[self.indexInTreeSequence]
            _, production = self.grammar.getProductionForIndex(
                int(transitionNumber))
            node = Node(currentSymbol, None, None)
            print("current val: " + node.val)
            print("finished nonterminal branch")
            self.indexInTreeSequence += 1
            node.c = self.buildRecursiveTree(
                self.grammar.splitRight(production))
            node.rs = self.buildRecursiveTree(currentTransition[1:])
            return node
        else:
            print('E branch')
            return Node("E", None, None)

    def print_table(self):
        self.BFS(self.root)

    def BFS(self, node, father_crt=None, left_sibling_crt=None):
        if node is None:
            return []
        print("{} | {} | {} | {}".format(
            self.crt, node.val, father_crt, left_sibling_crt))

        crt = self.crt
        self.crt += 1

        if left_sibling_crt is not None:
            return [[node.c, crt, None]] + self.BFS(node.rs, father_crt, crt)
        else:
            children = [[node.c, crt, None]] + \
                self.BFS(node.rs, father_crt, crt)
            for c in children:
                self.BFS(*c)

    def __str__(self):
        string = ""
        node = self.root
        while node is not None:
            string += str(node)
            node = node.rs
        return string
