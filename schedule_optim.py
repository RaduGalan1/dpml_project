from sys import getsizeof

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
from memory_profiler import profile

#
# def permute(a, l, r):
#     if l == r:
#         print(a)
#     else:
#         for i in range(l, r + 1):
#             a[l], a[i] = a[i], a[l]
#             permute(a, l + 1, r)
#             a[l], a[i] = a[i], a[l]  # backtrack

class ScheduleSolver():
    def __init__(self):
        self.memory_history = []
        self.subject_domain_variables = {"ma": "Math", "ch": "Chemistry", "ph": "philosophy", "hi": "History"}  # D-all
        self.time_domain_variables = { "1": "1", "2": "2", "3": "3","4": "4", "5": "5", "6": "6", "7": "7","8": "8",}  # D-all
        self.constraints = {}
        self.total_counter = 0
        self.iterations = 0


    def permutation(self, lst,place):

        if len(lst) == 0:
            return []

        if len(lst) == 1:
            return [lst]

        l = []
        self.iterations += 1
        for i in range(len(lst)):
            m = lst[i]

            remLst = lst[:i] + lst[i + 1:]
            self.memory_history.append((remLst))

            for p in self.permutation(remLst,place-1):
                l.append([m] + p)
        return l

    def check_constraints(self,perm):
        is_correct = True
        self.total_counter += 1
        # [['8', 'hi'], ['7', 'ph'], ['6', 'ch']]
        for el in perm:
            if el[1] == 'ch':
                if int(el[0]) % 2 == 0:
                    is_correct = False
            if el[1] == 'hi':
                if int(el[0]) not in [2,4]:
                    is_correct = False
            if el[1] == 'ph':
                if int(el[0]) not in [5,7]:
                    is_correct = False

        for i in range(1,len(perm)):
            if abs(int(perm[i][0]) - int(perm[i-1][0])) == 1:
                if perm[i][1] in ['ch', 'ma'] and perm[i-1][1] in ['hi','ph']:
                    return False
                if perm[i-1][1] in ['ch', 'ma'] and perm[i][1] in ['hi','ph']:
                    return False
        if int(perm[0][0]) == 1:
            return False

        sum = 0
        for el in perm:
            if int(el[0]) > 4:
                sum += 1
            else:
                sum -= 1
        if sum not in [-3,3]:
            return False

        return is_correct

    def run_simple_backtrack(self):

        a = list(self.subject_domain_variables.keys())
        b = list(self.time_domain_variables.keys())
        a_combos = self.permutation(a,0)
        a_combos = [x[:3] for x in a_combos]
        a_final = []
        for el in a_combos:
            if el not in a_final:
                a_final.append(el)
        # print(len(a_final))

        b_combos = self.permutation(b,0)
        b_combos = [x[:3] for x in b_combos]
        b_final = []
        for el in b_combos:
            if el not in b_final:
                b_final.append(el)
        # print(len(b_final))

        results = []
        for el1 in b_final:
            for el2 in a_final:
                choice = [[el1[i],el2[i]] for i in range(3)]
                choice.sort(key=lambda x: int(x[0]), reverse=False)
                if choice not in results:
                    results.append(choice)

        # print(results)


        solutions = []
        for p in results:
            if self.check_constraints(p):
                print("_" * 6, p)
                solutions.append(p)
        print("We got total steps: ", self.total_counter)
        print("We got total choices: ", len(results))
        print("We got solutions: ", len(solutions))




@profile
def main():
    time.sleep(0.2)
    times = []
    runtimes = 1
    for i in range(runtimes):

        start_time = time.time()
        solver = ScheduleSolver()
        solver.run_simple_backtrack()

        end_time = time.time()
        print("Time that it took to run everythink: ", end_time - start_time)
        times.append(end_time - start_time)
        time.sleep(1)
        print("Iterations:", solver.iterations, " | Constraints: ", solver.total_counter)

        print("We got size consumption for the algorithm of: ", getsizeof(solver.memory_history))
    print("We got an average runtime of:", sum(times) / runtimes, " with a max of: ", max(times), " and a min of: ",
          min(times))

main()
