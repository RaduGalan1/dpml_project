from copy import deepcopy
from sys import getsizeof

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from memory_profiler import profile


class ScheduleSolver():
    def __init__(self):
        self.iterations = 0
        self.memory_history = []

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

        self.iterations += 1
        for d_orig in self.D[var]:
            d = deepcopy(d_orig)

            self.memory_history.append([d])
            self.variables[var] = d
            self.D[var].remove(d_orig)
            if self.constraints() and self.nu_constraints():
                self.permutation()
            self.variables[var] = None
            self.D[var].append(d)

    def permutation_nc(self):
        if None not in self.variables.values():
            # print(self.variables)
            self.results.append(deepcopy(self.variables))

            # if str(self.variables2) == str(self.variables):
            #     print("EQUAL")
            return



        add_back = []
        var = self.find_unused_var()


        for value in self.D[var]:
            self.variables[var] = value

            self.memory_history.append([value])
            order = []
            order_time = []
            for i in range(self.no):
                order.append(self.variables["subject" + str(i)])
                order_time.append(self.variables["time" + str(i)])

            if (self.constraints(order, order_time) and self.nu_constraints(order, order_time)) is False:
                add_back.append(value)
                self.D[var].remove(value)

        self.variables[var] = None

        self.iterations += 1
        for d_orig in self.D[var]:
            d = deepcopy(d_orig)
            self.variables[var] = d

            self.memory_history.append([d])
            self.D[var].remove(d_orig)
            if self.constraints() and self.nu_constraints():
                self.permutation_nc()
            self.variables[var] = None
            self.D[var].append(d)

        for el in add_back:
            self.D[var].append(el)

    def nu_constraints(self,order = None, order_time = None):
        if order is None and order_time is None:
            order =[]
            order_time = []
            for i in range(self.no):
                if self.variables["subject" + str(i)] is not None and self.variables["subject" + str(i)] in order:
                    return False
                if self.variables["time" + str(i)] is not None and self.variables["time" + str(i)] in order_time:
                    return False
                order.append(self.variables["subject" + str(i)])
                order_time.append(self.variables["time" + str(i)])
        else:
            order_check = []
            order_time_check = []
            for i in range(self.no):
                if self.variables["subject" + str(i)] is not None and self.variables["subject" + str(i)] in order_check:
                    return False
                if self.variables["time" + str(i)] is not None and self.variables["time" + str(i)] in order_time_check:
                    return False
                order_check.append(self.variables["subject" + str(i)])
                order_time_check.append(self.variables["time" + str(i)])
        return True


    def constraints(self,order = None, order_time = None):
        if order is None and order_time is None:
            order =[]
            order_time = []
            for i in range(self.no):
                order.append(self.variables["subject" + str(i)])
                order_time.append(self.variables["time" + str(i)])

        self.total_counter += 1

        self.memory_history.append([order,order_time])
        for i in range(len(order_time)):
            for j in range(len(order_time)):
                try:
                    i_time = int(order_time[i])
                    j_time = int(order_time[j])

                    if abs(int(i_time) - int(j_time)) == 1:
                        if order[i] in ['ch', 'ma'] and order[j] in ['hi','ph']:
                            return False
                        if order[j] in ['ch', 'ma'] and order[i] in ['hi','ph']:
                            return False
                except Exception as e:
                    pass

        try:
            if int(order_time[order.index('ch')]) % 2 == 0:
                return False
        except Exception as e:
            pass
        try:
            if int(order_time[ order.index('hi')]) not in [2, 4]:
                return False
        except Exception as e:
            pass
        try:
            if int(order_time[order.index('ph')]) not in [5, 7]:
                return False
        except Exception as e:
            pass

        # # work mornings or abends
        counter = 0
        length = 0
        for i in range(self.no):
            try:
                if int(order_time[i]) < 5:
                    counter -= 1
                else:
                    counter += 1
                length += 1
            except Exception as e:
                pass
        if counter not in [-length, length]:
            return False

        # don t works first hours
        for i in range(self.no):
            try:
                if int(order_time[i]) == 1:
                    return False
            except Exception as e:
                pass
        return True


    def constraints_ac(self,order = None, order_time = None):
        if order is None and order_time is None:
            order =[]
            order_time = []
            for i in range(self.no):
                order.append(self.variables["subject" + str(i)])
                order_time.append(self.variables["time" + str(i)])

        self.memory_history.append([order,order_time])
        for i in range(len(order_time)):
            for j in range(len(order_time)):
                try:
                    i_time = int(order_time[i])
                    j_time = int(order_time[j])

                    if abs(int(i_time) - int(j_time)) == 1:
                        if order[i] in ['ch', 'ma'] and order[j] in ['hi','ph']:
                            return False
                        if order[j] in ['ch', 'ma'] and order[i] in ['hi','ph']:
                            return False
                except Exception as e:
                    pass

        try:
            if int(order_time[order.index('ch')]) % 2 == 0:
                return False
        except Exception as e:
            pass
        try:
            if int(order_time[ order.index('hi')]) not in [2, 4]:
                return False
        except Exception as e:
            pass
        try:
            if int(order_time[order.index('ph')]) not in [5, 7]:
                return False
        except Exception as e:
            pass

        # work mornings or abends
        counter = 0
        length = 0
        for i in range(self.no):
            try:
                if int(order_time[i]) < 5:
                    counter -= 1
                else:
                    counter += 1
                length += 1
            except Exception as e:
                pass
        if counter not in [-length, length]:
            return False

        return True

    def run_full_backtrack(self):

        self.D = {'subject0':['ma', 'ch', 'ph', 'hi'], 'time0':['1','2','3','4','5','6','7','8'],
                'subject1':['ma', 'ch', 'ph', 'hi'], 'time1':['1','2','3','4','5','6','7','8'],
                'subject2':['ma', 'ch', 'ph', 'hi'], 'time2':['1','2','3','4','5','6','7','8'],
                }
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
            adable = [ [el['subject0'], el['time0']], [el['subject1'], el['time1']], [el['subject2'], el['time2']] ]
            adable.sort(key= lambda x: x[1], reverse = False)

            if adable not in unique_solutions:
                unique_solutions.append(adable)

        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(unique_solutions))
        for el in unique_solutions:
            print(el)

    def run_nc_backtrack(self):

        self.D = {'subject0':['ma', 'ch', 'ph', 'hi'], 'time0':['1','2','3','4','5','6','7','8'],
                'subject1':['ma', 'ch', 'ph', 'hi'], 'time1':['1','2','3','4','5','6','7','8'],
                'subject2':['ma', 'ch', 'ph', 'hi'], 'time2':['1','2','3','4','5','6','7','8'],
                }
        var = ['subject','time']


        self.no = 3
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v + str(i)] = None
        print(self.variables)
        self.results = []

        self.total_counter = 0
        self.permutation_nc()

        unique_solutions = []
        for el in self.results:
            adable = [ [el['subject0'], el['time0']], [el['subject1'], el['time1']], [el['subject2'], el['time2']] ]
            adable.sort(key= lambda x: x[1], reverse = False)

            if adable not in unique_solutions:
                unique_solutions.append(adable)

        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(unique_solutions))
        for el in unique_solutions:
            print(el)


    def ac3(self):

        for a in self.D.keys():
            for var_a in self.D[a]:
                to_delete = True

                for b in self.D.keys():
                    if a != b:
                        for var_b in self.D[b]:
                            self.variables[a] = var_a
                            self.variables[b] = var_b

                            order = []
                            order_time = []
                            for i in range(self.no):
                                order.append(self.variables["subject" + str(i)])
                                order_time.append(self.variables["time" + str(i)])

                            if self.constraints_ac(order, order_time) is True:
                                to_delete = False

                            self.variables[a] = None
                            self.variables[b] = None
                if to_delete:
                    self.D[a].remove(var_a)
                    print("Fake: ", var_a, "_",a)


    def run_ac_backtrack(self):

        self.D = {'subject0':['ma', 'ch', 'ph', 'hi'], 'time0':['1','2','3','4','5','6','7','8'],
                'subject1':['ma', 'ch', 'ph', 'hi'], 'time1':['1','2','3','4','5','6','7','8'],
                'subject2':['ma', 'ch', 'ph', 'hi'], 'time2':['1','2','3','4','5','6','7','8'],
                }
        var = ['subject','time']


        self.no = 3
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v + str(i)] = None
        print(self.variables)
        self.results = []

        self.total_counter = 0
        self.ac3()

        self.variables = {}
        for i in self.D.keys():
            self.variables[i] = None

        print(self.D)

        self.permutation()

        unique_solutions = []
        for el in self.results:
            adable = [ [el['subject0'], el['time0']], [el['subject1'], el['time1']], [el['subject2'], el['time2']] ]
            adable.sort(key= lambda x: x[1], reverse = False)

            if adable not in unique_solutions:
                unique_solutions.append(adable)

        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(unique_solutions))
        for el in unique_solutions:
            print(el)


    def print_graph(self):
        G = nx.Graph()
        # Add nodes
        for node in self.variables.keys():
            G.add_node(node)


        G.add_edge("time0","subject0")
        G.add_edge("time0","subject1")
        G.add_edge("time0","subject2")
        G.add_edge("time1","subject0")
        G.add_edge("time1","subject1")
        G.add_edge("time1","subject2")
        G.add_edge("time2","subject0")
        G.add_edge("time2","subject1")
        G.add_edge("time2","subject2")
        G.add_edge("time0","time1")
        G.add_edge("time1","time2")


        nx.draw(G, with_labels=True)
        plt.savefig('labels_schedule2.png')


    def iterative_broadening(self):
        if None not in self.variables.values():
            # print(self.variables)
            self.results.append(deepcopy(self.variables))

            # if str(self.variables2) == str(self.variables):
            #     print("EQUAL")
            return

        var = self.find_unused_var()
        # print(var)
        domain = self.D[var]

        self.memory_history.append([domain])
        counted_attempts = 0
        max_attempts = len(domain)

        self.iterations += 1
        while counted_attempts < max_attempts and len(domain) > counted_attempts:
            value = domain[counted_attempts]

            self.memory_history.append([value])
            counted_attempts += 1
            save = deepcopy(self.variables)

            self.memory_history.append([save])
            self.variables[var] = value

            self.total_counter += 1
            print(self.variables)
            if self.constraints() and self.nu_constraints():
                print("True")
                self.iterative_broadening()
            else:
                print("False")

            # self.D[var].insert(-1,value)
            self.variables[var] = None
            #
            self.variables = save


    def run_iterative_broadening(self):

        self.D = {'subject0':['ma', 'ch', 'ph', 'hi'], 'time0':['1','2','3','4','5','6','7','8'],
                'subject1':['ma', 'ch', 'ph', 'hi'], 'time1':['1','2','3','4','5','6','7','8'],
                'subject2':['ma', 'ch', 'ph', 'hi'], 'time2':['1','2','3','4','5','6','7','8'],
                }
        var = ['subject','time']


        self.no = 3
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v + str(i)] = None
        print(self.variables)
        self.results = []

        self.total_counter = 0
        self.iterative_broadening()

        unique_solutions = []
        for el in self.results:
            adable = [ [el['subject0'], el['time0']], [el['subject1'], el['time1']], [el['subject2'], el['time2']] ]
            adable.sort(key= lambda x: x[1], reverse = False)

            if adable not in unique_solutions:
                unique_solutions.append(adable)

        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(unique_solutions))
        for el in unique_solutions:
            print(el)


import time
@profile
def main():
    time.sleep(0.2)
    times = []
    runtimes = 1
    for i in range(runtimes):

        start_time = time.time()
        solver = ScheduleSolver()
        # solver.run_full_backtrack()
        solver.run_nc_backtrack()
        # solver.run_ac_backtrack()
        # solver.run_iterative_broadening()


        end_time = time.time()
        print("Time that it took to run everythink: ", end_time-start_time)
        times.append(end_time - start_time)
        time.sleep(1)

        print("Iterations:",solver.iterations, " | Constraints: ", solver.total_counter)
        print("We got size consumption for the algorithm of: ", getsizeof(solver.memory_history))
    print("We got an average runtime of:", sum(times) / runtimes, " with a max of: ", max(times), " and a min of: ",
          min(times))

    # solver.print_graph()
main()
