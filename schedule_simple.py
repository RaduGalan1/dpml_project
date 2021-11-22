from copy import deepcopy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class ScheduleSolver():
    def __init__(self):
        pass

    def find_unused_var(self):
        for var in self.variables.keys():
            if self.variables[var] == None:
                return var

    def permutation(self):
        if None not in self.variables.values():
            # print(self.variables)
            self.results.append(deepcopy(self.variables))

            # if str(self.variables2) == str(self.variables):
            #     print("EQUAL")
            return
        var = self.find_unused_var()
        for d_orig in self.D[var[:-1]]:
            d = deepcopy(d_orig)
            self.variables[var] = d
            self.D[var[:-1]].remove(d_orig)
            if self.constraints():
                self.permutation()
            self.variables[var] = None
            self.D[var[:-1]].append(d)

    def constraints(self):
        order =[]
        for i in range(self.no):
            order.append(self.variables["subject" + str(i)])

        if 'ch' in order and order.index('ch') % 2 == 0:
            return False

        return True

    def run_full_backtrack(self):

        self.D = {'subject':['ma', 'ch', 'ph', 'hi'], 'time':['1','2','3','4','5','6','7','8']}
        var = ['subject','time']


        self.no = 3
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v + str(i)] = None
        print(self.variables)
        self.results = []

        self.total_counter = 0
        self.permutation()

        unique_solutions = []
        for el in self.results:
            print(el)
            # adable = tuple([el['dino0'],el['dino1'],el['dino2'],el['dino3'],el['dino4']])
            # unique_solutions.append(adable)
        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(set(unique_solutions)))

    def print_graph(self):
        G = nx.Graph()
        # Add nodes
        for node in self.variables.keys():
            G.add_node(node)

        nx.draw(G, with_labels=True)
        plt.savefig('labels_schedule2.png')


import time
def main():
    time.sleep(0)
    solver = ScheduleSolver()
    solver.run_full_backtrack()
    solver.print_graph()
main()
