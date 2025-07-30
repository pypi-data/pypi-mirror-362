import numpy as np
from warnings import warn

try:
    from sympy import primerange

    found_sympy = True
except ImportError:
    found_sympy = False
    warn("Did not find SymPy, therefore use" +
            " home-made ``primerange`` function.")

MAX = 1e18


def _prime_range(a: int, b: int = None):
    """Return all prime numbers in [a, b).

    Args:
        a: ``int``
        b: ``int``, optional
            If b is ``None`` (default) consider interval [2, a).

    Returns:
        ``list``
    """
    if b is None:
        start, end = 2, a
    else:
        start, end = a, b
    out = []
    if start % 2 == 0:
        inc = 1
    else:
        inc = 2
    for x in range(start, end, inc):
        prime = True
        for y in range(2, int(np.sqrt(start)) + 1, 1):
            if x % y == 0:
                prime = False
                break
        if prime:
            out.append(x)
    return out


def check_compatibility(b, c, type):
    """Return if the parameters b, c of deformale butterfly
    ensure the monotonicity of the chain.

    Args:
        b, c: ``int``
            The parameters b and c.
        type: ``str``
            Takes three values {square, expanding, shrinking}
            corresponding to three type of monotonicity.

    Returns:
        ``bool``
    """
    if type == "square":
        return b == c
    elif type == "expanding":
        return b <= c
    elif type == "shrinking":
        return b >= c
    else:
        raise Exception(
            "type must be either 'square'," + " 'expanding' or 'shrinking'."
        )


def format_conversion(m, n, chainbc, weight, format: str = "abcd"):
    """Return a sequence of deformable butterfly factors
    using the infomation of b and c.

    Args:
        m, n: ``int``
            Size of the matrix.
        chainbc: ``list``
            A sequence of pairs (b,c).
        format: ``str``, optional
            Support 2 formats (a,b,c,d) ("abcd" is default)
            and (p,q,r,s,t).

    Returns:
        ``list``
    """
    a = 1
    d = m
    result = []
    # print(chainbc)
    for i in range(len(chainbc)):
        (b, c) = chainbc[i]
        d = d // b
        if format == "abcd":
            result.append((a, b * weight[i], c * weight[i + 1], d))
        elif format == "pqrst":
            result.append(
                (
                    a * b * d * weight[i],
                    a * c * d * weight[i + 1],
                    b * weight[i],
                    c * weight[i + 1],
                    d,
                )
            )
        elif format == "abcdpq":
            result.append((a, b, c, d, weight[i], weight[i + 1]))
        else:
            raise Exception("format must be either 'abcd',"
                            + " 'pqrst' or 'abcdpq'.")
        a = a * c
    return result


def factorize(n):
    """Return a dictionary storing all prime divisor
    of n with their corresponding powers.

    Args:
        n: ``int``

    Returns:
        ``dict``
    """
    if found_sympy:
        prime_ints = list(primerange(1, n + 1))
    else:
        prime_ints = _prime_range(1, n + 1)
    # print(n + 1)
    # print(prime_ints)
    result = {}
    index = 0
    while n > 1:
        if n % prime_ints[index] == 0:
            k = 0
            while n % prime_ints[index] == 0:
                n = n // prime_ints[index]
                k = k + 1
            result[prime_ints[index]] = k
        index = index + 1
    return result


def random_Euler_sum(n, k):
    """Return k nonnegative integers whose sum equals to n.

    Args:
        n: ``int``
            Target sum.
        k: ``int``
            Number of nonnegative integers.

    Returns:
        ``list``
    """
    result = [0] * k
    sample = np.random.randint(0, k, n)
    for i in sample:
        result[i] = result[i] + 1
    return result


def enumerate_Euler_sum(n, k):
    if k == 1:
        yield (n,)
        return

    for i in range(n + 1):
        for t in enumerate_Euler_sum(n - i, k - 1):
            yield (i,) + t


class DebflyGen:
    def __init__(self, m, n, r):
        self.m = m
        self.n = n
        self.rank = r
        self.divisor_m = []
        self.divisor_n = []
        # Calculate the set of divisor of m
        for i in range(1, m + 1):
            if m % i == 0:
                self.divisor_m.append(i)

        # Calculate the set of divisor of n
        for i in range(1, n + 1):
            if n % i == 0:
                self.divisor_n.append(i)

        self.dp_table = np.zeros((m + 1, n + 1))
        self.dp_table_temp = np.zeros((m + 1, n + 1))

    def random_debfly_chain(self, n_factors, format: str='abcd'):
        """Return an uniformly random deformable butterfly chain
        whose product is of size m x n has ``n_factors`` factors.

        Args:
            n_factors: ``int``
                The number of factors.
            format: ``str``, optional
                ``'abcd'`` is default.

        Returns:
            ``list``
        """
        decomp_m = factorize(self.m)
        decomp_n = factorize(self.n)
        b_chain = [1] * n_factors
        c_chain = [1] * n_factors
        weight = [1] + [self.rank] * (n_factors - 1) + [1]
        for divisor, powers in decomp_m.items():
            random_partition = random_Euler_sum(powers, n_factors)
            for i in range(len(b_chain)):
                b_chain[i] = b_chain[i] * (divisor ** random_partition[i])

        for divisor, powers in decomp_n.items():
            random_partition = random_Euler_sum(powers, n_factors)
            for i in range(len(c_chain)):
                c_chain[i] = c_chain[i] * (divisor ** random_partition[i])
        chainbc = [(b_chain[i], c_chain[i]) for i in range(n_factors)]
        return format_conversion(
            self.m, self.n, chainbc, weight, format=format
        )

#     @staticmethod
#     def enumeration_inner_chain(m, n_factors):
#         if m == 1:
#             return [[1] * n_factors]
#         f_divisors, f_powers = list(factorize(m).items())[0]
#         results = []
#         for f1 in enumerate_Euler_sum(f_powers, n_factors):
#             for f2 in DebflyGen.enumeration_inner_chain(
#                 m // (f_divisors**f_powers), n_factors
#             ):
#                 results.append([(f_divisors**a) * b
#                         for (a, b) in zip(f1, f2)])
#         return results

    # def enumeration_debfly_chain(self, n_factors, format="abcd"):
    #     results = []
    #     weight = [1] + [self.rank] * (n_factors - 1) + [1]
    #     chain_b = DebflyGen.enumeration_inner_chain(self.m, n_factors)
    #     chain_c = DebflyGen.enumeration_inner_chain(self.n, n_factors)
    #     for f1 in chain_b:
    #         for f2 in chain_c:
    #             results.append(
    #                 format_conversion(
    #                     self.m,
    #                     self.n,
    #                     list(zip(f1, f2)),
    #                     weight,
    #                     format=format,
    #                 )
    #             )
    #     return results

    def smallest_monotone_debfly_chain(self, n_factors, format: str = "abcd"):
        """Return a deformable butterfly chain whose product is of
        size m x n has n_factors factors.

        Args:
            n_factors: ``int``
                The number of factors.
            format: ``str``, optional
                "abcd" is default.
        """
        try:
            assert n_factors > 0
        except AssertionError:
            print("Need at least 1 factor in the function")
        memorization = {}

        weight = [self.rank] * (n_factors - 1) + [1]
        # Determine the monotonicity type
        if self.m == self.n:
            type = "square"
        elif self.m > self.n:
            type = "shrinking"
        else:
            type = "expanding"

        # Initialize the dynamic programming table
        for i in self.divisor_m:
            for j in self.divisor_n:
                if check_compatibility(i, j, type):
                    self.dp_table[i, j] = i * j * self.rank
                else:
                    self.dp_table[i, j] = MAX

        # Update the value in the dynamic programming table
        for k in range(n_factors - 1):
            for i in self.divisor_m:
                for j in self.divisor_n:
                    self.dp_table_temp[i, j] = MAX

            for i in self.divisor_m:
                for j in self.divisor_n:
                    for ii in self.divisor_m:
                        if i <= ii:
                            break
                        if i % ii != 0:
                            continue
                        for jj in self.divisor_n:
                            if j <= jj:
                                break
                            if j % jj != 0:
                                continue
                            if not check_compatibility(ii, jj, type):
                                continue
                            n_params_fact = (i * jj * weight[k]
                                               * weight[k + 1])
                            dp_tab = self.dp_table
                            if (
                                self.dp_table_temp[i, j]
                                > n_params_fact + jj * dp_tab[i // ii, j // jj]
                            ):
                                self.dp_table_temp[i, j] = (
                                    n_params_fact
                                    + jj * self.dp_table[i // ii, j // jj]
                                )
                                memorization[(i, j, k + 1)] = (ii, jj)
            self.dp_table = self.dp_table_temp * 1

        # Recover the parameterizations (b,c)
        k = n_factors - 1
        current_i = self.m
        current_j = self.n
        chainbc = []
        while k >= 0:
            if k == 0:
                chainbc.append((current_i, current_j))
                break
            i, j = memorization[(current_i, current_j, k)]
            chainbc.append((i, j))
            current_i = current_i // i
            current_j = current_j // j
            k = k - 1
        # print('chainbc', chainbc)
        return self.dp_table[self.m, self.n], format_conversion(
            self.m, self.n, chainbc, [1] + weight, format=format
        )


# def count_parameters(param_chain):
#     """Return number of parameters.

#     Args:
#         param_chain: ``tuple``
#             A generalized butterfly chain.

#     Returns:
#         Number of parameters (``int``).
#     """
#     assert len(param_chain) > 0
#     count = 0
#     for params in param_chain:
#         if len(params) == 4:
#             count += params[0] * params[1] * params[2] * params[3]
#         elif len(params) == 5:
#             count += params[0] * params[3]
#         else:
#             count += (
#                 params[0]
#                 * params[1]
#                 * params[2]
#                 * params[3]
#                 * params[4]
#                 * params[5]
#             )
#     return count


# def check_monotone(param_chain, rank):
#     """Decide if the chain is monotone
#     (defined as in the paper Deformable butterfly).

#     Args:
#         param_chain:
#             A generalized butterfly chain and the intended rank.
#         rank: ``int``
#             Expected rank.

#     Returns:
#         bool
#     """
#     assert len(param_chain) > 0
#     weight = [1] + [rank] * (len(param_chain) - 1) + [1]
#     if len(param_chain[0]) == 4:
#         m = param_chain[0][0] * param_chain[0][1] * param_chain[0][3]
#         n = param_chain[-1][0] * param_chain[-1][2] * param_chain[-1][3]
#     else:
#         m = param_chain[0][0]
#         n = param_chain[-1][1]

#     if m == n:
#         type = "square"
#     elif m > n:
#         type = "shrinking"
#     else:
#         type = "expanding"

#     for i in range(len(param_chain)):
#         if len(param_chain[i]) == 4:
#             b = param_chain[i][1] // weight[i]
#             c = param_chain[i][2] // weight[i + 1]
#             if not check_compatibility(b, c, type):
#                 return False
#         elif len(param_chain[i]) == 5:
#             b = param_chain[i][2] // weight[i]
#             c = param_chain[i][3] // weight[i + 1]
#             if not check_compatibility(b, c, type):
#                 return False
#         else:
#             if not check_compatibility(
#                 param_chain[i][1], param_chain[i][2], type
#             ):
#                 return False
#     return True
