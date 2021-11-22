
#
# def permute(a, l, r):
#     if l == r:
#         print(a)
#     else:
#         for i in range(l, r + 1):
#             a[l], a[i] = a[i], a[l]
#             permute(a, l + 1, r)
#             a[l], a[i] = a[i], a[l]  # backtrack

class DinoSolver():
    def __init__(self):
        self.dino_variables = {"eu": "Eucentrosaurus", "ha": "Hadrosaurus", "he": "Herrerasaurus", "me": "Megasaurus",
                          "nu": "Nuoerosaurus"}  # Z
        self.country_domain_objects = {"ar": "Argentina", "ca": "Canada", "ch": "China", "en": "England",
                                  "us": "USA"}  # D-all
        self.constraints = {}
        self.total_counter = 0

        self.dinos = ['eu', 'ha', 'he', 'me', 'nu']  # Solution
        print("Dinos:", self.dinos)

    def permutation(self, lst,place):

        if len(lst) == 0:
            return []

        if len(lst) == 1:
            return [lst]

        l = []

        for i in range(len(lst)):
            m = lst[i]

            remLst = lst[:i] + lst[i + 1:]

            for p in self.permutation(remLst,place-1):
                l.append([m] + p)
        return l

    def check_constraints(self,perm):
        is_correct = True
        self.total_counter += 1
        if not(perm[self.dinos.index('me')] == 'ch' or perm[self.dinos.index('nu')] == 'ch'):
            is_correct = False

        if not (perm[self.dinos.index('me')] == 'ar' or perm[self.dinos.index('me')] == 'en'):
            is_correct = False

        if not (perm[self.dinos.index('eu')] == 'us' or perm[self.dinos.index('eu')] == 'ca'):
            is_correct = False

        if not (perm[self.dinos.index('ha')] == 'ar' or perm[self.dinos.index('ha')] == 'us'):
            is_correct = False

        if perm[self.dinos.index('he')] == 'ca' or perm[self.dinos.index('he')] == 'us' or perm[self.dinos.index('he')] == 'en':
            is_correct = False

        return is_correct

    def run_simple_backtrack(self):

        a = list(self.country_domain_objects.keys())
        results = self.permutation(a,0)

        solutions = []
        for p in results:
            if self.check_constraints(p):
                for i in range(len(p)):
                    p[i]+="-"+self.dinos[i]

                print("_" * 6, p)
                solutions.append(p)
        print("We got total steps: ", self.total_counter)
        print("We got total choices: ", len(results))
        print("We got solutions: ", len(solutions))


import time
def main():
    time.sleep(2)
    solver = DinoSolver()
    solver.run_simple_backtrack()

main()
