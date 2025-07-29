import re, sys
import numpy as np
import mpmath as mp
from tablegen import constants

class TETER:
    
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

        self.CHARGES = constants.TETER_CHARGES

        self.COEFFS = dict()

        visited = list()
        for spec1 in self.SPECIES:
            for spec2 in self.SPECIES:
                pair_name = self.get_pair_name(spec1, spec2)
                if (pair_name not in visited) and (pair_name is not None):
                    visited.append(pair_name)
                    self.COEFFS[pair_name] = constants.TETER_coeffs[pair_name]

        print("Charges:\n")
        for spec in self.SPECIES:
            if spec in self.CHARGES:
                print(spec, ":", self.CHARGES[spec])


        self.CUTOFF = mp.mpf(args.cutoff)
        self.DATAPOINTS = args.data_points

    def get_pair_name(self, spec1, spec2):
        for attempt in (f"{spec1}-{spec2}", f"{spec2}-{spec1}"):
            if attempt in constants.TETER_coeffs:
                return attempt

        return None


    def get_force(self, A, B, C, D, rho, n, r_0, r):
        A =   mp.mpf(A)
        B =   mp.mpf(B)
        C =   mp.mpf(C)
        D =   mp.mpf(D)
        rho = mp.mpf(rho)
        n =   mp.mpf(n)
        r_0 = mp.mpf(r_0)
        r =   mp.mpf(r)

        if r <= r_0:
            return B * n * mp.power(r, -n - 1) - 2 * D * r
        else:
            return (A / rho) * mp.exp(-r / rho) - 6 * C * mp.power(r, -7)


    def get_pot(self, A, B, C, D, rho, n, r_0, r):
        A =   mp.mpf(A)
        B =   mp.mpf(B)
        C =   mp.mpf(C)
        D =   mp.mpf(D)
        rho = mp.mpf(rho)
        n =   mp.mpf(n)
        r_0 = mp.mpf(r_0)
        r =   mp.mpf(r)

        if r <= r_0:
            return B * mp.power(r, -n) + D * mp.power(r, 2)
        else:
            return A * mp.exp(-r / rho) - C * mp.power(r, -6)


    def eval_force(self, spec1, spec2, r):
        pair_name = self.get_pair_name(spec1, spec2)
        return float(self.get_force(*self.COEFFS[pair_name], r))

    def eval_pot(self, spec1, spec2, r):
        pair_name = self.get_pair_name(spec1, spec2)
        return float(self.get_pot(*self.COEFFS[pair_name], r))

    def no_spec_msg(self, spec1, spec2):
        return f"No {spec1}-{spec2} interaction is specified by Teter potentials.\n One should use Coulombic interactions."

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
