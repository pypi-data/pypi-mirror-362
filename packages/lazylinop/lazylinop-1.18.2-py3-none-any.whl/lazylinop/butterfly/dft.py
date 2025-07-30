import numpy as np
from lazylinop.basicops import bitrev
from lazylinop.signal import fft
from lazylinop.butterfly.ksm import ksm, _multiple_ksm
from lazylinop.wip.butterfly.utils import clean


def _dft_square_dyadic_ks_values(N: int, dense: bool = False,
                                 dtype: str = 'complex64'):
    r"""
    Return a list of ``ks_values`` that corresponds
    to the ``F @ P.T`` matrix decomposition into
    ``n = int(np.log2(N))`` factors, where ``F`` is the DFT matrix
    and ``P`` the bit-reversal permutation matrix.
    The size $N=2^n$ of the DFT must be a power of $2$.

    We can draw the square-dyadic decomposition for $N=16$:

    .. image:: _static/square_dyadic.svg

    Args:
        N: ``int``
            DFT of size $N=2^n$.
        dense: ``bool``, optional
            If ``dense=True`` compute and return
            2d representation of the factors.
            Default value is ``False``.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        List of 4d ``np.ndarray`` corresponding to ``ks_values``.
        If ``dense=True`` it also returns a list of
        2d ``np.ndarray`` corresponding to the ``n = int(np.log2(N))`` factors.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly.dft import _dft_square_dyadic_ks_values
        >>> from lazylinop.butterfly import ksm
        >>> from lazylinop.signal import fft
        >>> from lazylinop.basicops import bitrev
        >>> N = 2 ** 7
        >>> ks_values = _dft_square_dyadic_ks_values(N)
        >>> x = np.random.randn(N)
        >>> L = ksm(ks_values)
        >>> P = bitrev(N)
        >>> np.allclose(fft(N) @ x, L @ P @ x)
        True

    References:
        - Learning Fast Algorithms for Linear Transforms Using Butterfly Factorizations.
          Dao T, Gu A, Eichhorn M, Rudra A, Re C.
          Proc Mach Learn Res. 2019 Jun;97:1517-1527. PMID: 31777847; PMCID: PMC6879380.
    """
    if not (((N & (N - 1)) == 0) and N > 0):
        raise ValueError("N must be a power of two.")
    inv_sqrt2 = 1.0 / np.sqrt(2.0)
    p = int(np.log2(N))
    if dense:
        factors = [None] * p
    ks_values = [None] * p
    for n in range(p):
        if n == (p - 1):
            f2 = (fft(2) @ np.eye(2)).astype(dtype)
            if dense:
                factors[n] = np.kron(np.eye(N // 2, dtype=dtype), f2)
            a = N // 2
            b, c = 2, 2
            d = 1
            ks_values[n] = np.empty((a, b, c, d), dtype=dtype)
            for i in range(a):
                ks_values[n][i, :, :, 0] = f2
        else:
            s = N // 2 ** (p - n)
            t = N // 2 ** (n + 1)
            w = np.exp(2.0j * np.pi / (2 * t))
            omega = (w ** (-np.arange(t))).astype(dtype)
            if dense:
                diag_omega = np.diag(omega)
                factors[n] = np.kron(
                    np.eye(s, dtype=dtype) * inv_sqrt2,
                    np.vstack((
                        np.hstack((np.eye(t, dtype=dtype), diag_omega)),
                        np.hstack((np.eye(t, dtype=dtype), -diag_omega)))))
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
                            # diag(omega).
                            sub_col = u + t
                            sub_row = u
                            tmp = omega[u] * inv_sqrt2
                        elif v == 2:
                            # Identity.
                            sub_col = u
                            sub_row = u + t
                            tmp = inv_sqrt2
                        else:
                            # -diag(omega)
                            sub_col = u + t
                            sub_row = u + t
                            tmp = -omega[u] * inv_sqrt2
                        j = sub_row // d
                        k = sub_col // d
                        ks_values[n][i, j, k, sub_col - k * d] = tmp
    if dense:
        return ks_values, factors
    else:
        return ks_values


def dft(N: int, backend: str = 'numpy', dtype: str = 'complex64'):
    r"""
    Return a :class:`LazyLinOp` `L` with the Butterfly structure
    corresponding to the Discrete-Fourier-Transform (DFT).

    Shape of ``L`` is $\left(N,~N\right)$ where
    $N=2^n$ must be a power of two.

    The number of factors $n$ of the square-dyadic decomposition
    is given by $n=\log_2\left(N\right)$

    Args:
        N: ``int``
            Size of the DFT. $N$ must be a power of two.
        backend: ``str``, ``tuple`` or ``pycuda.driver.Device``, optional
            See :py:func:`ksm` for more details.
        dtype: ``str``, optional
            It could be either ``'complex64'`` (default) or ``'complex128'``.

    Returns:
        :class:`LazyLinOp` `L` corresponding to the DFT.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.butterfly import dft as bdft
        >>> from lazylinop.signal import dft as sdft
        >>> N = 2 ** 7
        >>> x = np.random.randn(N).astype('float32')
        >>> y = bdft(N) @ x
        >>> z = sdft(N) @ x
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
    if dtype != 'complex64' and dtype != 'complex128':
        raise Exception("dtype must be either 'complex64' or 'complex128'.")

    ks_values = _dft_square_dyadic_ks_values(N, dtype=dtype)
    L = ksm(ks_values, backend='numpy')
    if backend in ('numpy', 'scipy'):
        F = ksm(L.ks_values, backend=backend) @ bitrev(N)
        F.ks_values = L.ks_values
    else:
        # FIXME: params=None.
        F = _multiple_ksm(L.ks_values, backend=backend,
                          params=None, perm=True)
        F.ks_values = L.ks_values
    clean(L)
    del L
    return F
