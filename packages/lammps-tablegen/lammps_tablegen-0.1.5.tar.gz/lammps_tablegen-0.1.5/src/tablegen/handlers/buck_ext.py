import re, sys
import numpy as np
import mpmath as mp
from tablegen import constants

class BUCK_EXT:
    
    def __init__(self, args):
        self.TABLENAME = args.table_name
        self.PLOT = args.plot

        self.TWO_BODY = True
        spec_set = set()
        self.all_pairs = list()

        for pair in args.pairs:
            spec_lst = re.sub(r'\s+', '', pair).split("-")
            if len(spec_lst) != 2:
                raise RuntimeError("Each pair should consist of exactly two atomic species.")
            spec_set.update(spec_lst)
            self.all_pairs.append(pair)
            self.all_pairs.append(f"{spec_lst[1]}-{spec_lst[0]}")

        self.SPECIES = sorted(list(spec_set))

        self.order_map = dict()
        for i, spec in enumerate(self.SPECIES):
            self.order_map[spec] = i

        self.COEFFS = dict()

        visited = list()
        print("Please provide extended Buckingham coefficients A, rho, C, and D for the following pairs:")
        for spec1 in self.SPECIES:
            for spec2 in self.SPECIES:
                pair_name = self.get_pair_name(spec1, spec2)
                if (pair_name not in visited) and (pair_name is not None):
                    visited.append(pair_name)
                    try:
                        A = float(input(f"({pair_name}) A: "))
                    except ValueError:
                        print("Buckingham coefficients should be numbers")
                        sys.exit()

                    try:
                        rho = float(input(f"({pair_name}) rho: "))
                    except ValueError:
                        print("Buckingham coefficients should be numbers")
                        sys.exit()

                    try:
                        C = float(input(f"({pair_name}) C: "))
                    except ValueError:
                        print("Buckingham coefficients should be numbers")
                        sys.exit()

                    try:
                        D = float(input(f"({pair_name}) D: "))
                    except ValueError:
                        print("Buckingham coefficients should be numbers")
                        sys.exit()

                    self.COEFFS[pair_name] = [A, rho, C, D]

        self.CUTOFF = mp.mpf(args.cutoff)
        self.DATAPOINTS = args.data_points

    def get_pair_name(self, spec1, spec2):
        if self.order_map[spec1] < self.order_map[spec2]:
            res = f"{spec1}-{spec2}"
        else:
            res = f"{spec2}-{spec1}"            

        if res in self.all_pairs:
            return res

    def get_force(self, A, rho, C, D, r):
        A = mp.mpf(A)
        rho = mp.mpf(rho)
        C = mp.mpf(C)
        D = mp.mpf(D)
        r = mp.mpf(r)
        if (not A) and (not C) and (not rho):
            rho = mp.mpf(1)
        rp = r / (43 * rho)
        return float((A / rho) * mp.exp(-r / rho) - 6 * C * r**-7 * (1 - mp.exp(-rp**6)) + (6 * C / (43**6 * rho**6)) * r**-1 * mp.exp(-rp**6) + 12 * D * r**-13)



    def get_pot(self, A, rho, C, D, r):
        A = mp.mpf(A)
        rho = mp.mpf(rho)
        C = mp.mpf(C)
        D = mp.mpf(D)
        r = mp.mpf(r)
        if (not A) and (not C) and (not rho):
            rho = mp.mpf(1)
        rp = r / (43 * rho)
        return float(A * mp.exp(-r / rho) - (C / r**6) * (1 - mp.exp(-rp**6)) + D / r**12)


    def eval_force(self, spec1, spec2, r):
        pair_name = self.get_pair_name(spec1, spec2)
        return self.get_force(*self.COEFFS[pair_name], r)

    def eval_pot(self, spec1, spec2, r):
        pair_name = self.get_pair_name(spec1, spec2)
        return self.get_pot(*self.COEFFS[pair_name], r)

    def no_spec_msg(self, spec1, spec2):
        return ""

    def get_table_name(self):
        return self.TABLENAME

    def to_plot(self):
        return self.PLOT

    def get_cutoff(self):
        return float(self.CUTOFF)

    def get_datapoints(self):
        return self.DATAPOINTS

    def get_species(self):
        return self.SPECIES

    def is_2b(self):
        return self.TWO_BODY
