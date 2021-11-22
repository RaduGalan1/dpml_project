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
        self.total_counter += 1
        order =[]
        order_time =[]
        for i in range(self.no):
            order.append(self.variables["subject" + str(i)])

        for i in range(len(order_time)):
            for j in range(len(order_time)):
                try:
                    i_time = int(self.variables["time" + str(i)])
                    j_time = int(self.variables["time" + str(j)])

                    print(i_time, "-", j_time)
                    if abs(int(i_time) - int(j_time)) == 1:
                        if order[i] in ['ch', 'ma'] and order[j] in ['hi','ph']:
                            return False
                except:
                    pass

        try:
            if int(self.variables["time" + str(order.index('ch'))]) % 2 == 1:
                return False
        except:
            pass
        try:
            if int(self.variables["time" + str(order.index('hi'))]) in [2, 4]:
                return False
        except:
            pass
        try:
            if int(self.variables["time" + str(order.index('ph'))]) in [5, 7]:
                return False
        except:
            pass

        # work mornings or abends
        counter = 0
        length = 0
        for i in range(self.no):
            try:
                if int(self.variables["time" + str(i)]) < 5:
                    counter -= 1
                else:
                    counter += 1
                length += 1
            except:
                pass
        if counter not in [-length, length]:
            return False

        # don t works first hours
        for i in range(self.no):
            try:
                if int(self.variables["time" + str(i)]) == 1:
                    return False
            except:
                pass

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
