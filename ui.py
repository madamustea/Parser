from domain.grammar import Grammar
from domain.parser import Parser
from domain.tree import Tree


class UI:

    def __init__(self):
        self.grammar = None
        self.parser = None

    def run(self):
        while True:
            print("1.Evaluate G1")
            print("2.Evaluate G2")
            print("3.Evaluate G3")
            cmd = int(input("Give me an option:"))
            if cmd == 1:
                self.evaluateG1()
            elif cmd == 2:
                self.evaluateG2()
            elif cmd == 3:
                self.evaluateG3()

    def readG1(self):
        self.g1 = Grammar.ReadFromFile('g1.txt')
        print('Read g1')

    def readG2(self):
        self.g2 = Grammar.ReadFromFile('g2.txt')
        print('Read g2')

    def readG3(self):
        self.g3 = Grammar.ReadFromFile('g3.txt')
        print('Read g3')

    def readSeq(self, fname):
        sequence = ""
        with open(fname, 'r') as fin:
            for l in fin.readlines():
                sequence += l.strip() + " "
        return sequence.strip()

    def evaluateG1(self):
        self.readG1()
        self.p1 = Parser(self.g1)
        print(self.p1.firstS)
        print(self.p1.followS)
        for k in self.p1.table.keys():
            print(k, '->', self.p1.table[k])
        result = self.p1.evaluateSeq(self.readSeq('seq.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g1)
            t.buildTree(result.strip().split(' '))
            t.print_table()

    def evaluateG2(self):
        self.readG2()
        self.p2 = Parser(self.g2)
        print(self.p2.firstS)
        print(self.p2.followS)
        for k in self.p2.table.keys():
            print(k, '->', self.p2.table[k])
        result = self.p2.evaluateSeq(self.readSeq('seq2.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g2)
            t.buildTree(result.strip().split(' '))
            t.print_table()

    def evaluateG3(self):
        self.readG3()
        self.p3 = Parser(self.g3)
        print(self.p3.firstS)
        print(self.p3.followS)
        for k in self.p3.table.keys():
            print(k, '->', self.p3.table[k])
        result = self.p3.evaluateSeq(self.readSeq('seq3.txt'))
        if result is None:
            print("Sequence not accepted")
        else:
            print(result)
            t = Tree(self.g3)
            t.buildTree(result.strip().split(' '))
            t.print_table()
