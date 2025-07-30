import numpy as np
from lazylinop import LazyLinOp, aslazylinop
from lazylinop.basicops import hstack, vstack, eye, kron, ones, zeros, anti_eye
from warnings import warn
import array_api_compat
from array_api_compat import is_torch_array, is_cupy_array
try:
    import torch
except ModuleNotFoundError:
    torch = None
import sys
sys.setrecursionlimit(100000)


def pad(op, pad_width, mode='constant', constant_values=0):
    """
    Returns a :class:`.LazyLinOp` ``L`` that acts as a padded version
    of a given compatible linear operator ``op``.

    Args:
        op: (``scipy LinearOperator``, ``LazyLinOperator``, ``numpy array``, ``torch.Tensor``)
            The operator/array to pad.

        pad_width: (``tuple``, ``list``)
            Number of values padded to the edges of each axis.

            - ``((B0, A0), (B1, A1))`` (See Figure `Padding format`).
            - ``(B, A)`` is equivalent to ``((B, A), (B, A))``.
            - ``((B0, ), (B1, ))`` is equivalent to ``((B0, B0), (B1, B1))``.
            - ``(B, )`` is equivalent to ``((B, B), (B, B))``.
            - ``C`` is equivalent to ``((C, C), (C, C))``.

        mode: (``str``)
            - ``'constant'``:
                Pads with a constant value.
            - ``'symmetric'``:
                Pads with the reflection of the vector mirrored along the edge
                of the array.
            - ``'antisymmetric'``:
                Pads with the reflection of the vector mirrored and negated
                along the edge of the array.
            - ``'reflect'``:
                Pads with the reflection of the vector mirrored on the first
                and last values of the vector along each axis.
            - ``'mean'``:
                Pads with the mean value of all the vector along each axis.
            - ``'edge'``:
                Pads with the edge values of :class:`.LazyLinOp`.
            - ``'wrap'``:
                Pads with the wrap of the vector along the axis.
                The first values are used to pad the end and the end values
                are used to pad the beginning.
        constant_values: (``tuple``, ``list``, ``scalar``)
            The padded values for each axis (in ``mode='constant'``).

            - ``((VB0, VA0)``, ``(VB1, VA1))``: padding values before (``VBi``)
              and values after (``VAi``) on each dimension.
              In Figure `Padding format` value ``VBi`` (resp. ``VAi``) goes
              where padding width ``Bi`` (resp.  ``Ai``) is.
            - ``((VB0, VA0))`` is equivalent to ``((VB0, VA0), (VB0, VA0))``.
            - ``(V,)`` or ``V`` is equivalent to ``((V, V), (V, V))``.
            - ``((VB0,), (VB1,))`` is equivalent to
              ``((VB0, VB0), (VB1, VB1))``.

    .. _padding_format
    Padding format (for an operator ``op``)
    --------------
        .. image:: _static/pad_width.svg
            :width: 400px
            :height: 400px

    Example ``mode='constant'``:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> A = np.arange(18 * 2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lpA = lz.pad(A, (2, 3))
        >>> lpA
        <23x7 LazyLinOp with unspecified dtype>
        >>> lpA.toarray().astype(int)
        array([[ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  1,  0,  0,  0],
               [ 0,  0,  2,  3,  0,  0,  0],
               [ 0,  0,  4,  5,  0,  0,  0],
               [ 0,  0,  6,  7,  0,  0,  0],
               [ 0,  0,  8,  9,  0,  0,  0],
               [ 0,  0, 10, 11,  0,  0,  0],
               [ 0,  0, 12, 13,  0,  0,  0],
               [ 0,  0, 14, 15,  0,  0,  0],
               [ 0,  0, 16, 17,  0,  0,  0],
               [ 0,  0, 18, 19,  0,  0,  0],
               [ 0,  0, 20, 21,  0,  0,  0],
               [ 0,  0, 22, 23,  0,  0,  0],
               [ 0,  0, 24, 25,  0,  0,  0],
               [ 0,  0, 26, 27,  0,  0,  0],
               [ 0,  0, 28, 29,  0,  0,  0],
               [ 0,  0, 30, 31,  0,  0,  0],
               [ 0,  0, 32, 33,  0,  0,  0],
               [ 0,  0, 34, 35,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0]])
        >>> lpA2 = lz.pad(A, ((2, 3), (4, 1)))
        >>> lpA2
        <23x7 LazyLinOp with unspecified dtype>
        >>> lpA2.toarray().astype('int')
        array([[ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  1,  0],
               [ 0,  0,  0,  0,  2,  3,  0],
               [ 0,  0,  0,  0,  4,  5,  0],
               [ 0,  0,  0,  0,  6,  7,  0],
               [ 0,  0,  0,  0,  8,  9,  0],
               [ 0,  0,  0,  0, 10, 11,  0],
               [ 0,  0,  0,  0, 12, 13,  0],
               [ 0,  0,  0,  0, 14, 15,  0],
               [ 0,  0,  0,  0, 16, 17,  0],
               [ 0,  0,  0,  0, 18, 19,  0],
               [ 0,  0,  0,  0, 20, 21,  0],
               [ 0,  0,  0,  0, 22, 23,  0],
               [ 0,  0,  0,  0, 24, 25,  0],
               [ 0,  0,  0,  0, 26, 27,  0],
               [ 0,  0,  0,  0, 28, 29,  0],
               [ 0,  0,  0,  0, 30, 31,  0],
               [ 0,  0,  0,  0, 32, 33,  0],
               [ 0,  0,  0,  0, 34, 35,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0],
               [ 0,  0,  0,  0,  0,  0,  0]])
        >>> # the same with arbitrary values
        >>> pw = ((2, 3), (4, 1))
        >>> cv = ((-1, -2), (-3, -4))
        >>> lpA3 = lz.pad(A, pw, constant_values=cv)
        >>> lpA3
        <23x7 LazyLinOp with unspecified dtype>
        >>> lpA3.toarray().astype('int')
        array([[-3, -3, -3, -3, -1, -1, -4],
               [-3, -3, -3, -3, -1, -1, -4],
               [-3, -3, -3, -3,  0,  1, -4],
               [-3, -3, -3, -3,  2,  3, -4],
               [-3, -3, -3, -3,  4,  5, -4],
               [-3, -3, -3, -3,  6,  7, -4],
               [-3, -3, -3, -3,  8,  9, -4],
               [-3, -3, -3, -3, 10, 11, -4],
               [-3, -3, -3, -3, 12, 13, -4],
               [-3, -3, -3, -3, 14, 15, -4],
               [-3, -3, -3, -3, 16, 17, -4],
               [-3, -3, -3, -3, 18, 19, -4],
               [-3, -3, -3, -3, 20, 21, -4],
               [-3, -3, -3, -3, 22, 23, -4],
               [-3, -3, -3, -3, 24, 25, -4],
               [-3, -3, -3, -3, 26, 27, -4],
               [-3, -3, -3, -3, 28, 29, -4],
               [-3, -3, -3, -3, 30, 31, -4],
               [-3, -3, -3, -3, 32, 33, -4],
               [-3, -3, -3, -3, 34, 35, -4],
               [-3, -3, -3, -3, -2, -2, -4],
               [-3, -3, -3, -3, -2, -2, -4],
               [-3, -3, -3, -3, -2, -2, -4]])



        zero-padded DFT example:
            >>> import lazylinop as lz
            >>> from lazylinop.signal import fft
            >>> e = lz.eye(5)
            >>> pe = lz.pad(e, (0, 3))
            >>> pfft = fft(8) @ pe

        Example ``mode='symmetric'``, ``mode='reflect'``:
            >>> import lazylinop as lz
            >>> a = np.arange(25).reshape(5, 5)
            >>> sp_a = lz.pad(a, (2, 1), mode='symmetric')
            >>> print(sp_a)
            <8x8 LazyLinOp with unspecified dtype>
            >>> sp_a.toarray().astype('int')
            array([[ 6,  5,  5,  6,  7,  8,  9,  9],
                   [ 1,  0,  0,  1,  2,  3,  4,  4],
                   [ 1,  0,  0,  1,  2,  3,  4,  4],
                   [ 6,  5,  5,  6,  7,  8,  9,  9],
                   [11, 10, 10, 11, 12, 13, 14, 14],
                   [16, 15, 15, 16, 17, 18, 19, 19],
                   [21, 20, 20, 21, 22, 23, 24, 24],
                   [21, 20, 20, 21, 22, 23, 24, 24]])
            >>> sp_a2 = lz.pad(a, ((1, 1), (2, 1)), mode='symmetric')
            >>> print(sp_a2)
            <7x8 LazyLinOp with unspecified dtype>
            >>> sp_a2.toarray().astype('int')
            array([[ 1,  0,  0,  1,  2,  3,  4,  4],
                   [ 1,  0,  0,  1,  2,  3,  4,  4],
                   [ 6,  5,  5,  6,  7,  8,  9,  9],
                   [11, 10, 10, 11, 12, 13, 14, 14],
                   [16, 15, 15, 16, 17, 18, 19, 19],
                   [21, 20, 20, 21, 22, 23, 24, 24],
                   [21, 20, 20, 21, 22, 23, 24, 24]])
            >>> rp_a = lz.pad(a, (2, 1), mode='reflect')
            >>> print(rp_a)
            <8x8 LazyLinOp with unspecified dtype>
            >>> rp_a.toarray().astype('int')
            array([[12, 11, 10, 11, 12, 13, 14, 13],
                   [ 7,  6,  5,  6,  7,  8,  9,  8],
                   [ 2,  1,  0,  1,  2,  3,  4,  3],
                   [ 7,  6,  5,  6,  7,  8,  9,  8],
                   [12, 11, 10, 11, 12, 13, 14, 13],
                   [17, 16, 15, 16, 17, 18, 19, 18],
                   [22, 21, 20, 21, 22, 23, 24, 23],
                   [17, 16, 15, 16, 17, 18, 19, 18]])
            >>> rp_a2 = lz.pad(a, ((1, 1), (2, 1)), mode='reflect')
            >>> print(rp_a2)
            <7x8 LazyLinOp with unspecified dtype>
            >>> rp_a2.toarray().astype('int')
            array([[ 7,  6,  5,  6,  7,  8,  9,  8],
                   [ 2,  1,  0,  1,  2,  3,  4,  3],
                   [ 7,  6,  5,  6,  7,  8,  9,  8],
                   [12, 11, 10, 11, 12, 13, 14, 13],
                   [17, 16, 15, 16, 17, 18, 19, 18],
                   [22, 21, 20, 21, 22, 23, 24, 23],
                   [17, 16, 15, 16, 17, 18, 19, 18]])


        Example ``mode='mean'``:
            >>> import lazylinop as lz
            >>> a = np.arange(25).reshape(5, 5)
            >>> mp_a = lz.pad(a, (2, 1), mode='mean')
            >>> print(mp_a)
            <8x8 LazyLinOp with unspecified dtype>
            >>> mp_a.toarray()
            array([[12., 12., 10., 11., 12., 13., 14., 12.],
                   [12., 12., 10., 11., 12., 13., 14., 12.],
                   [ 2.,  2.,  0.,  1.,  2.,  3.,  4.,  2.],
                   [ 7.,  7.,  5.,  6.,  7.,  8.,  9.,  7.],
                   [12., 12., 10., 11., 12., 13., 14., 12.],
                   [17., 17., 15., 16., 17., 18., 19., 17.],
                   [22., 22., 20., 21., 22., 23., 24., 22.],
                   [12., 12., 10., 11., 12., 13., 14., 12.]])
            >>> mp_a2 = lz.pad(a, ((1, 1), (2, 1)), mode='mean')
            >>> print(mp_a2)
            <7x8 LazyLinOp with unspecified dtype>
            >>> mp_a2.toarray()
            array([[12., 12., 10., 11., 12., 13., 14., 12.],
                   [ 2.,  2.,  0.,  1.,  2.,  3.,  4.,  2.],
                   [ 7.,  7.,  5.,  6.,  7.,  8.,  9.,  7.],
                   [12., 12., 10., 11., 12., 13., 14., 12.],
                   [17., 17., 15., 16., 17., 18., 19., 17.],
                   [22., 22., 20., 21., 22., 23., 24., 22.],
                   [12., 12., 10., 11., 12., 13., 14., 12.]])

        Example ``mode='edge'``:
            >>> import lazylinop as lz
            >>> a = np.arange(25).reshape(5, 5)
            >>> ep_a = lz.pad(a, (2, 1), mode='edge')
            >>> print(ep_a)
            <8x8 LazyLinOp with unspecified dtype>
            >>> y = ep_a.toarray().astype('int')
            >>> y
            array([[ 0,  0,  0,  1,  2,  3,  4,  4],
                   [ 0,  0,  0,  1,  2,  3,  4,  4],
                   [ 0,  0,  0,  1,  2,  3,  4,  4],
                   [ 5,  5,  5,  6,  7,  8,  9,  9],
                   [10, 10, 10, 11, 12, 13, 14, 14],
                   [15, 15, 15, 16, 17, 18, 19, 19],
                   [20, 20, 20, 21, 22, 23, 24, 24],
                   [20, 20, 20, 21, 22, 23, 24, 24]])
            >>> z = np.pad(a, (2, 1), mode='edge')
            >>> np.allclose(y, z)
            True
            >>> ep_a2 = lz.pad(a, ((1, 1), (2, 1)), mode='edge')
            >>> print(ep_a2)
            <7x8 LazyLinOp with unspecified dtype>
            >>> ep_a2.toarray().astype('int')
            array([[ 0,  0,  0,  1,  2,  3,  4,  4],
                   [ 0,  0,  0,  1,  2,  3,  4,  4],
                   [ 5,  5,  5,  6,  7,  8,  9,  9],
                   [10, 10, 10, 11, 12, 13, 14, 14],
                   [15, 15, 15, 16, 17, 18, 19, 19],
                   [20, 20, 20, 21, 22, 23, 24, 24],
                   [20, 20, 20, 21, 22, 23, 24, 24]])

        Example ``mode='wrap'``:
            >>> import lazylinop as lz
            >>> a = np.arange(25).reshape(5, 5)
            >>> wp_a = lz.pad(a, (2, 1), mode='wrap')
            >>> print(wp_a)
            <8x8 LazyLinOp with unspecified dtype>
            >>> wp_a.toarray().astype('int')
            array([[18, 19, 15, 16, 17, 18, 19, 15],
                   [23, 24, 20, 21, 22, 23, 24, 20],
                   [ 3,  4,  0,  1,  2,  3,  4,  0],
                   [ 8,  9,  5,  6,  7,  8,  9,  5],
                   [13, 14, 10, 11, 12, 13, 14, 10],
                   [18, 19, 15, 16, 17, 18, 19, 15],
                   [23, 24, 20, 21, 22, 23, 24, 20],
                   [ 3,  4,  0,  1,  2,  3,  4,  0]])
            >>> wp_a2 = lz.pad(a, ((1, 1), (2, 1)), mode='wrap')
            >>> print(wp_a2)
            <7x8 LazyLinOp with unspecified dtype>
            >>> wp_a2.toarray().astype('int')
            array([[23, 24, 20, 21, 22, 23, 24, 20],
                   [ 3,  4,  0,  1,  2,  3,  4,  0],
                   [ 8,  9,  5,  6,  7,  8,  9,  5],
                   [13, 14, 10, 11, 12, 13, 14, 10],
                   [18, 19, 15, 16, 17, 18, 19, 15],
                   [23, 24, 20, 21, 22, 23, 24, 20],
                   [ 3,  4,  0,  1,  2,  3,  4,  0]])

        .. seealso::
            `numpy.pad <https://numpy.org/doc/stable/reference/generated/
            numpy.pad.html>`_,
            :func:`.aslazylinop`
    """

    msg = "Invalid pad_width, see documentation for more details."
    if isinstance(pad_width, int):
        pw = ((pad_width, pad_width), (pad_width, pad_width))
    elif isinstance(pad_width, tuple) and len(pad_width) == 1:
        pw = ((pad_width[0], pad_width[0]), (pad_width[0], pad_width[0]))
    elif len(pad_width) == 2 and isinstance(pad_width[0], int) and \
       isinstance(pad_width[1], int):
        pw = ((pad_width[0], pad_width[1]), (pad_width[0], pad_width[1]))
    elif len(pad_width) == 2 and isinstance(pad_width[0], tuple) and \
         isinstance(pad_width[1], tuple):
        if len(pad_width[0]) == 1:
            b = (pad_width[0][0], pad_width[0][0])
        else:
            b = (pad_width[0][0], pad_width[0][1])
        if len(pad_width[1]) == 1:
            a = (pad_width[1][0], pad_width[1][0])
        else:
            a = (pad_width[1][0], pad_width[1][1])
        pw = (b, a)
    else:
        raise Exception(msg)
    for i in range(2):
        for j in range(2):
            if not isinstance(pw[i][j], int):
                raise Exception(msg)

    msg = "Invalid constant_values, see documentation for more details."
    if isinstance(constant_values, int):
        cv = ((constant_values, constant_values),
              (constant_values, constant_values))
    elif isinstance(constant_values, tuple) and len(constant_values) == 1:
        cv = ((constant_values[0], constant_values[0]),
              (constant_values[0], constant_values[0]))
    elif len(constant_values) == 2 and isinstance(constant_values[0], int) and \
       isinstance(constant_values[1], int):
        cv = ((constant_values[0], constant_values[1]),
              (constant_values[0], constant_values[1]))
    elif len(constant_values) == 2 and isinstance(constant_values[0], tuple) and \
         isinstance(constant_values[1], tuple):
        if len(constant_values[0]) == 1:
            b = (constant_values[0][0], constant_values[0][0])
        else:
            b = (constant_values[0][0], constant_values[0][1])
        if len(constant_values[1]) == 1:
            a = (constant_values[1][0], constant_values[1][0])
        else:
            a = (constant_values[1][0], constant_values[1][1])
        cv = (b, a)
    else:
        raise Exception(msg)
    for i in range(2):
        for j in range(2):
            if not isinstance(cv[i][j], int):
                raise Exception(msg)

    if mode == 'constant':
        P = aslazylinop(op)
        # Pad axis=0.
        # Before.
        M, N = P.shape
        b, a = pw[0]
        if b > 0:
            if cv[0][0] != 0:
                P = vstack((cv[0][0] * ones((b, N)), P))
            else:
                P = vstack((zeros((b, N)), P))
        # After.
        if a > 0:
            if cv[0][1] != 0:
                P = vstack((P, cv[0][1] * ones((a, N))))
            else:
                P = vstack((P, zeros((a, N))))
        # Pad axis=1.
        # Before.
        M, N = P.shape
        b, a = pw[1]
        if b > 0:
            if cv[1][0] != 0:
                P = hstack((cv[1][0] * ones((M, b)), P))
            else:
                P = hstack((zeros((M, b)), P))
        # After.
        if a > 0:
            if cv[1][1] != 0:
                P = hstack((P, cv[1][1] * ones((M, a))))
            else:
                P = hstack((P, zeros((M, a))))
    elif mode == 'symmetric':
        lop = aslazylinop(op)
        M, N = lop.shape
        bn = (pw[0][0] // M, pw[1][0] // N)
        be = (pw[0][0] % M, pw[1][0] % N)
        an = (pw[0][1] // M, pw[1][1] // N)
        ae = (pw[0][1] % M, pw[1][1] % N)
        # Pad axis=0.
        P = aslazylinop(op)
        # Before
        flip = True
        for _ in range(bn[0]):
            # Symmetric copy?
            P = vstack((anti_eye(M) @ lop if flip else lop, P))
            flip ^= True
        # be elements (according to mode).
        if be[0] > 0:
            P = vstack((eye(be[0], M, k=M - be[0]) @ (
                anti_eye(M) @ lop if flip else lop), P))
        # After
        flip = True
        for _ in range(an[0]):
            # Symmetric copy?
            P = vstack((P, anti_eye(M) @ lop if flip else lop))
            flip ^= True
        # ae elements (according to mode).
        if ae[0] > 0:
            P = vstack((P, eye(ae[0], M) @ (
                anti_eye(M) @ lop if flip else lop)))
        # Pad axis=1.
        lop = aslazylinop(P)
        M, N = lop.shape
        # Before
        flip = True
        for _ in range(bn[1]):
            # Symmetric copy?
            P = hstack((lop @ anti_eye(N) if flip else lop, P))
            flip ^= True
        # be elements (according to mode).
        if be[1] > 0:
            P = hstack(((lop @ anti_eye(N) if flip else lop) @ eye(be[1], N, k=N - be[1]).T, P))
        # After
        flip = True
        for _ in range(an[1]):
            # Symmetric copy?
            P = hstack((P, lop @ anti_eye(N) if flip else lop))
            flip ^= True
        # ae elements (according to mode).
        if ae[1] > 0:
            P = hstack((P, (
                lop @ anti_eye(N) if flip else lop) @ eye(ae[1], N).T))
    elif mode == 'antisymmetric':
        lop = aslazylinop(op)
        M, N = lop.shape
        bn = (pw[0][0] // M, pw[1][0] // N)
        be = (pw[0][0] % M, pw[1][0] % N)
        an = (pw[0][1] // M, pw[1][1] // N)
        ae = (pw[0][1] % M, pw[1][1] % N)
        # Pad axis=0.
        P = aslazylinop(op)
        # Before
        flip = True
        for _ in range(bn[0]):
            # Symmetric copy?
            P = vstack((-anti_eye(M) @ lop if flip else lop, P))
            flip ^= True
        # be elements (according to mode).
        if be[0] > 0:
            P = vstack((eye(be[0], M, k=M - be[0]) @ (
                -anti_eye(M) @ lop if flip else lop), P))
        # After
        flip = True
        for _ in range(an[0]):
            # Symmetric copy?
            P = vstack((P, -anti_eye(M) @ lop if flip else lop))
            flip ^= True
        # ae elements (according to mode).
        if ae[0] > 0:
            P = vstack((P, eye(ae[0], M) @ (
                -anti_eye(M) @ lop if flip else lop)))
        # Pad axis=1.
        lop = aslazylinop(P)
        M = lop.shape[0]
        # Before
        flip = True
        for _ in range(bn[1]):
            # Symmetric copy?
            P = hstack((-anti_eye(M) @ lop if flip else lop, P))
            flip ^= True
        # be elements (according to mode).
        if be[1] > 0:
            P = hstack(((lop @ -anti_eye(M) if flip else lop) @ eye(be[1], M, k=M - be[1]).T, P))
        # After
        flip = True
        for _ in range(an[1]):
            # Symmetric copy?
            P = hstack((P, -anti_eye(M) @ lop if flip else lop))
            flip ^= True
        # ae elements (according to mode).
        if ae[1] > 0:
            P = hstack((P, (
                lop @ -anti_eye(M) if flip else lop) @ eye(ae[1], M).T))
    elif mode == 'periodic' or mode == 'wrap':
        lop = aslazylinop(op)
        M, N = lop.shape
        bn = (pw[0][0] // M, pw[1][0] // N)
        be = (pw[0][0] % M, pw[1][0] % N)
        an = (pw[0][1] // M, pw[1][1] // N)
        ae = (pw[0][1] % M, pw[1][1] % N)
        # Pad axis=0
        # Because mode is periodic, we just have to copy/paste.
        if (bn[0] + an[0]) == 0:
            P = aslazylinop(op)
        else:
            P = kron(ones((bn[0] + 1 + an[0], 1)), lop)
        if be[0] > 0:
            P = (eye(be[0], M, k=M - be[0]) @ lop).vstack(P)
        if ae[0] > 0:
            P = P.vstack(eye(ae[0], M) @ lop)
        # Pad axis=1
        lop = aslazylinop(P)
        M, N = lop.shape
        # Before
        for _ in range(bn[1]):
            P = hstack((lop, P))
        # be elements (according to mode).
        if be[1] > 0:
            P = hstack((lop @ eye(be[1], N, k=N - be[1]).T, P))
        # After
        for _ in range(an[1]):
            P = hstack((P, lop))
        # ae elements (according to mode).
        if ae[1] > 0:
            P = hstack((P, lop @ eye(ae[1], N).T))
    elif mode == 'reflect':
        M, N = op.shape
        if M == 1 or N == 1:
            raise ValueError("op.shape must be > 1.")
        lop = aslazylinop(op)
        M, N = lop.shape
        bn = (pw[0][0] // (M - 1), pw[1][0] // (N - 1))
        be = (pw[0][0] % (M - 1), pw[1][0] % (N - 1))
        an = (pw[0][1] // (M - 1), pw[1][1] // (N - 1))
        ae = (pw[0][1] % (M - 1), pw[1][1] % (N - 1))
        # Pad axis=0.
        P = aslazylinop(op)
        # Before
        flip = True
        for _ in range(bn[0]):
            # Reflected copy.
            P = vstack((anti_eye(M - 1, M) @ lop if flip
                        else eye(M - 1, M) @ lop, P))
            flip ^= True
        # be elements (according to mode).
        if be[0] > 0:
            P = vstack((anti_eye(be[0], M, k=M - 1 - be[0]) @ lop if flip
                        else eye(be[0], M, k=M - 1 - be[0]) @ lop, P))
        # After
        flip = True
        for _ in range(an[0]):
            # Reflected copy.
            P = vstack((P, anti_eye(M - 1, M, k=1) @ lop if flip
                        else eye(M - 1, M, k=1) @ lop))
            flip ^= True
        # ae elements (according to mode).
        if ae[0] > 0:
            P = vstack((P, anti_eye(ae[0], M, k=1) @ lop if flip
                        else eye(ae[0], M, k=1) @ lop))
        # Pad axis=1.
        lop = aslazylinop(P)
        M, N = lop.shape
        # Before
        flip = True
        for _ in range(bn[1]):
            # Reflected copy.
            P = hstack((lop @ anti_eye(N - 1, N).T if flip
                        else lop @ eye(N - 1, N).T, P))
            flip ^= True
        # be elements (according to mode).
        if be[1] > 0:
            P = hstack((lop @ anti_eye(be[1], N, k=N - 1 - be[1]).T if flip
                        else lop @ eye(be[1], N, k=N - 1 - be[1]).T, P))
        # After
        flip = True
        for _ in range(an[1]):
            # Reflected copy.
            P = hstack((P, lop @ anti_eye(N - 1, N, k=1).T if flip
                        else lop @ eye(N - 1, N, k=1).T))
            flip ^= True
        # ae elements (according to mode).
        if ae[1] > 0:
            P = hstack((P, lop @ anti_eye(ae[1], N, k=1).T if flip
                        else lop @ eye(ae[1], N, k=1).T))
    elif mode == 'edge':
        # Pad axis=0.
        lop = aslazylinop(op)
        M, N = lop.shape
        P = aslazylinop(op)
        # Edge before.
        if pw[0][0] > 0:
            P = vstack((
                kron(ones((pw[0][0], 1)), eye(1, M) @ lop), lop))
        # Edge after.
        if pw[0][1] > 0:
            P = vstack((
                P, kron(ones((pw[0][1], 1)), eye(1, M, k=M - 1) @ lop)))
        # Pad axis=1.
        lop = aslazylinop(P)
        M, N = lop.shape
        # Edge before.
        if pw[1][0] > 0:
            P = hstack((
                kron(ones((1, pw[1][0])), lop @ eye(N, 1)), P))
        # Edge after.
        if pw[1][1] > 0:
            P = hstack((
                P, kron(ones((1, pw[1][1])), lop @ eye(N, 1, k=-(N - 1)))))
    elif mode == 'mean':
        # Pad axis=0.
        lop = aslazylinop(op)
        M, N = lop.shape
        P = aslazylinop(op)
        # Mean before.
        if pw[0][0] > 0:
            P = vstack((
                kron(ones((pw[0][0], 1)), 1 / M * ones((1, M)) @ lop), lop))
        # Mean after.
        if pw[0][1] > 0:
            P = vstack((
                P, kron(ones((pw[0][1], 1)), 1 / M * ones((1, M)) @ lop)))
        # Pad axis=1.
        lop = aslazylinop(P)
        M, N = lop.shape
        # Mean before.
        if pw[1][0] > 0:
            P = hstack((
                kron(ones((1, pw[1][0])), lop @ (1 / N * ones((N, 1)))), P))
        # Mean after.
        if pw[1][1] > 0:
            P = hstack((
                P, kron(ones((1, pw[1][1])), lop @ (1 / N * ones((N, 1))))))
    else:
        raise Exception("mode must be either 'constant', 'symmetric', 'antisymmetric',"
                        + " 'wrap', 'periodic', 'reflect', 'edge' or 'mean'.")
    return P


def misc_padder(X_shape, pad_width):
    """
    Returns a :py:class:`LazyLinOp` for row dimension zero padding of any X.

    The :py:class:`LazyLinOp` ``L`` returned is also able to unpad the
    padded result ``(L @ x)`` to get back the original ``x``.
    See unpadding examples below.

    Args:
        X:
            Operator to apply the padding to.
        pad_width: (tuple[int, int]/list[int, int])
            A pair of integers. pad_width[0] is the "before"
            padding size and pad_width[1] is the "after" padding size.

    Example:
        >>> from lazylinop import misc_padder
        >>> from numpy import arange
        >>> A = arange(18*2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lz = misc_padder(A.shape, (2, 3))
        >>> lz
        <46x36 LazyLinOp with unspecified dtype>
        >>> lz @ A
        array([[ 0,  0],
               [ 0,  0],
               [ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35],
               [ 0,  0],
               [ 0,  0],
               [ 0,  0]])
        >>> # padding for a vector
        >>> x = np.full(3, 1.)
        >>> lz2 = misc_padder(x.shape, (2, 3))
        >>> lz2 @ x
        array([0., 0., 1., 1., 1., 0., 0., 0.])

        Unpadding:

        >>> paddedA = (lz @ A).ravel()
        >>> np.allclose(lz.H @ paddedA, A.ravel())
        True
        >>> np.allclose((lz.H @ paddedA).reshape(A.shape), A)
        True

        >>> lz2.H @ (lz2 @ x)
        array([1., 1., 1.])
    """
    return ppadder(X_shape, (pad_width, (0, 0))
                   if len(X_shape) == 2 else pad_width)


def ppadder(x_shape, pad_width, mode='constant', constant_values=0, **kwargs):
    """
    Returns a :py:class:`LazyLinOp` for zero padding of any X.

    .. warning:: this is a permissive padder that allows to break the properly
    defined matrix product because it can pad such that the number of columns
    of input is not the same as output.
    It permits also to pad with nonzero constant values.
    Rather use :py:func:`pad` or :py:func:`padder` for a strict LazyLinOp.

    Note: the LazyLinOp L returned is able to unpad the padded result
    (L @ x) to get back the original x. See unpadding examples below.

    Args:
        x_shape:
             shape of x to apply the padding to.
        pad_width:
             a tuple/list of tuples/pairs of integers. It can be one tuple only
             if x is one-dimensional or a tuple of two tuples if x
             two-dimensional.
        mode:
            see :py:func:`.pad`
        constant_values: one or two tuples of two scalars or scalar.
            ((before0, after0), (before1, after1)), or ((before0, after0)) or
            (constant,) or constant: values for padding before and after on
            each dimension. If not enough values before = after and in case of
            a missing value for a dimension then the same values are used for
            the two dimensions.

    Example:
        >>> from lazylinop.basicops import ppadder
        >>> from numpy import arange
        >>> A = arange(18*2).reshape((18, 2))
        >>> A
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> lz = ppadder(A.shape, ((2, 3), (4, 1)))
        >>> lz
        <161x36 LazyLinOp with unspecified dtype>
        >>> np.round(lz @ A, decimals=2).astype('double')
        array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  1.,  0.],
               [ 0.,  0.,  0.,  0.,  2.,  3.,  0.],
               [ 0.,  0.,  0.,  0.,  4.,  5.,  0.],
               [ 0.,  0.,  0.,  0.,  6.,  7.,  0.],
               [ 0.,  0.,  0.,  0.,  8.,  9.,  0.],
               [ 0.,  0.,  0.,  0., 10., 11.,  0.],
               [ 0.,  0.,  0.,  0., 12., 13.,  0.],
               [ 0.,  0.,  0.,  0., 14., 15.,  0.],
               [ 0.,  0.,  0.,  0., 16., 17.,  0.],
               [ 0.,  0.,  0.,  0., 18., 19.,  0.],
               [ 0.,  0.,  0.,  0., 20., 21.,  0.],
               [ 0.,  0.,  0.,  0., 22., 23.,  0.],
               [ 0.,  0.,  0.,  0., 24., 25.,  0.],
               [ 0.,  0.,  0.,  0., 26., 27.,  0.],
               [ 0.,  0.,  0.,  0., 28., 29.,  0.],
               [ 0.,  0.,  0.,  0., 30., 31.,  0.],
               [ 0.,  0.,  0.,  0., 32., 33.,  0.],
               [ 0.,  0.,  0.,  0., 34., 35.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.],
               [ 0.,  0.,  0.,  0.,  0.,  0.,  0.]])
        >>> # padding for a vector
        >>> x = np.full(3, 1)
        >>> lz2 = ppadder(x.shape, ((2, 3)))
        >>> lz2 @ x
        array([0, 0, 1, 1, 1, 0, 0, 0])

    Padding A with arbitrary constant values:
        >>> x = np.full(3, 1)
        >>> lcv = ppadder(x.shape, ((2, 3)), constant_values=(2, 5))
        >>> lcv @ x
        array([2, 2, 1, 1, 1, 5, 5, 5])
        >>> lcv = ppadder(x.shape, ((2, 3)), constant_values=(2., 5.))
        >>> lcv @ x
        array([2, 2, 1, 1, 1, 5, 5, 5])
        >>> cv = ((2, 5), (3, 6))
        >>> pw = ((2, 3), (4, 1))
        >>> lz3 = ppadder(A.shape, pw, constant_values=cv)
        >>> lz3 @ A
        array([[ 3,  3,  3,  3,  2,  2,  6],
               [ 3,  3,  3,  3,  2,  2,  6],
               [ 3,  3,  3,  3,  0,  1,  6],
               [ 3,  3,  3,  3,  2,  3,  6],
               [ 3,  3,  3,  3,  4,  5,  6],
               [ 3,  3,  3,  3,  6,  7,  6],
               [ 3,  3,  3,  3,  8,  9,  6],
               [ 3,  3,  3,  3, 10, 11,  6],
               [ 3,  3,  3,  3, 12, 13,  6],
               [ 3,  3,  3,  3, 14, 15,  6],
               [ 3,  3,  3,  3, 16, 17,  6],
               [ 3,  3,  3,  3, 18, 19,  6],
               [ 3,  3,  3,  3, 20, 21,  6],
               [ 3,  3,  3,  3, 22, 23,  6],
               [ 3,  3,  3,  3, 24, 25,  6],
               [ 3,  3,  3,  3, 26, 27,  6],
               [ 3,  3,  3,  3, 28, 29,  6],
               [ 3,  3,  3,  3, 30, 31,  6],
               [ 3,  3,  3,  3, 32, 33,  6],
               [ 3,  3,  3,  3, 34, 35,  6],
               [ 3,  3,  3,  3,  5,  5,  6],
               [ 3,  3,  3,  3,  5,  5,  6],
               [ 3,  3,  3,  3,  5,  5,  6]])
        >>> np.allclose(lz3 @ A, np.pad(A, pw, constant_values=cv))
        True

    Unpadding a padded vector:
        >>> lz2.H @ (lz2 @ x)
        array([1, 1, 1])
        >>> lcv.H @ (lcv @ x)
        array([1, 1, 1])
        >>> # in both cases we retrieved the original x

    Unpadding a padded 2d-array:
        >>> (lz3.H @ (lz3 @ A).ravel()).reshape(A.shape)
        array([[ 0,  1],
               [ 2,  3],
               [ 4,  5],
               [ 6,  7],
               [ 8,  9],
               [10, 11],
               [12, 13],
               [14, 15],
               [16, 17],
               [18, 19],
               [20, 21],
               [22, 23],
               [24, 25],
               [26, 27],
               [28, 29],
               [30, 31],
               [32, 33],
               [34, 35]])
        >>> # original A is retrieved

    See also `numpy.pad <https://numpy.org/doc/stable/reference/generated/
    numpy.pad.html>`_
    """
    constant_values = _sanitize_contant_values(constant_values)
    pad_width = np.array(pad_width).astype('int')
    if pad_width.shape[0] > 2 or pad_width.ndim > 1 and pad_width.shape[1] > 2:
        raise ValueError('Cannot pad zeros on more than two dimensions')
    if len(x_shape) != pad_width.ndim:
        raise ValueError('pad_width number of tuples must be len(x_shape).')
    if pad_width.ndim == 1:
        pad_width_ndim_was_1 = True
        pad_width = np.vstack((pad_width, (0, 0)))
    else:
        pad_width_ndim_was_1 = False
    kron_handled_cv = [((0, 0), (0, 0))]
    x_size = np.prod(x_shape)
    # See NumPy behavior.
    # x_is_vec = x_size == x_shape[0] or x_size == x_shape[1]
    x_is_vec = len(x_shape) == 1
    if 'impl' not in kwargs or kwargs['impl'] != 'nokron':
        if ('impl' in kwargs and 'kron' == kwargs['impl'] or
            'impl' not in kwargs and
                x_is_vec and constant_values in kron_handled_cv):
            if constant_values not in kron_handled_cv:
                raise ValueError('kron impl can only be used in case of'
                                 ' zero-padding but constant_values are not 0')
            if x_is_vec == 1:
                pad_width = tuple(pad_width[0])
            return kron_pad((x_size,), pad_width)
    lop_shape = (np.prod(np.sum(pad_width if len(x_shape) == 2 else
                                pad_width[0], axis=0 if len(x_shape) == 1 else
                                1) +
                         x_shape),
                 np.prod(x_shape))

    def mul(op):
        # op can only be a np.ndarray, a torch.Tensor, a cupy.array
        # or a scipy matrix (see LazyLinOp)
        if 'scipy.sparse' in str(op.__class__):
            import array_api_compat.numpy as xp
        elif 'cupyx.scipy.sparse' in str(op.__class__):
            import array_api_compat.cupy as xp
        else:
            xp = array_api_compat.array_namespace(op)
        op_reshaped = False
        if op.ndim == 1:
            if pad_width_ndim_was_1:
                if is_torch_array(op):
                    if len(constant_values[0]) == 1:
                        return torch.nn.functional.pad(
                            op, pad_width[0].tolist(), mode=mode,
                            value=constant_values[0])
                    else:
                        # FIXME
                        op = torch.nn.functional.pad(
                            op, (pad_width[0][0], 0), mode=mode,
                            value=constant_values[0][0])
                        return torch.nn.functional.pad(
                            op, (0, pad_width[0][1]), mode=mode,
                            value=constant_values[0][1])
                else:
                    return np.pad(op, pad_width[0], mode=mode,
                                  constant_values=constant_values[0])
            else:
                op = op.reshape(x_shape)
                op_reshaped = True
        elif (mode == 'constant' and x_shape == op.shape and
              (isinstance(op, np.ndarray) or
               is_torch_array(op) or is_cupy_array(op))):
            if (constant_values == ((0, 0), (0, 0)) and
                    all(pad_width[0] == (0, 0))):
                # particular case opt. (zero padding of columns)
                out = xp.zeros((x_shape[0], x_shape[1] + np.sum(pad_width[1])),
                               dtype=op.dtype)
                out[:, pad_width[1][0]:pad_width[1][0]+op.shape[1]] = op
                return out
            else:
                if is_torch_array(op):
                    xo = torch.nn.functional.pad(op, (pad_width[1, 0], 0, 0, 0), mode=mode, value=constant_values[1][0])
                    xo = torch.nn.functional.pad(xo, (0, pad_width[1, 1], 0, 0), mode=mode, value=constant_values[1][1])
                    xo = torch.nn.functional.pad(xo, (0, 0, pad_width[0, 0], 0), mode=mode, value=constant_values[0][0])
                    return torch.nn.functional.pad(xo, (0, 0, 0, pad_width[0, 1]), mode=mode, value=constant_values[0][1])
                    # return torch.nn.functional.pad(
                    #     op, pad_width[::-1], mode=mode,
                    #     value=constant_values)
                else:
                    return np.pad(op, pad_width, mode=mode,
                                  constant_values=constant_values)
        elif x_shape != op.shape:
            # FIXME: Do not understand next line.
            #        It seems to return a recursion limit.
            # out = aslazylinop(xp.empty((lop_shape[0], 0)))
            for j in range(op.shape[1]):
                out_v = mul(op[:, j])
                if out_v.ndim == 1:
                    out_v = out_v.reshape((out_v.shape[0], 1))
                if j == 0:
                    out = aslazylinop(out_v)
                else:
                    out = hstack((out, out_v))
            return out.toarray(array_namespace=xp)
        out = _cat_pad(op, pad_width, mode, constant_values)
        if op_reshaped:
            return out.toarray(array_namespace=xp).ravel()
        else:
            return out.toarray(array_namespace=xp)

    def rmul(op):
        # op can only be a np.ndarray, a torch.Tensor or a scipy matrix (see LazyLinOp)
        if 'scipy.sparse' in str(op.__class__):
            import array_api_compat.numpy as xp
        elif 'cupyx.scipy.sparse' in str(op.__class__):
            import array_api_compat.cupy as xp
        else:
            xp = array_api_compat.array_namespace(op)
        op_std_2d_shape = tuple(np.sum(pad_width, axis=len(pad_width) - 1) +
                                x_shape)
        if op.ndim == 1:
            if pad_width_ndim_was_1:
                return op[pad_width[0, 0]: pad_width[0, 0] + x_shape[0]]
            else:
                op = op.reshape(op_std_2d_shape)
                r_offset = pad_width[0][0]
                c_offset = pad_width[1][0]
                out = op[r_offset:r_offset + x_shape[0],
                        c_offset:c_offset + x_shape[1]]
                return out.ravel()
        elif op_std_2d_shape != op.shape:
            # FIXME: Do not understand next line.
            #        It seems to return a recursion limit.
            # out = aslazylinop(xp.empty((lop_shape[1], 0)))
            for j in range(op.shape[1]):
                out_v = rmul(op[:, j])
                if out_v.ndim == 1:
                    out_v = out_v.reshape((out_v.shape[0], 1))
                if j == 0:
                    out = aslazylinop(out_v)
                else:
                    out = hstack((out, out_v))
            return out.toarray(array_namespace=xp)
        else:
            # FIXME: it happens it enters the else.
            print('why here?')

    ret = LazyLinOp(lop_shape, matmat=lambda op: mul(op), rmatmat=lambda
                    op: rmul(op))
    ret.ravel_op = True  # a 2d array can be flatten to be compatible
    # to zpad.shape[1]
    return ret


def _cat_pad(op, pad_width, mode, constant_values):
    out = aslazylinop(op)
    for i in range(pad_width.shape[0]):
        bw = pad_width[i][0]
        aw = pad_width[i][1]
        bv = constant_values[i][0]
        av = constant_values[i][0]
        if bw > 0:
            if i == 0:
                out = vstack((_pad_block((bw, out.shape[1]), bv,
                                         mode=mode, op=op,
                                         axis=i,
                                         side='before'), out))
            else:  # i == 1:
                out = hstack((_pad_block((out.shape[0], bw), bv,
                                         mode=mode, op=op,
                                         axis=i,
                                         side='before'), out))
        if aw > 0:
            if i == 0:
                out = vstack((out, _pad_block((aw, out.shape[1]), av,
                                              mode=mode, op=op,
                                              axis=i,
                                              side='after')))
            else:  # i == 1:
                out = hstack((out, _pad_block((out.shape[0], aw), av,
                                              mode=mode, op=op,
                                              axis=i,
                                              side='after')))
        op = out
    return out


def zpad(x_shape, pad_width):
    """
    Deprecated alias for :py:func:`pad` with zero as constant value to pad.
    This function might be removed in a next version.
    """
    warn("Don't use [DEPRECATED] zpad, use pad with default constant_values"
         " (zeros)")
    return ppadder(x_shape, pad_width, constant_values=0)


def _sanitize_contant_values(constant_values):
    if np.isscalar(constant_values) and np.isreal(constant_values):
        constant_values = [int(constant_values), ]
    if isinstance(constant_values, (tuple, np.ndarray)):
        constant_values = list(constant_values)
    if not isinstance(constant_values, list):
        raise TypeError('Invalid constant_values')
    if len(constant_values) == 1:
        constant_values = [constant_values, constant_values]
    if np.isscalar(constant_values[0]) and np.isscalar(constant_values[1]):
        constant_values = [constant_values, constant_values]
    for i in range(2):
        lc = len(constant_values[i])
        if lc == 1:
            constant_values[i] = [constant_values[i][0],
                                  constant_values[i][0]]
        elif lc != 2:
            raise ValueError('constant_values contain sequence of invalid size'
                             ' (valid sizes are 1 or 2)')
        for j in range(2):
            if (not np.isscalar(constant_values[i][j]) or
                    not np.isreal(constant_values[i][j])):
                raise ValueError('constant_values contains something that is'
                                 ' not a scalar')
        constant_values[i] = list((int(constant_values[i][0]),
                                  int(constant_values[i][1])))
        # convert to tuple
        constant_values[i] = tuple(constant_values[i])
    return tuple(constant_values)


sanitize_const_values = _sanitize_contant_values

# TODO: _sanitize_pad_width


def _pad_block(shape, v=0, op=None, mode='constant', axis=0, side='before'):
    from lazylinop.basicops import zeros, ones
    assert side in ['before', 'after']
    if mode == 'constant':
        if v == 0:
            return zeros(shape)
        else:
            return ones(shape) * v
    elif mode in ['symmetric', 'reflect']:
        return _pad_reflect_symmetric(op, shape, axis, side, mode)
    elif mode == 'mean':
        return _pad_block_mean(op, shape, axis, side)
    elif mode == 'edge':
        return _pad_block_edge(op, shape, axis, side)
    elif mode == 'wrap':
        return _pad_block_wrap(op, shape, axis, side)


def _pad_reflect_symmetric(op, shape, axis, side, mode):
    ids = {
        'symmetric':
        {
            0:  # axis
                {
                    'before': slice(0, shape[0]),
                    'after': slice(op.shape[0] - shape[0], op.shape[0])
                },
            1:  # axis
                {
                    'before': slice(0, shape[1]),
                    'after': slice(op.shape[1] - shape[1], op.shape[1])
                }
        },
        'reflect':
        {
            0:  # axis
                {
                    'before': slice(1, shape[0] + 1),
                    'after': slice(op.shape[0] - shape[0] - 1,
                                   op.shape[0]-1)
                },
            1:  # axis
                {
                    'before': slice(1, shape[1] + 1),
                    'after': slice(op.shape[1] - shape[1] - 1,
                                   op.shape[1] - 1)
                }
        }
    }
    if axis == 0:
        return op[ids[mode][axis][side]][::-1]
    elif axis == 1:
        return op[:, ids[mode][axis][side]][:, ::-1]


def _pad_block_mean(op, shape, axis, side):
    from lazylinop.wip.basicops import mean
    m = mean(op, axis)
    if axis == 0:
        sf = vstack
    else:
        assert axis == 1
        sf = hstack
    m_stack = sf([m for _ in range(shape[axis])])
    return m_stack


def _pad_block_edge(op, shape, axis, side):
    if axis == 0:
        sf = vstack
        if side == 'before':
            e = op[0:1, :]
        else:
            assert side == 'after'
            e = op[-1:, :]
    else:
        assert axis == 1
        sf = hstack
        if side == 'before':
            e = op[:, 0:1]
        else:
            assert side == 'after'
            e = op[:, -1:]
    e_stack = sf([e for _ in range(shape[axis])])
    return e_stack


def _pad_block_wrap(op, shape, axis, side):
    n = shape[axis]  # num of rows/cols yet to pad
    w = None  # wrap padded block
    while n > 0:
        pn = min(n, op.shape[axis])  # num of padded rows/cols for ite
        if axis == 0:
            if side == 'before':
                w = op[-pn:] if w is None else vstack((op[-pn:], w))
            else:
                assert side == 'after'
                w = op[:pn] if w is None else vstack((w, op[:pn]))
        else:
            assert axis == 1
            if side == 'before':
                w = op[:, -pn:] if w is None else hstack((op[:, -pn:], w))
            else:
                assert side == 'after'
                w = op[:, :pn] if w is None else hstack((w, op[:, :pn]))
        n -= pn
    return w


def kron_pad(shape: tuple, pad_width: tuple):
    """Constructs a lazy linear operator Op for padding.

    If shape is a tuple (X, Y), Op is applied to a 1d array of shape (X * Y, ).
    The output of the padding of the 2d input array is given by
    Op @ input.flatten(order='C').
    You should use output.reshape(X, Y) to get a 2d output array.
    The function uses Kronecker trick vec(M @ X @ N) = kron(M.T, N) @ vec(X)
    to pad both rows and columns.

    Args:
        shape: tuple
            Shape of the input
        pad_width: tuple
            It can be (A, B):
            Add A zero columns and rows before and B zero columns and
            rows after.
            or ((A, B), (C, D)):
            Add A zero rows before and B zero rows after.
            Add C zero columns to the left and D zero columns to the right.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            pad_width expects (A, B) or ((A, B), (C, D)).
        ValueError
            pad_width expects positive values.
        ValueError
            If len(shape) is 1, pad_width expects a tuple (A, B).

    Examples:
        >>> from lazylinop.basicops.pad import kron_pad as lz_kron_pad
        >>> x = np.arange(1, 4 + 1, 1).reshape(2, 2)
        >>> x
        array([[1, 2],
               [3, 4]])
        >>> y = lz_kron_pad(x.shape, (1, 2)) @ x.flatten()
        >>> y.reshape(5, 5)
        array([[0, 0, 0, 0, 0],
               [0, 1, 2, 0, 0],
               [0, 3, 4, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]])
        >>> x = np.arange(1, 6 + 1, 1).reshape(2, 3)
        >>> x
        array([[1, 2, 3],
               [4, 5, 6]])
        >>> y = lz_kron_pad(x.shape, ((2, 1), (2, 3))) @ x.flatten()
        >>> y.reshape(5, 8)
        array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 2, 3, 0, 0, 0],
               [0, 0, 4, 5, 6, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]])

    References:
        See also `numpy.pad <https://numpy.org/doc/stable/reference/generated/
        numpy.pad.html>`_
    """
    W = len(pad_width)
    if W != 2:
        raise ValueError("pad_width expects (A, B) or ((A, B), (C, D)).")
    if len(shape) == 1:
        if type(pad_width) is not tuple:
            raise ValueError("If len(shape) is 1, pad_width expects"
                             " a tuple (A, B).")
        if pad_width[0] < 0 or pad_width[1] < 0:
            raise ValueError("pad_width expects positive values.")
        Op = eye(shape[0] + pad_width[0] + pad_width[1], shape[0],
                 k=-pad_width[0])
        return Op
    elif len(shape) == 2:
        if type(pad_width[0]) is tuple:
            # pad_witdh is ((A, B), (C, D))
            for w in range(W):
                if pad_width[w][0] < 0 or pad_width[w][1] < 0:
                    raise ValueError("pad_width expects positive values.")
                Ww = len(pad_width[w])
                if Ww != 2:
                    raise ValueError("pad_width expects (A, B) or"
                                     " ((A, B), (C, D)).")
                if w == 0:
                    M = eye(shape[0] + pad_width[w][0] + pad_width[w][1],
                            shape[0], k=-pad_width[w][0])
                elif w == 1:
                    NT = eye(shape[1] + pad_width[w][0] + pad_width[w][1],
                             shape[1], k=-pad_width[w][0])
            return kron(M, NT)
        else:
            if pad_width[0] < 0 or pad_width[1] < 0:
                raise ValueError("pad_width expects positive values.")
            # pad_witdh is (A, B), pad each dimension
            M = eye(shape[0] + pad_width[0] + pad_width[1], shape[0],
                    k=-pad_width[0])
            NT = eye(shape[1] + pad_width[0] + pad_width[1], shape[1],
                     k=-pad_width[0])
            return kron(M, NT)
    else:
        raise ValueError("shape must be 1d or 2d dimensional only")


def mpad2(L: int, X: int, n: int = 1):
    """Return a :py:class:`LazyLinOp` to zero-pad each block of a signal.

    If you apply this operator to a vector of length L * X the output will
    have a length (L + n) * X.

    Args:
        L: int
            Block size
        X: int
            Number of blocks.
        n: int, optional
            Add n zeros to each block.

    Returns:
        LazyLinOp

    Raises:
        ValueError
            Invalid block size and/or number of blocks.

    Examples:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> x = np.full(5, 1.0)
        >>> x
        array([1., 1., 1., 1., 1.])
        >>> lz.mpad(1, 5, 1) @ x
        array([1., 0., 1., 0., 1., 0., 1., 0., 1., 0.])
    """
    from lazylinop import eye
    if n <= 0:
        # reproducing mpad behaviour
        # (but is that really necessary? why a negative padding size?)
        return eye(X * L, X * L, k=0)
    P = ppadder((X, L), ((0, 0), (0, n)), impl='nokron')

    def matmat(x):
        nonlocal P
        ndim = len(x.shape)  # do not use x.ndim in case it is not defined
        if ndim == 1 or x.shape[1] == 1:
            px = P @ x.reshape((X, L))
            return px.ravel() if ndim == 1 else px.reshape(-1,
                                                           1)
        elif ndim == 2:
            xncols = x.shape[1]
            ncols = L * xncols
            mP = ppadder((X, L * x.shape[1]), ((0, 0), (0, n * xncols)),
                         impl='nokron')
            return (mP @ x.reshape(X, ncols)).reshape(-1, xncols)
        # else:  x.ndim >= 3 is handled directly in LazyLinOp

    def rmatmat(x):
        nonlocal P
        ndim = len(x.shape)  # do not use x.ndim in case it is not defined
        if ndim == 1:
            return P.H @ x
        elif ndim == 2:
            xncols = x.shape[1]
            mP = ppadder((X, L * x.shape[1]), ((0, 0), (0, n * xncols)),
                         impl='nokron')
            return (mP.H @ x.ravel()).reshape(-1, x.shape[1])
        # else:  x.ndim >= 3 is handled directly in LazyLinOp

    return LazyLinOp(
        shape=(X * (L + n), X * L),
        # it works the same with matvec and rmatvec but it would be slower for
        # x a matrix (LazyLinOp loops on matvec to compute LazyLinOp @ M)
        #        matvec=lambda x: (P @ x.reshape((X, L))).ravel(),
        #        rmatvec=lambda x: (P.H @ x.ravel())
        matmat=matmat,
        rmatmat=rmatmat
    )


def mpad(L: int, X: int, n: int = 1, add: str = 'after'):
    """Returns a :py:class:`LazyLinOp` to zero-pad each signal block.

    If you apply this operator to a vector of length L * X the output will have
    a length (L + n) * X.

    Args:
        L: int
            Block size
        X: int
            Number of blocks.
        n: int, optional
            Add n zeros to each block.
        add: str, optional
            If ``add='after'`` add ``n`` zeros after the block.
            If ``add='before'`` add ``n`` zeros before the block.
            Default value is ``'after'``.

    Returns:
        LazyLinOp

    Examples:
        >>> import lazylinop as lz
        >>> import numpy as np
        >>> x = np.full(3, 1.0)
        >>> x
        array([1., 1., 1.])
        >>> lz.mpad(1, 3, 1) @ x
        array([1., 0., 1., 0., 1., 0.])
        >>> lz.mpad(1, 3, 1, add='before') @ x
        array([0., 1., 0., 1., 0., 1.])
    """

    if n <= 0:
        return eye(X * L, X * L, k=0)

    if add == 'after':
        return kron(eye(X), eye(L + n, L))
    elif add == 'before':
        return kron(eye(X), eye(n + L, L, k=-n))
    else:
        raise Exception("add must be either after or before.")
