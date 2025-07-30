import numpy as np
from lazylinop.butterfly.ksm import ksm, _multiple_ksm
from lazylinop.butterfly.fuse import fuse
from lazylinop.wip.butterfly.utils import clean


def _hadamard_square_dyadic_ks_values(N: int, dense: bool = False,
                                      dtype: str = 'float64'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``H @ P.T`` matrix decomposition into
    ``n = int(np.log2(N))`` factors, where ``H`` is the Hadamard
    matrix and ``P`` the bit-reversal permutation matrix.
    The size $N=2^n$ of the Hadamard matrix must be a power of $2$.

    We can draw the square-dyadic decomposition for $N=16$:

    .. image:: _static/square_dyadic.svg

    Args:
        N: ``int``
            FWHT of size $N=2^n$.
        dense: ``bool``, optional
            If ``dense=True`` compute and return
            2d representation of the factors.
            Default value is ``False``.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.

    Returns:
        List of 4d ``np.ndarray`` corresponding to ``ks_values``.
        If ``dense=True`` it also returns a list of
        2d ``np.ndarray`` corresponding to the ``n = int(np.log2(N))`` factors.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly.hadamard import _hadamard_square_dyadic_ks_values
        >>> from lazylinop.butterfly import ksm
        >>> from lazylinop.signal import fwht
        >>> N = 2 ** 5
        >>> ks_values = _hadamard_square_dyadic_ks_values(N)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values)
        >>> np.allclose(fwht(N) @ x, (L @ x) / np.sqrt(N))
        True

    References:
        - Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
          Dao T, Gu A, Eichhorn M, Rudra A, Re C.
          Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    inv_sqrt2 = 1.0  # / np.sqrt(2.0)
    p = int(np.log2(N))
    if dense:
        factors = [None] * p
    ks_values = [None] * p
    for n in range(p):
        if n == (p - 1):
            h2 = (inv_sqrt2 * np.array([[1, 1], [1, -1]])).astype(dtype)
            if dense:
                factors[n] = np.kron(np.eye(N // 2, dtype=dtype), h2)
            a = N // 2
            b, c = 2, 2
            d = 1
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            for i in range(a):
                ks_values[n][i, :, :, 0] = h2
        else:
            s = N // 2 ** (p - n)
            t = N // 2 ** (n + 1)
            if dense:
                factors[n] = np.kron(
                    np.eye(s, dtype=dtype) * inv_sqrt2,
                    np.vstack((
                        np.hstack((np.eye(t, dtype=dtype),
                                   np.eye(t, dtype=dtype))),
                        np.hstack((np.eye(t, dtype=dtype),
                                   -np.eye(t, dtype=dtype))))))
            a = s
            b, c = 2, 2
            d = t
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            # Map between 2d and 4d representations.
            # col = i * c * d + k * d + l
            # row = i * b * d + j * d + l
            # Loop over the a blocks.
            for i in range(a):
                for u in range(t):
                    for v in range(4):
                        if v == 0:
                            # Identity.
                            sub_col = u
                            sub_row = u
                            tmp = inv_sqrt2
                        elif v == 1:
                            # Identity.
                            sub_col = u + t
                            sub_row = u
                            tmp = inv_sqrt2
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + t
                            tmp = inv_sqrt2
                        else:
                            # -Identity.
                            sub_col = u + t
                            sub_row = u + t
                            tmp = -inv_sqrt2
                        j = sub_row // d
                        k = sub_col // d
                        ks_values[n][i, j, k, sub_col - k * d] = tmp
    if dense:
        return ks_values, factors
    else:
        return ks_values


def fwht(N: int, backend: str = 'numpy', dtype: str = 'float64'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Fast-Walsh-Hadamard-Transform (FWHT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is orthogonal and *symmetric* and
    the inverse WHT operator is ``L.T = L``.

    The number of factors $n$ of the square-dyadic decomposition
    is given by $n=\log_2\left(N\right)$

    Args:
        N: ``int``
            Size of the FWHT. $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the FWHT.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly import fwht as bfwht
        >>> from lazylinop.signal import fwht as sfwht
        >>> N = 2 ** 5
        >>> x = np.random.randn(N).astype('float64')
        >>> y = bfwht(N) @ x
        >>> z = sfwht(N) @ x
        >>> np.allclose(y, z)
        True

    .. _dec:

        **References:**

        [1] Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
        Dao T, Gu A, Eichhorn M, Rudra A, Re C.
        Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    return hadamard(N, backend, dtype) / np.sqrt(N)


def hadamard(N: int, backend: str = 'numpy', dtype: str = 'float64'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Hadamard matrix.

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is orthogonal and *symmetric* and
    the inverse operator is ``L.T = L``.

    The number of factors $n$ of the square-dyadic decomposition
    is given by $n=\log_2\left(N\right)$

    Args:
        N: ``int``
            Size of the Hadamard matrix.
            $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the
        Hadamard matrix.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.butterfly import hadamard
        >>> N = 2 ** 5
        >>> x = np.random.randn(N).astype('float64')
        >>> y = hadamard(N) @ x
        >>> z = sp.linalg.hadamard(N) @ x
        >>> np.allclose(y, z)
        True

    .. _dec:

        **References:**

        [1] Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
        Dao T, Gu A, Eichhorn M, Rudra A, Re C.
        Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")

    ks_values = _hadamard_square_dyadic_ks_values(N, dtype=dtype)
    L = ksm(ks_values, backend='numpy')
    if backend in ('numpy', 'scipy'):
        H = ksm(L.ks_values, backend=backend)
    else:
        # FIXME: params=None.
        H = _multiple_ksm(L.ks_values, backend=backend,
                          params=None, perm=False)
    H.ks_values = L.ks_values
    clean(L)
    del L
    return H


def _fwht_helper(N: int, n_factors: int, backend: str = 'numpy',
                 strategy: str = 'memory', dtype: str = 'float64'):
    r"""
    Return a :class:`LazyLinOp` `L` corresponding to
    the Fast-Walsh-Hadamard-Transform (FWHT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    ``L`` is orthogonal and *symmetric* and
    the inverse WHT operator is ``L.T = L``.

    Args:
        N: ``int``
            FWHT of size $N$. $N$ must be a power of two.
        n_factors: ``int``
            Number of factors ``n_factors <= n``.
            If ``n_factors = n``, return the square-dyadic decomposition.
            The performance of the algorithm depends on
            the number of factors, the size of the FWHT
            as-well-as the strategy.
            Our experimentation shows that square-dyadic decomposition
            is always the worse choice.
            The best choice is two, three or four factors.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        strategy: ``str``, optional
            It could be:

            - ``'l2r'`` fuse from left to right.
            - ``balanced`` fuse from left to right and right to left ($n>3$).

              - Case ``n = 6`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5
                - step 1: 01 2 3 45
                - step 2: 012 345
              - Case ``n = 7`` and ``n_factors = 2``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
                - step 3: 0123 456
              - Case ``n = 7`` and ``n_factors = 3``:

                - step 0: 0 1 2 3 4 5 6
                - step 1: 01 2 3 4 56
                - step 2: 012 3 456
            - ``'memory'`` find the two consecutive ``ks_values`` that
              minimize the memory of the fused ``ks_values``.
              It is the default value.
            - ``'sparsity'`` find the two consecutive ``ks_values`` that
              minimize the ratio $\frac{1}{ad}$ of the fused ``ks_values``.
            - ``'speed'`` find the two consecutive ``ks_values`` that
              minimize the ratio $\frac{bc}{b+c}$ of the fused ``ks_values``.
        dtype: ``str``, optional
            The dtype of Hadamard matrix elements.
            The defaut value is 'float64'.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the FWHT.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    p = int(np.log2(N))
    if n_factors > p or n_factors < 1:
        raise ValueError("n_factors must be positive and less or"
                         + " equal to int(np.log2(N)).")

    # FIXME
    if n_factors == 7:
        params = None
    elif n_factors == 8:
        params = None
    elif n_factors == 9:
        params = None
    elif n_factors == 10:
        params = None
    elif n_factors == 11:
        params = None
    elif n_factors == 12:
        params = None
    elif n_factors == 13:
        params = None
    elif n_factors == 14:
        params = None
    else:
        params = None

    ks_values = _hadamard_square_dyadic_ks_values(N, dtype=dtype)
    if p == n_factors:
        # Nothing to fuse.
        L = ksm(ks_values, backend='numpy')
    else:
        tmp = [None] * (p // 2 + p % 2)
        m, target = p, p
        if strategy == 'l2r':
            # Fuse from left to right (in-place modification of ks_values).
            while True:
                for i in range(0, m - m % 2 - 1, 2):
                    if target > n_factors:
                        ks_values[i // 2] = fuse(ks_values[i],
                                                 ks_values[i + 1])
                        # ks_values[i // 2] = _fuse(ks_values[i],
                        #                           ks_values[i + 1],
                        #                           backend=backend)
                        target -= 1
                if target == n_factors:
                    break
                if m % 2 == 1:
                    ks_values[m // 2 + m % 2 - 1] = ks_values[m - 1]
                    # target -= 1
                if target == n_factors:
                    break
                m = m // 2 + m % 2
                target = m
            L = ksm(ks_values[:n_factors], backend='numpy')
        elif strategy == 'balanced':
            if p <= 3:
                raise Exception("strategy 'balanced' does" +
                                " not work when p <= 3.")
            # Fuse from left to right and from right to left.
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"      ", idx)
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    idx[lpos + 1] = idx[lpos] + idx[lpos + 1]
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    idx[rpos - 1] = idx[rpos - 1] + idx[rpos]
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m / 2:
                    lpos, rpos = n_left, m - 1 - n_right
                print(f"step={step}", idx[n_left:(p - n_right)])
                step += 1
                if target == n_factors:
                    break
            m, target = p, p
            lpos, rpos, n_left, n_right = 0, m - 1, 0, 0
            while True:
                if target > n_factors:
                    # From left to right.
                    ks_values[lpos + 1] = fuse(ks_values[lpos],
                                               ks_values[lpos + 1])
                    # ks_values[lpos + 1] = _fuse(ks_values[lpos],
                    #                             ks_values[lpos + 1],
                    #                             backend=backend)
                    target -= 1
                    lpos += 1
                    n_left += 1
                if target > n_factors:
                    # From right to left.
                    ks_values[rpos - 1] = fuse(ks_values[rpos - 1],
                                               ks_values[rpos])
                    # ks_values[rpos - 1] = _fuse(ks_values[rpos - 1],
                    #                             ks_values[rpos],
                    #                             backend=backend)
                    target -= 1
                    rpos -= 1
                    n_right += 1
                if lpos + 1 >= m // 2:
                    lpos, rpos = n_left, m - 1 - n_right
                if target == n_factors:
                    break
            L = ksm(ks_values[n_left:(n_left + n_factors)], backend='numpy')
        elif strategy in ('memory', 'speed', 'sparsity'):
            step = 0
            idx = [str(i) for i in range(p)]
            print(f"      ", idx)
            n_fuses = 0
            while True:
                # Build memory list.
                heuristic = np.full(p - n_fuses - 1, 0.0)
                memory = np.full(p - n_fuses - 1, 0)
                sparsity = np.full(p - n_fuses - 1, 0.0)
                for i in range(p - n_fuses - 1):
                    a1, b1, c1, d1 = ks_values[i].shape
                    a2, b2, c2, d2 = ks_values[i + 1].shape
                    b = (b1 * d1) // d2
                    c = (a2 * c2) // a1
                    memory[i] = a1 * b * c * d2
                    # Because of argmin, compute the inverse.
                    heuristic[i] = 1.0 / ((b + c) / (b * c))
                    sparsity[i] = 1.0 / (a1 * d2)
                # Find argmin.
                if strategy == 'memory':
                    # argmin = np.argmin(memory)
                    tmp = np.where(memory == memory[np.argmin(memory)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                elif strategy == 'speed':
                    # argmin = np.argmin(heuristic)
                    tmp = np.where(
                        heuristic == heuristic[np.argmin(heuristic)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                elif strategy == 'sparsity':
                    # argmin = np.argmin(sparsity)
                    tmp = np.where(
                        sparsity == sparsity[np.argmin(sparsity)])[0]
                    if n_fuses % 2 == 0:
                        argmin = tmp[0]
                    else:
                        argmin = tmp[-1]
                # Fuse argmin and argmin + 1.
                ks_values[argmin] = fuse(ks_values[argmin],
                                         ks_values[argmin + 1])
                # ks_values[argmin] = _fuse(ks_values[argmin],
                #                           ks_values[argmin + 1],
                #                           backend=backend)
                idx[argmin] = idx[argmin] + idx[argmin + 1]
                n_fuses += 1
                # Delete argmin + 1.
                ks_values.pop(argmin + 1)
                idx.pop(argmin + 1)
                target -= 1
                print(f"step={step}", idx)
                step += 1
                if target == n_factors:
                    break
            L = ksm(ks_values, backend='numpy')
        else:
            raise Exception("strategy must be either 'l2r'," +
                            " 'balanced', 'memory', 'sparsity'" +
                            " or 'speed'.")

    if backend in ('numpy', 'scipy'):
        H = ksm(L.ks_values, backend=backend)
        H.ks_values = L.ks_values
    else:
        H = _multiple_ksm(L.ks_values, backend=backend,
                          params=params, perm=False)
        H.ks_values = L.ks_values
    clean(L)
    del L
    return H / np.sqrt(N)
