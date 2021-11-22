from copy import deepcopy


class DinoSolver():
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
            if var[:-1] != 'vegan':
                self.D[var[:-1]].remove(d_orig)
            if self.constraints():
                self.permutation()
            self.variables[var] = None
            if var[:-1] != 'vegan':
                self.D[var[:-1]].append(d)

    def constraints(self):
        self.total_counter += 1
        if not( self.variables['size' + self.countries['ch']] in ['5', None] ):
            return False

        for el in range(5):
            if self.variables['dino' + str(el)] == 'he':
                if not(self.variables['size' + str(el)] in ['1', None]):
                    return False

        me_no = ''
        ha_no = ''
        eu_no = ''
        for el in range(5):
            if self.variables['dino' + str(el)] == 'me':
                me_no = str(el)
            elif self.variables['dino' + str(el)] == 'ha':
                ha_no = str(el)
            elif self.variables['dino' + str(el)] == 'eu':
                eu_no = str(el)
        if me_no != '' and ha_no != '' and eu_no != '' and self.variables['size' + me_no] is not None and self.variables['size' + eu_no] is not None and self.variables['size' + ha_no] is not None:
            if int(self.variables['size' + me_no]) < int(self.variables['size' + ha_no]):
                return False
            if int(self.variables['size' + me_no]) < int(self.variables['size' + eu_no]):
                return False


        if not( self.variables['vegan' + self.countries['ch']] in ['y', None]) or not(self.variables['vegan' + self.countries['us']] in ['y', None])  or not(self.variables['vegan' + self.countries['ca']] in ['y', None] ):
            return False

        if me_no != '' and self.variables['vegan' + me_no] in ['y']:
            return False

        if not( self.variables['dino' + self.countries['ca']] in ['eu', None] or self.variables['dino' + self.countries['us']] in ['eu', None] ):
            return False

        if not( self.variables['dino' + self.countries['ar']] in ['ha', None] or self.variables['dino' + self.countries['us']] in ['ha', None] ):
            return False
        #


        # if self.variables['dino' + self.countries['ch']] in ['he', None] or self.variables['dino' + self.countries['ca']] in ['he', None] or self.variables['dino' + self.countries['ch']] in ['he', None]:
        #     return False

        if self.variables['dino' + self.countries['en']] in ['he'] or self.variables['dino' + self.countries['ca']] in ['he'] or self.variables['dino' + self.countries['us']] in ['he']:
            # if self.variables['dino0']=='he':
            #     pass
            return False

        return True

    def run_full_backtrack(self):

        self.D = {'dino':['eu', 'ha', 'he', 'me', 'nu'], 'size':['1','2','3','4','5'],'vegan':['n','y']}
        var = ['dino','size','vegan']
        self.countries = {'ar': '0', 'ca': '1', 'ch': '2', 'en': '3',
                          'us': '4'}


        no = 5
        self.variables = {}
        for i in range(no):
            for v in var:
                self.variables[v+str(i)] = None
        self.results = []

        # self.variables2 = {}
        # self.variables2['dino0']= 'me'
        # self.variables2['dino1']= 'eu'
        # self.variables2['dino2']= 'nu'
        # self.variables2['dino3']= 'he'
        # self.variables2['dino4']= 'ha'
        #
        # self.variables2['vegan0']= 'n'
        # self.variables2['vegan1']= 'y'
        # self.variables2['vegan2']= 'y'
        # self.variables2['vegan3']= 'y'
        # self.variables2['vegan4']= 'y'
        #
        # self.variables2['size0']= '4'
        # self.variables2['size1']= '3'
        # self.variables2['size2']= '5'
        # self.variables2['size3']= '1'
        # self.variables2['size4']= '2'
        # print(self.constraints())
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

import time
def main():
    time.sleep(2)
    solver = DinoSolver()
    solver.run_full_backtrack()

main()
