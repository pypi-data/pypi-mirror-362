"""
Factors class.
"""


class Factors():
    """
    Helper for doing a bunch of operations on Factors.

    Parameters:
        factors: list[Factor]
    """

    def __init__(self, factors):
        self.factors = factors

    def __iter__(self):
        for factor in self.factors:
            yield factor

    def __repr__(self):
        return f"Factors(\n{self.factors})"

    def __len__(self):
        return len(self.factors)

    def __getitem__(self, item):
        return self.factors[item]

    def append(self, factor):
        """
        Append a factor.

        Parameters:
            factor: Factor
        """
        self.factors.append(factor)

    def filter(self, filt):
        """
        Filter the factors.
        """

        new_factors = []
        for f in self.factors:
            new_factors.append(f.filter(filt))

        return Factors(new_factors)

    def prod(self):
        """
        Multiply set of factors
        """
        factor_prod = None

        for factor in self.factors:
            if factor_prod is None:
                factor_prod = factor
            else:
                factor_prod = factor_prod.prod(factor)

        return factor_prod

    def get_variables(self):
        """
        Return set of variables.

        Returns: set[string]
        """
        variables = set({})

        for factor in self.factors:
            get_vars = factor.get_variables()
            variables = variables.union(get_vars)

        return variables

    def remove(self, factor):
        """
        Remove a factor.
        """
        self.factors.remove(factor)
