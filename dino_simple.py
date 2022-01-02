from copy import deepcopy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from memory_profiler import profile
from sys import getsizeof


class DinoSolver():
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
            if var[:-1] != 'vegan':
                self.D[var].remove(d_orig)
            # print(self.variables)
            # print(self.D)
            # print("____")
            if self.constraints() and self.nu_constraints():
                self.permutation()
            self.variables[var] = None

            if var[:-1] != 'vegan':
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
            order_size = []
            order_vegan = []
            for i in range(self.no):
                order.append(self.variables["dino" + str(i)])
                order_size.append(self.variables["size" + str(i)])
                order_vegan.append(self.variables["vegan" + str(i)])
            if (self.constraints(order, order_size,order_vegan) and self.nu_constraints(order, order_size,order_vegan)) is False:
                add_back.append(value)
                self.D[var].remove(value)

        self.variables[var] = None


        self.iterations += 1
        for d_orig in self.D[var]:
            d = deepcopy(d_orig)

            self.memory_history.append([d])
            self.variables[var] = d
            if var[:-1] != 'vegan':
                self.D[var].remove(d_orig)
            if self.constraints() and self.nu_constraints():
                self.permutation_nc()
            self.variables[var] = None
            if var[:-1] != 'vegan':
                self.D[var].append(d)

        for el in add_back:
            self.D[var].append(el)


    def permutation_ac(self):

        if None not in self.variables.values():
            # print(self.variables)
            self.results.append(deepcopy(self.variables))

            # if str(self.variables2) == str(self.variables):
            #     print("EQUAL")
            return

        self.iterations += 1
        var = self.find_unused_var()
        for d_orig in self.D[var]:
            d = deepcopy(d_orig)
            self.variables[var] = d

            self.memory_history.append([d])
            if var[:-1] != 'vegan':
                self.D[var].remove(d_orig)
            # print(self.variables)
            # print(self.D)
            # print("____")
            if self.constraints() and self.nu_constraints():
                self.permutation()
            self.variables[var] = None

            if var[:-1] != 'vegan':
                self.D[var].append(d)

    def nu_constraints(self,order = None, order_size = None, order_vegan = None):

        if order is None and order_size is None and order_vegan is None:
            order =[]
            order_size = []
            order_vegan = []
            for i in range(self.no):
                if self.variables["dino" + str(i)] is not None and self.variables["dino" + str(i)] in order:
                    return False
                if self.variables["size" + str(i)] is not None and self.variables["size" + str(i)] in order_size:
                    return False
                order.append(self.variables["dino" + str(i)])
                order_size.append(self.variables["size" + str(i)])
        else:
            order_check = []
            order_size_check = []
            for i in range(self.no):
                if self.variables["dino" + str(i)] is not None and self.variables["dino" + str(i)] in order_check:
                    return False
                if self.variables["size" + str(i)] is not None and self.variables["size" + str(i)] in order_size_check:
                    return False
                order_check.append(self.variables["dino" + str(i)])
                order_size_check.append(self.variables["size" + str(i)])
        return True



    def constraints(self,order = None, order_size = None, order_vegan = None):
        if order is None and order_size is None and order_vegan is None:
            order = []
            order_size = []
            order_vegan = []
            for i in range(self.no):
                order.append(self.variables["dino" + str(i)])
                order_size.append(self.variables["size" + str(i)])
                order_vegan.append(self.variables["vegan" + str(i)])

        self.memory_history.append([order, order_size, order_vegan])

        self.total_counter += 1
        if not( order_size[ int( self.countries['ch'])] in ['5', None] ):
            return False

        for el in range(5):
            if order[ el] == 'he':
                if not(order_size[ int(el)] in ['1', None]):
                    return False

        me_no = ''
        ha_no = ''
        eu_no = ''
        for el in range(5):
            if order[ el] == 'me':
                me_no = str(el)
            elif order[ el] == 'ha':
                ha_no = str(el)
            elif order[ el] == 'eu':
                eu_no = str(el)
        if me_no != '' and ha_no != '' and eu_no != '' and order_size[ int(me_no)] is not None and order_size[ int(eu_no)] is not None and order_size[ int(ha_no)] is not None:
            if int(order_size[int(me_no)]) < int(order_size[ int(ha_no)]) :
                return False
            if int(order_size[ int(me_no)]) < int(order_size[ int(eu_no)]):
                return False


        if not( order_vegan[int(self.countries['ch'])] in ['y', None]) or not(order_vegan[ int(self.countries['us'])] in ['y', None])  or not(order_vegan[ int(self.countries['ca'])] in ['y', None] ):
            return False

        if me_no != '' and order_vegan[int(me_no)] in ['y']:
            return False

        if not( order[ int(self.countries['ca'])] in ['eu', None] or order[ int(self.countries['us'])] in ['eu', None] ):
            return False

        if not( order[ int(self.countries['ar'])] in ['ha', None] or order[ int(self.countries['us'])] in ['ha', None] ):
            return False
        #


        # if order[ int(self.countries['ch'])] in ['he', None] or order[ int(self.countries['ca'])] in ['he', None] or order[ int(self.countries['ch'])] in ['he', None]:
        #     return False

        if order[ int(self.countries['en'])] in ['he'] or order[ int(self.countries['ca'])] in ['he'] or order[ int(self.countries['us'])] in ['he']:
            # if self.variables['dino0']=='he':
            #     pass
            return False

        return True


    def constraints_ac(self,order = None, order_size = None, order_vegan = None):
        if order is None and order_size is None and order_vegan is None:
            order = []
            order_size = []
            order_vegan = []
            for i in range(self.no):
                order.append(self.variables["dino" + str(i)])
                order_size.append(self.variables["size" + str(i)])
                order_vegan.append(self.variables["vegan" + str(i)])
        self.memory_history.append([order, order_size, order_vegan])

        self.total_counter += 1
        if not( order_size[ int( self.countries['ch'])] in ['5', None] ):
            return False

        me_no = ''
        ha_no = ''
        eu_no = ''
        for el in range(5):
            if order[ el] == 'me':
                me_no = str(el)
            elif order[ el] == 'ha':
                ha_no = str(el)
            elif order[ el] == 'eu':
                eu_no = str(el)
        if me_no != '' and ha_no != '' and eu_no != '' and order_size[ int(me_no)] is not None and order_size[ int(eu_no)] is not None and order_size[ int(ha_no)] is not None:
            if int(order_size[int(me_no)]) < int(order_size[ int(ha_no)]) :
                return False
            if int(order_size[ int(me_no)]) < int(order_size[ int(eu_no)]) :
                return False


        if not( order_vegan[int(self.countries['ch'])] in ['y', None]) or not(order_vegan[ int(self.countries['us'])] in ['y', None])  or not(order_vegan[ int(self.countries['ca'])] in ['y', None] ):
            return False

        if me_no != '' and order_vegan[int(me_no)] in ['y']:
            return False

        if order[ int(self.countries['ca'])] in ['ha'] or order[ int(self.countries['ch'])] in ['ha'] or order[ int(self.countries['en'])] in ['ha']:
            return False



        if order[ int(self.countries['en'])] in ['he'] or order[ int(self.countries['ca'])] in ['he'] or order[ int(self.countries['us'])] in ['he']:
            # if self.variables['dino0']=='he':
            #     pass
            return False

        return True

    def run_full_backtrack(self):

        self.D = {'dino0':['eu', 'ha', 'he', 'me', 'nu'], 'size0':['1','2','3','4','5'],'vegan0':['n','y'],
                'dino1':['eu', 'ha', 'he', 'me', 'nu'], 'size1':['1','2','3','4','5'],'vegan1':['n','y'],
                'dino2':['eu', 'ha', 'he', 'me', 'nu'], 'size2':['1','2','3','4','5'],'vegan2':['n','y'],
                'dino3':['eu', 'ha', 'he', 'me', 'nu'], 'size3':['1','2','3','4','5'],'vegan3':['n','y'],
                'dino4':['eu', 'ha', 'he', 'me', 'nu'], 'size4':['1','2','3','4','5'],'vegan4':['n','y'],
                  }
        var = ['dino','size','vegan']
        self.countries = {'ar': '0', 'ca': '1', 'ch': '2', 'en': '3',
                          'us': '4'}


        self.no = 5
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v+str(i)] = None
        self.results = []

        self.total_counter = 0
        self.permutation()

        unique_solutions = []
        for el in self.results:
            adable = tuple([el['dino0'],el['dino1'],el['dino2'],el['dino3'],el['dino4']])
            unique_solutions.append(adable)
        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(set(unique_solutions)))
        for el in set(unique_solutions):
            res = []
            for i in range(len(el)):
                res.append(list(self.countries.keys())[i] + "-" + el[i])
            print(res)

    def run_nc_backtrack(self):


        self.D = {'dino0':['eu', 'ha', 'he', 'me', 'nu'], 'size0':['1','2','3','4','5'],'vegan0':['n','y'],
                'dino1':['eu', 'ha', 'he', 'me', 'nu'], 'size1':['1','2','3','4','5'],'vegan1':['n','y'],
                'dino2':['eu', 'ha', 'he', 'me', 'nu'], 'size2':['1','2','3','4','5'],'vegan2':['n','y'],
                'dino3':['eu', 'ha', 'he', 'me', 'nu'], 'size3':['1','2','3','4','5'],'vegan3':['n','y'],
                'dino4':['eu', 'ha', 'he', 'me', 'nu'], 'size4':['1','2','3','4','5'],'vegan4':['n','y'],
                  }
        self.countries = {'ar': '0', 'ca': '1', 'ch': '2', 'en': '3',
                          'us': '4'}


        self.no = 5
        self.variables = {}
        for i in self.D.keys():
            self.variables[i] = None
        print(self.variables )
        self.results = []

        self.total_counter = 0
        self.permutation_nc()

        unique_solutions = []
        for el in self.results:
            adable = tuple([el['dino0'],el['dino1'],el['dino2'],el['dino3'],el['dino4']])
            unique_solutions.append(adable)
        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(set(unique_solutions)))
        for el in set(unique_solutions):
            res = []
            for i in range(len(el)):
                res.append(list(self.countries.keys())[i] + "-" + el[i])
            print(res)

    def ac3(self):

        for a in self.D.keys():
            if a[:-1] != 'vegan':
                for var_a in self.D[a]:
                    to_delete = True

                    for b in self.D.keys():
                        if a != b and b[:-1] != 'vegan':
                            for var_b in self.D[b]:
                                self.variables[a] = var_a
                                self.variables[b] = var_b

                                order = []
                                order_size = []
                                order_vegan = []
                                for i in range(self.no):
                                    order.append(self.variables["dino" + str(i)])
                                    order_size.append(self.variables["size" + str(i)])
                                    order_vegan.append(self.variables["vegan" + str(i)])

                                if self.constraints_ac(order, order_size, order_vegan) is True:
                                    to_delete = False

                                self.variables[a] = None
                                self.variables[b] = None
                    if to_delete:
                        self.D[a].remove(var_a)
                        print("Fake: ", var_a, "_",a)

    def run_ac_backtrack(self):


        self.D = {'dino0':['eu', 'ha', 'he', 'me', 'nu'], 'size0':['1','2','3','4','5'],'vegan0':['n','y'],
                'dino1':['eu', 'ha', 'he', 'me', 'nu'], 'size1':['1','2','3','4','5'],'vegan1':['n','y'],
                'dino2':['eu', 'ha', 'he', 'me', 'nu'], 'size2':['1','2','3','4','5'],'vegan2':['n','y'],
                'dino3':['eu', 'ha', 'he', 'me', 'nu'], 'size3':['1','2','3','4','5'],'vegan3':['n','y'],
                'dino4':['eu', 'ha', 'he', 'me', 'nu'], 'size4':['1','2','3','4','5'],'vegan4':['n','y'],
                  }
        self.countries = {'ar': '0', 'ca': '1', 'ch': '2', 'en': '3',
                          'us': '4'}


        self.no = 5
        self.variables = {}
        for i in self.D.keys():
            self.variables[i] = None
        print(self.variables )
        self.results = []

        self.total_counter = 0
        self.ac3()

        self.variables = {}
        for i in self.D.keys():
            self.variables[i] = None

        print(self.D)
        self.permutation_ac()



        unique_solutions = []
        for el in self.results:
            adable = tuple([el['dino0'],el['dino1'],el['dino2'],el['dino3'],el['dino4']])
            unique_solutions.append(adable)
        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(set(unique_solutions)))
        for el in set(unique_solutions):
            res = []
            for i in range(len(el)):
                res.append(list(self.countries.keys())[i] + "-" + el[i])
            print(res)




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
        max_attempts = len(self.D[var])

        self.iterations += 1
        while counted_attempts < max_attempts and len(domain) > counted_attempts:
            value = domain[counted_attempts]
            counted_attempts += 1
            save = deepcopy(self.variables)

            self.memory_history.append([save])
            self.memory_history.append([value])
            self.variables[var] = value

            self.total_counter += 1
            # print(self.variables)
            if self.constraints() and self.nu_constraints():
                # print("True")
                self.iterative_broadening()
            else:
                # print("False")
                pass
            # self.D[var].insert(-1,value)
            self.variables[var] = None
            #
            self.variables = save


    def run_iterative_broadening(self):

        self.D = {'dino0':['eu', 'ha', 'he', 'me', 'nu'], 'size0':['1','2','3','4','5'],'vegan0':['n','y'],
                'dino1':['eu', 'ha', 'he', 'me', 'nu'], 'size1':['1','2','3','4','5'],'vegan1':['n','y'],
                'dino2':['eu', 'ha', 'he', 'me', 'nu'], 'size2':['1','2','3','4','5'],'vegan2':['n','y'],
                'dino3':['eu', 'ha', 'he', 'me', 'nu'], 'size3':['1','2','3','4','5'],'vegan3':['n','y'],
                'dino4':['eu', 'ha', 'he', 'me', 'nu'], 'size4':['1','2','3','4','5'],'vegan4':['n','y'],
                  }
        var = ['dino','size','vegan']
        self.countries = {'ar': '0', 'ca': '1', 'ch': '2', 'en': '3',
                          'us': '4'}


        self.no = 5
        self.variables = {}
        for i in range(self.no):
            for v in var:
                self.variables[v+str(i)] = None
        self.results = []

        self.total_counter = 0
        self.iterative_broadening()

        unique_solutions = []
        for el in self.results:
            adable = tuple([el['dino0'],el['dino1'],el['dino2'],el['dino3'],el['dino4']])
            unique_solutions.append(adable)
        print("We got steps: ", self.total_counter)
        print("We got solutions: ", len(self.results))
        print("We got uniques: ", len(set(unique_solutions)))
        for el in set(unique_solutions):
            res = []
            for i in range(len(el)):
                res.append(list(self.countries.keys())[i] + "-" + el[i])
            print(res)


    def print_graph(self):
        G = nx.Graph()
        # Add nodes
        for node in self.variables.keys():
            G.add_node(node)

        for el in range(5):
            G.add_edge("size"+str(el),"5")
            G.add_edge('dino' + str(el),'1')
        for el in range(5):

            for el2 in range(5):
                G.add_edge("dino" + str(el), "vegan" + str(el2))
                G.add_edge("dino" + str(el), "dino" + str(el2))
                G.add_edge('dino' + str(el),'size' + str(el2))


        nx.draw(G, with_labels=True)
        plt.savefig('labels2.png')



import time
@profile
def main():
    time.sleep(0.2)
    print("Solving with Chronological BackTracking")
    times = []
    runtimes = 1
    for i in range(runtimes):
        solver = DinoSolver()
        start_time = time.time()
        # solver.run_full_backtrack()
        # solver.run_nc_backtrack()
        # solver.run_ac_backtrack()
        solver.run_iterative_broadening()
        end_time = time.time()
        print("Time that it took to run everythink: ", end_time-start_time)
        times.append(end_time - start_time)
        time.sleep(1)

        print("Iterations:",solver.iterations, " | Constraints: ", solver.total_counter)
        print("We got size consumption for the algorithm of: ", getsizeof(solver.memory_history))
    print("We got an average runtime of:", sum(times)/runtimes, " with a max of: ",max(times), " and a min of: ",min(times))
    # solver.print_graph()
main()
