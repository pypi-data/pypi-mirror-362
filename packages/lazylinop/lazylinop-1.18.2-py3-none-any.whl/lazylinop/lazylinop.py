"""
This module defines the general lazy linear operator and basic specializations.
It provides also utility functions.
"""

import numpy as np
from scipy.sparse.linalg import LinearOperator
import array_api_compat
from array_api_compat import (
    is_array_api_obj, is_cupy_array, is_torch_array)
from array_api_compat import array_namespace as _array_namespace
from array_api_compat import device as _device
from array_api_compat import size as _size
try:
    from cupyx.scipy.sparse import issparse as _iscxsparse
except ModuleNotFoundError:
    def _iscxsparse(x):
        return False
from scipy.sparse import issparse
from typing import Union
HANDLED_FUNCTIONS = {'ndim'}


class LazyLinOp(LinearOperator):
    """
    The ``LazyLinOp`` class is a specialization of a
    `scipy.linalg.LinearOperator <https://docs.scipy.org/
    doc/scipy/reference/generated/scipy.sparse.linalg.LinearOperator.html>`_.

    .. admonition:: The lazy principle
        :class: admonition note

        The evaluation of any defined operation on a ``LazyLinOp`` is
        delayed until a multiplication by a matrix/vector or a call of
        :py:func:`LazyLinOp.toarray` is made.


    .. admonition:: Two ways to instantiate
        :class: admonition note

        - Using :py:func:`lazylinop.aslazylinop` or
        - Using this constructor (:py:func:`lazylinop.LazyLinOp`) to define
          ``matmat``, ``matvec`` functions.

    .. admonition:: Available operations
        :class: admonition note

        ``+`` (addition), ``-`` (subtraction),
        ``@`` (matrix product), ``*`` (scalar multiplication),
        ``**`` (matrix power for square operators),
        indexing, slicing and others.
        For a nicer introduction you might look at `these tutorials
        <https://faustgrp.gitlabpages.inria.fr/lazylinop/tutorials.html>`_.

    .. admonition:: Recursion limit
        :class: admonition warning

        Repeated "inplace" modifications of a :py:class:`LazyLinOp`
        through any operation like a concatenation
        (``op = vstack((op, anything))``)
        are subject to a :py:class:`RecursionError` if the number of recursive
        calls exceeds :py:func:`sys.getrecursionlimit`. You might change this
        limit if needed using :py:func:`sys.setrecursionlimit`.
    """

    def __init__(self, shape, matvec=None, matmat=None, rmatvec=None,
                 rmatmat=None, dtype=None, **kwargs):
        """
        A ``LazyLinOp`` instance is defined by a shape and at least
        a function ``matvec`` or ``matmat``.
        Additionally the functions ``rmatvec`` and ``rmatmat`` can be
        defined through the following parameters.


        Parameters
        ----------
            shape: (``tuple[int, int]``)
                 Operator $L$ dimensions $(M, N)$.
            matvec: (callable)
                 Returns $y = L * v$ with $v$ a vector of size $N$.
                 $y$ size is $M$ with the same number of dimension(s) as $v$.
            rmatvec: (callable)
                 Returns $y = L^H * v$ with $v$ a vector of size $M$.
                 $y$ size is $N$ with the same number of dimension(s) as $v$.
            matmat: (callable)
                 Returns $L * V$.
                 The output matrix shape is $(M, K)$.
            rmatmat: (``callable``)
                 Returns $L^H * V$.
                 The output matrix shape is $(N, K)$.
            dtype: (numpy ``dtype`` or ``NoneType``)
                 Data type of the ``LazyLinOp`` (default is ``None``).
                 Only used for LazyLinops created from arrays
                 ``L = aslazylinop(array)``, in which case
                 ``L.dtype = array.dtype``.
                 All other lazylinops have ``dtype = None``.

        .. admonition:: Auto-implemented operations
            :class: admonition note

            - If only ``matvec`` is defined and not ``matmat``, an
              automatic naive ``matmat`` will be defined upon the given
              ``matvec`` but note that it might be suboptimal (in which
              case a ``matmat`` is useful).
            - No need to provide the implementation of the multiplication by a
              :class:`LazyLinOp`, or a numpy array with ``ndim > 2`` because
              both of them are auto-implemented. For the latter operation,
              it is computed as in `numpy.__matmul__ <https://numpy.org/
              doc/stable/reference/generated/numpy.matmul.html>`_.


        Return:
            ``LazyLinOp``

        Example:
            >>> # In this example we create a LazyLinOp
            >>> # for the DFT using the fft from scipy
            >>> import numpy as np
            >>> from scipy.fft import fft, ifft
            >>> from lazylinop import LazyLinOp
            >>> fft_mm = lambda x: fft(x, norm='ortho')
            >>> fft_rmm = lambda x: ifft(x, norm='ortho')
            >>> n = 16
            >>> F = LazyLinOp((n, n), matvec=fft_mm, rmatvec=fft_rmm)
            >>> x = np.random.rand(n)
            >>> y = F * x
            >>> np.allclose(y, fft(x, norm='ortho'))
            True
            >>> np.allclose(x, F.H * y)
            True

        .. seealso::
            `SciPy linear Operator
            <https://docs.scipy.org/doc/scipy/reference/generated/
            scipy.sparse.linalg.LinearOperator.html>`_.
            :py:func:`LazyLinOp.check`
            `scipy fft
            <https://docs.scipy.org/doc/scipy/reference/generated/
            scipy.fft.fft.html>`_
        """
        if 'internal_call' in kwargs and kwargs['internal_call']:
            self.shape = shape
            self.dtype = dtype
            super(LazyLinOp, self).__init__(self.dtype, self.shape)
            return

        def check_matfunc(f, fn):
            if f is not None and not callable(f):
                raise TypeError(f+' must be a callable/function')

        for fn in ['matvec', 'rmatvec', 'matmat', 'rmatmat']:
            f = eval(fn)
            check_matfunc(f, fn)

        if matvec is None and matmat is None:
            raise ValueError('At least a matvec or a matmat function must be'
                             ' passed to the constructor.')

        def _matmat(M, _matvec, shape):
            # M is always 2d
            nonlocal dtype
            xp = _array_namespace(M)
            if M.shape[1] == 1:
                return _matvec(M.ravel()).reshape(-1, 1)
            first_col = _matvec(M[:, 0])
            dtype = first_col.dtype
            out = xp.empty((shape[0], M.shape[1]), dtype=dtype,
                           device=first_col.device)
            out[:, 0] = first_col
            for i in range(1, M.shape[1]):
                out[:, i] = _matvec(M[:, i])
            return out

        if matmat is None:
            def matmat(M): return _matmat(M, matvec, shape)

        if rmatmat is None and rmatvec is not None:
            def rmatmat(M): return _matmat(M, rmatvec, (shape[1], shape[0]))

        # MX = lambda X: matmat(np.eye(shape[1])) @ X
        def MX(X): return matmat(X)
        # MTX = lambda X: rmatmat(X.T).T
        def MHX(X): return rmatmat(X)

        def MTX(X):
            # computes L.T @ X # L LazyLinOp, X anything compatible
            L_possibly_cplx = 'complex' in str(dtype) or dtype is None
            X_possibly_cplx = 'complex' in str(X.dtype) or X.dtype is None
            if L_possibly_cplx:
                if X_possibly_cplx:
                    if is_array_api_obj(X) and is_torch_array(X):
                        # Torch does not support multiplication of
                        # two tensors with different dtype.
                        return (
                            rmatmat(X.real.to(dtype=X.dtype)).conj()
                            - rmatmat((1j * X.imag).to(dtype=X.dtype)).conj())
                    else:
                        return rmatmat(X.real).conj() - rmatmat(1j * X.imag).conj()
                else:
                    # X is real
                    return rmatmat(X).conj()
            else:  # L is real
                return rmatmat(X)

        def MCX(X):
            # computes L.conj() @ X # L LazyLinOp, X anything compatible
            L_possibly_cplx = 'complex' in str(dtype) or dtype is None
            X_possibly_cplx = 'complex' in str(X.dtype) or X.dtype is None
            if L_possibly_cplx:
                if X_possibly_cplx:
                    if is_array_api_obj(X) and is_torch_array(X):
                        # Torch does not support multiplication of
                        # two tensors with different dtype.
                        return (
                            matmat(X.real.to(dtype=X.dtype)).conj()
                            - matmat((1j * X.imag).to(dtype=X.dtype)).conj())
                    else:
                        return matmat(X.real).conj() - matmat(1j * X.imag).conj()
                else:
                    # X is real
                    return matmat(X).conj()
            else:  # L is real
                return MX(X)

        lambdas = {'@': MX}
        lambdasT = {'@': MTX}
        lambdasH = {'@': MHX}
        lambdasC = {'@': MCX}
        # set lambdas temporarily to None (to satisfy the ctor)
        # they'll be initialized later
        for func in [lambdas, lambdasT, lambdasH, lambdasC]:
            func['T'] = None
            func['H'] = None
            func['slice'] = None

        lop = LazyLinOp._create_LazyLinOp(lambdas, shape,
                                          dtype=dtype,
                                          self=self)
        super(LazyLinOp, lop).__init__(lop.dtype, lop.shape)
        lopT = LazyLinOp._create_LazyLinOp(
            lambdasT, (shape[1], shape[0]), dtype=dtype)
        super(LazyLinOp, lopT).__init__(lopT.dtype, lopT.shape)
        lopH = LazyLinOp._create_LazyLinOp(
            lambdasH, (shape[1], shape[0]), dtype=dtype)
        super(LazyLinOp, lopH).__init__(lopH.dtype, lopH.shape)
        lopC = LazyLinOp._create_LazyLinOp(lambdasC, shape, dtype=dtype)
        super(LazyLinOp, lopC).__init__(lopC.dtype, lopC.shape)

        LazyLinOp._set_matching_lambdas(
            lambdas, lambdasT, lambdasH,
            lambdasC, lop, lopT, lopH, lopC)
        self = lop

    @staticmethod
    def _create_LazyLinOp(lambdas, shape, root_obj=None, dtype=None,
                          self=None):
        """
        Low-level constructor. Not meant to be used directly.

        Args:
            lambdas: starting operations.
            shape: (``tuple[int, int]``)
                the initial shape of the operator.
            root_obj: the initial object the operator is based on.

        .. seealso:: :py:func:`lazylinop.aslazylinop`.
        """
        if root_obj is not None:
            if not hasattr(root_obj, 'shape'):
                raise TypeError('The starting object to initialize a'
                                ' LazyLinOp must possess a shape'
                                ' attribute.')
            if len(root_obj.shape) != 2:
                raise ValueError('The starting object to initialize'
                                 ' a LazyLinOp must have two dimensions,'
                                 ' not: '+str(len(root_obj.shape)))

        if self is None:
            self = LazyLinOp(shape, dtype=dtype, internal_call=True)
        else:
            self.shape = shape
            self.dtype = dtype
        self.lambdas = lambdas
        self._check_lambdas()
        self._root_obj = root_obj
        return self

    def _check_lambdas(self):
        """
        Internal function for checking self.lambdas is well-formed
        (dict type and proper keys).
        """
        if not isinstance(self.lambdas, dict):
            raise TypeError('lambdas must be a dict')
        keys = self.lambdas.keys()
        for k in ['@', 'H', 'T', 'slice']:
            if k not in keys:
                raise ValueError(k+' is a mandatory lambda, it must be set in'
                                 ' self.lambdas')

    @staticmethod
    def _create_from_op(obj, shape=None):
        """
        See :py:func:`lazylinop.aslazylinop`.
        """
        if shape is None:
            oshape = obj.shape
        else:
            oshape = shape
        lambdas = {'@': lambda op: obj @ op}
        lambdasT = {'@': lambda op: obj.T @ op}
        lambdasH = {'@': lambda op: obj.T.conj() @ op}
        # obj might not have a conj method
        # e.g. scipy.sparse.linalg._interface.IdentityOperator
        if hasattr(obj, 'conj') and hasattr(obj.T, 'conj'):
            lambdasH = {'@': lambda op: obj.T.conj() @ op}
            lambdasC = {'@': lambda op:
                        obj.conj() @ op if 'complex' in
                        str(obj.dtype) or obj.dtype is None
                        else obj @ op}
        elif hasattr(obj, 'T') and hasattr(obj, 'H'):
            lambdasH = {'@': lambda op: obj.H @ op}
            lambdasC = {'@': lambda op:
                        obj.H.T() @ op if 'complex' in
                        str(obj.dtype) or obj.dtype is None
                        else obj @ op}
        else:
            raise TypeError('Cannot create a LazyLinOp from object that has'
                            ' neither conj() method nor T and H'
                            ' attributes.')

        # set lambdas temporarily to None (to satisfy the ctor)
        # they'll be initialized later
        for func in [lambdas, lambdasT, lambdasH, lambdasC]:
            func['T'] = None
            func['H'] = None
            func['slice'] = None  # TODO: rename slice to index

        lop = LazyLinOp._create_LazyLinOp(lambdas,
                                          oshape,
                                          obj,
                                          dtype=None)
        lopT = LazyLinOp._create_LazyLinOp(lambdasT,
                                           (oshape[1], oshape[0]),
                                           obj,
                                           dtype=None)
        lopH = LazyLinOp._create_LazyLinOp(lambdasH,
                                           (oshape[1], oshape[0]),
                                           obj,
                                           dtype=None)
        lopC = LazyLinOp._create_LazyLinOp(lambdasC, oshape, obj,
                                           dtype=None)

        LazyLinOp._set_matching_lambdas(
            lambdas, lambdasT, lambdasH, lambdasC,
            lop, lopT, lopH, lopC)

        return lop

    @staticmethod
    def _set_matching_lambdas(lambdas, lambdasT, lambdasH, lambdasC,
                              lop, lopT, lopH, lopC):
        """
        Internal function.
        Set the corresponding relations for operations/LazyLinOp-s.
        """
        lambdas['T'] = lambda: lopT
        lambdas['H'] = lambda: lopH
        lambdas['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lop, indices)())
        lambdasT['T'] = lambda: lop
        lambdasT['H'] = lambda: lopC
        lambdasT['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopT, indices)())
        lambdasH['T'] = lambda: lopC
        lambdasH['H'] = lambda: lop
        lambdasH['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopH, indices)())
        lambdasC['T'] = lambda: lopH
        lambdasC['H'] = lambda: lopT
        lambdasC['slice'] = lambda indices: (
            LazyLinOp._index_lambda(lopC, indices)())

    @staticmethod
    def _create_from_scalar(s, shape):
        """
        Returns a :class:`LazyLinOp` ``L`` created scalar ``s``.

        ``L`` is such that ``l @ x == s * x``
        """
        if not np.isscalar(s):
            raise TypeError('s must be a scalar')

        def matmat(M): return M * s

        def rmatmat(M):
            return M * np.conj(s)  # or s.conjugate() ?

        return LazyLinOp(shape, matmat=matmat,
                         rmatmat=rmatmat,
                         dtype=np.asarray(s).dtype)

    def _checkattr(self, attr):
        if self._root_obj is not None and not hasattr(self._root_obj, attr):
            raise TypeError(attr+' is not supported by the root object of this'
                            ' LazyLinOp')

    def _slice_to_indices(self, s, axis):
        step = s.step
        if step is None:
            step = 1
        if step == 0:
            raise ValueError('slice step cannot be zero')
        start = s.start
        stop = s.stop
        if start is None:
            if step > 0:
                start = 0
            else:
                if stop is not None:
                    if stop >= 0:
                        start = self.shape[axis] - 1
                    else:
                        start = - self.shape[axis]
                else:
                    start = self.shape[axis] - 1
        # start is not None
        if stop is None:
            if step > 0:
                if start >= 0:
                    stop = self.shape[axis]
                else:
                    # start < 0
                    start = self.shape[axis] + start
                    stop = self.shape[axis]
            else:
                # step < 0
                if start >= 0:
                    stop = -1
                else:
                    stop = - self.shape[axis] - 1
        if start < 0 and stop < 0 and step > 0:
            start = self.shape[axis] + start
            stop = self.shape[axis] + stop - 1
        return np.arange(start, stop, step)

    def _index_lambda(self, indices):

        def s():
            _indices = [None, None]
            if isinstance(indices, slice):
                _indices[0] = self._slice_to_indices(indices, 0)
                _indices[1] = np.arange(self.shape[1])
            else:
                for i in range(2):
                    s = indices[i]
                    if isinstance(s, slice):
                        _indices[i] = self._slice_to_indices(s, i)
                    elif isinstance(s, int):
                        _indices[i] = np.arange(s, s+1)
                    else:
                        _indices[i] = indices[i]
            n0, n1 = len(_indices[0]), len(_indices[1])
            return (
                _seye(self.shape[0], v=_indices[0])
                @ self
                @ _seye(self.shape[1], v=_indices[1]).T
            )
        return s

    @property
    def _shape(self):
        """
        The shape (``tuple[int, int]``) of the :class:`LazyLinOp`.
        """
        return self.shape

    @property
    def ndim(self):
        """
        The number of dimensions of the :class:`LazyLinOp`
        (it is always 2).
        """
        return 2

    def transpose(self):
        """
        Returns the :class:`LazyLinOp` transpose.
        """
        self._checkattr('transpose')
        return self.lambdas['T']()

    @property
    def T(self):
        """
        The :py:class:`LazyLinOp` transpose.
        """
        return self.transpose()

    def _transpose(self):
        """
        Alias of :py:func:`lazylinop.transpose`.
        """
        return self.transpose()

    def conj(self):
        """
        Returns the :py:class:`LazyLinOp` conjugate.
        """
        self._checkattr('conj')
        return self.H.T

    def conjugate(self):
        """
        Returns the :py:class:`LazyLinOp` conjugate.
        """
        return self.conj()

    def getH(self):
        """
        Returns the :py:class:`LazyLinOp` adjoint/transconjugate.
        """
        # self._checkattr('getH')
        return self.lambdas['H']()

    @property
    def H(self):
        """
        The :py:class:`LazyLinOp` adjoint/transconjugate.
        """
        return self.getH()

    def _adjoint(self):
        """
        Returns the LazyLinOp adjoint/transconjugate.
        """
        return self.H

    def _slice(self, indices):
        return self.lambdas['slice'](indices)

    def __add__(self, op):
        """
        Returns the LazyLinOp for self + op.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__add__')
        if not LazyLinOp.islazylinop(op):
            if np.isscalar(op):
                from lazylinop import ones
                if op == 0:
                    return self
                else:
                    op = ones(self.shape) * op
            else:
                op = LazyLinOp._create_from_op(op)
        if op.shape != self.shape:
            raise ValueError('Dimensions must agree')
        lambdas = {'@': lambda o: self @ o + op @ o,
                   'H': lambda: self.H + op.H,
                   'T': lambda: self.T + op.T,
                   'slice': lambda indices:
                   self._slice(indices) + op._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=tuple(self.shape),
            # dtype=binary_dtype(self.dtype, op.dtype),
            dtype=None,
            root_obj=None)
        return new_op

    def __radd__(self, op):
        """
        Returns the LazyLinOp for op + self.

        Args:
            op: an object compatible with self for this binary operation.

        """
        return self.__add__(op)

    def __iadd__(self, op):
        """
        Not Implemented self += op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__iadd__")

    def __sub__(self, op):
        """
        Returns the LazyLinOp for self - op.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__sub__')
        if not LazyLinOp.islazylinop(op):
            if np.isscalar(op):
                from lazylinop import ones
                if op == 0:
                    return self
                else:
                    op = ones(self.shape) * op
            else:
                op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self @ o - op @ o,
                   'H': lambda: self.H - op.H,
                   'T': lambda: self.T - op.T,
                   'slice': lambda indices:
                   self._slice(indices) - op._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=tuple(self.shape),
            # dtype=binary_dtype(self.dtype, op.dtype),
            dtype=None,
            root_obj=None)
        return new_op

    def __rsub__(self, op):
        """
        Returns the LazyLinOp for op - self.

        Args:
            op: an object compatible with self for this binary operation.

        """
        self._checkattr('__rsub__')
        if not LazyLinOp.islazylinop(op):
            if np.isscalar(op):
                from lazylinop import ones
                if op == 0:
                    return self * -1
                else:
                    op = ones(self.shape) * op
            else:
                op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: op @ o - self @ o,
                   'H': lambda: op.H - self.H,
                   'T': lambda: op.T - self.T,
                   'slice': lambda indices:
                   op._slice(indices) - self._slice(indices)}
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=self.shape,
            # dtype=binary_dtype(self.dtype, op.dtype),
            dtype=None,
            root_obj=None)
        return new_op

    def __isub__(self, op):
        """
        Not implemented self -= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__isub__")

    def __truediv__(self, s):
        """
        Returns the LazyLinOp for self / s.

        Args:
            s: a scalar.

        """
        new_op = self * (1/s)
        return new_op

    def __itruediv__(self, op):
        """
        Not implemented self /= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__itruediv__")

    def __idiv__(self, op):
        """
        Not implemented self //= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__idiv__")

    def _sanitize_matmul(self, op, swap=False):
        self._checkattr('__matmul__')
        sanitize_op(op)
        dim_err = ValueError('dimensions must agree')
        if (hasattr(self, 'ravel_op') and self.ravel_op and
                len(op.shape) >= 2):
            # see lazylinop.pad
            # array flattening is authorized for self LazyLinOp
            if ((not swap and
                 self.shape[1] != op.shape[-2] and
                 np.prod(op.shape) != self.shape[1])
                or
                (swap and self.shape[0] != op.shape[-2] and
                 np.prod(op.shape) != self.shape[0])):
                raise dim_err
            return  # flattened op is compatible to self
            # TODO: it should be made more properly
        if (len(op.shape) == 1 and
            self.shape[(int(swap) + 1) % 2] != op.shape[-1]
            or
            len(op.shape) >= 2 and
            (swap and op.shape[-1] != self.shape[0] or
             not swap and self.shape[1] != op.shape[-2])):
            raise dim_err

    def __matmul__(self, op):
        """
        Computes self @ op.

        Args:
            op: an object compatible with self for this binary operation.

        Returns:
            If op is an numpy array or a scipy matrix the function returns
            (``self @ op``) as a numpy array or a scipy matrix. Otherwise
            it returns the :class:`LazyLinOp` for the multiplication
            ``self @ op``.

        """
        self._sanitize_matmul(op)
        sanitize_op(op)
        if is_array_api_obj(op) or issparse(op) or _iscxsparse(op):
            if op.ndim == 2:
                res = self.lambdas['@'](op)
            else:
                if issparse(op):
                    import array_api_compat.numpy as xp
                elif _iscxsparse(op):
                    import array_api_compat.cupy as xp
                else:
                    xp = _array_namespace(op)
                if op.ndim == 1:
                    # hasattr(op, 'reshape') == True
                    # because op is a np.ndarray
                    # (scipy matrix => ndim != 1)
                    res = xp.ravel(self.lambdas['@'](
                        xp.reshape(op, (_size(op), 1))))
                elif op.ndim > 2:
                    from itertools import product
                    # op.ndim > 2
                    dtype = _binary_dtype(self.dtype, op.dtype)
                    res = xp.empty(
                        (*op.shape[:-2], self.shape[0], op.shape[-1]),
                        dtype=dtype)
                    idl = [list(range(op.shape[i])) for i in range(op.ndim-2)]
                    for t in product(*idl):
                        tr = (*t,
                              slice(0, res.shape[-2]), slice(0, res.shape[-1]))
                        to = (*t,
                              slice(0, op.shape[-2]), slice(0, op.shape[-1]))
                        R = self.lambdas['@'](op.__getitem__(to))
                        res.__setitem__(tr, R)
                    # parallelization would not necessarily be faster because
                    # successive 2d multiplications might themselves be
                    # parallelized
        else:
            if not LazyLinOp.islazylinop(op):
                op = LazyLinOp._create_from_op(op)
            lambdas = {'@': lambda o: self @ (op @ o),
                       'H': lambda: op.H @ self.H,
                       'T': lambda: op.T @ self.T,
                       'slice': lambda indices:
                       self._slice((indices if isinstance(indices, slice)
                                    else indices[0], slice(0, self.shape[1])))
                       @ op._slice((slice(0, op.shape[0]), indices[1]
                                   if hasattr(indices, "__len__") and
                                    len(indices) > 1
                                   else slice(0, self.shape[1])))}
            res_shape = (self.shape[0], op.shape[1])
            res = LazyLinOp._create_LazyLinOp(
                lambdas=lambdas,
                shape=res_shape,
                root_obj=None,
                # dtype=binary_dtype(self.dtype, op.dtype),
                dtype=None)
            # res = LazyLinOp._create_from_op(super(LazyLinOp,
            #                                       self).__matmul__(op))
        return res

    def dot(self, op):
        """
        Alias of LazyLinOp.__matmul__.
        """
        return self.__matmul__(op)

    def matvec(self, op):
        """
        This function is an alias of self @ op, where the multiplication might
        be specialized for op a vector (depending on how self has been defined
        ; upon on a operator object or through a matvec/matmat function).


        .. seealso:: lazylinop.LazyLinOp.
        """
        sanitize_op(op)
        if op.ndim != 1 and op.shape[0] != 1 and op.shape[1] != 1:
            raise ValueError('op must be a vector -- attribute ndim to 1 or'
                             ' shape[0] or shape[1] to 1')
        return self.__matmul__(op)

    def _rmatvec(self, op):
        """
        Returns self^H @ op, where self^H is the conjugate transpose of A.

        Returns:
            It might be a LazyLinOp or an array depending on the op type
            (cf. lazylinop.LazyLinOp.__matmul__).
        """
        # LinearOperator need.
        return self.T.conj() @ op

    def _matmat(self, op):
        """
        Alias of LazyLinOp.__matmul__.
        """
        return self.__matmul__(op)

    def _rmatmat(self, op):
        """
        Returns self^H @ op, where self^H is the conjugate transpose of A.

        Returns:
            It might be a LazyLinOp or an array depending on the op type
            (cf. lazylinop.LazyLinOp.__matmul__).
        """
        # LinearOperator need.
        return self.T.conj() @ op

    def __imatmul__(self, op):
        """
        Not implemented self @= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__imatmul__")

    def __rmatmul__(self, op):
        """
        Returns op @ self.

        Args:
            op: an object compatible with self for this binary operation.

        Returns:
            a :class:`LazyLinOp` or an array depending on op type.

        .. seealso::
            :py:func:`LazyLinOp.__matmul__`
        """
        self._checkattr('__rmatmul__')
        self._sanitize_matmul(op, swap=True)
        if is_array_api_obj(op) or issparse(op) or _iscxsparse(op):
            res = (self.H @ op.T.conj()).T.conj()
        else:
            # this code doesn't make sense because:
            # - either op has implemented __matmul__ and then
            # it would have been called on op @ something/LazyLinOp
            # - or op hasn't __matmul__ implemented and we end up here but
            # the lambdas['@'] below relies on __matmul__ so it would fail
            # anyway

            # if not LazyLinOp.islazylinop(op):
            # op = LazyLinOp._create_from_op(op)
            # lambdas = {'@': lambda o: (op @ self) @ o,
            # 'H': lambda: self.H @ op.H,
            # 'T': lambda: self.T @ op.T,
            # 'slice': lambda indices: (op @ self)._slice(indices)}
            # res_shape = (op.shape[0], self.shape[1])
            # res = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
            # shape=res_shape,
            # root_obj=None)
            raise TypeError(str(op)+" has no __matmul__ operation.")
        return res

    def __mul__(self, other):
        """
        Returns the LazyLinOp for self * other if other is a scalar
        otherwise returns self @ other.

        Args:
            other: a scalar or a vector/array.

        .. seealso:: lazylinop.LazyLinOp.__matmul__)
        """
        self._checkattr('__mul__')
        if np.isscalar(other):
            if other == 1:
                new_op = self
            else:
                Dshape = (self.shape[1], self.shape[1])
                new_op = self @ LazyLinOp._create_from_scalar(other, Dshape)
        else:
            new_op = self @ other
        return new_op

    def __rmul__(self, other):
        """
        Returns other * self.

        Args:
            other: a scalar or a vector/array.

        """
        if np.isscalar(other):
            return self * other
        else:
            return other @ self

    def __imul__(self, op):
        """
        Not implemented self *= op.
        """
        raise NotImplementedError(LazyLinOp.__name__+".__imul__")

    def toarray(self, dtype: str = None, array_namespace=np, device: str = None):
        """
        Computes ``y = self @ array_namespace.eye(self.shape[1], dtype=dtype)``
        with smallest possible ``dtype`` and returns self as a
        NumPy/CuPy array or torch tensor.
        ``dtype`` of the output ``y`` depends on
        the :class:`LazyLinOp` instance ``self``.

        Args:
            dtype: ``str``, optional
                Use ``dtype`` to compute
                ``y = self @ array_namespace.eye(self.shape[1], dtype=dtype)``.
                Default value is ``None`` and corresponds to the
                smallest possible dtype.
            array_namespace: ``namespace``, optional

                - NumPy namespace uses ``numpy.eye(...)``.
                  This is the default value.
                - CuPy namespace uses ``cupy.eye(...)``.
                - torch namespace uses ``torch.eye(...)``.
            device: ``str``, optional
                Use ``device`` to compute
                ``y = self @ xp.eye(self.shape[1], device=device)``.
                Default value is ``None``.
                ``device`` has no effect if ``lib`` is not
                equal to ``'torch'``.

        Examples:
            >>> import numpy as np
            >>> from lazylinop import aslazylinop
            >>> L = aslazylinop(np.eye(2, dtype='int'))
            >>> L.toarray(array_namespace=np, dtype='float')
            array([[1., 0.],
                   [0., 1.]])
        """
        # FIXME: do we really need to build complete eye matrix ?
        # At this point we do not know if self is built from a torch.Tensor.
        if hasattr(self, '_dtype'):
            _dtype = self._dtype
        else:
            _dtype = dtype
        if 'torch' in str(array_namespace.__package__):
            if _dtype is not None:
                return self @ array_namespace.eye(
                    self.shape[1], dtype=_dtype, device=device)
            else:
                # Loop over torch.dtype to match with self.
                for t in [array_namespace.int32,
                          array_namespace.int64,
                          array_namespace.float16,
                          array_namespace.bfloat16,
                          array_namespace.float32,
                          array_namespace.float64,
                          array_namespace.complex64,
                          array_namespace.complex128]:
                    try:
                        return self @ array_namespace.eye(
                            self.shape[1], dtype=t, device=device)
                    except RuntimeError:
                        pass
        elif 'cupy' in str(array_namespace.__package__):
            return self @ array_namespace.eye(
                self.shape[1], order='F',
                dtype='int8' if dtype is None else dtype)
        else:
            return self @ array_namespace.eye(
                self.shape[1], order='F',
                dtype='int8' if dtype is None else dtype)

    def __getitem__(self, indices):
        """
        Returns the LazyLinOp for slicing/indexing.

        Args:
            indices:
                array of length 1 or 2 which elements must be slice, integer or
                Ellipsis (...). Note that using Ellipsis for more than two
                indices is normally forbidden.

        """
        self._checkattr('__getitem__')
        if isinstance(indices, int):
            indices = (indices, slice(0, self.shape[1]))
        if (isinstance(indices, tuple) and len(indices) == 2 and
                isinstance(indices[0], int) and isinstance(indices[1], int)):
            return self.toarray().__getitem__(indices)
        elif isinstance(indices, slice) or isinstance(indices[0], slice) and \
                isinstance(indices[0], slice):
            return self._slice(indices)
        else:
            return self._slice(indices)

    def concatenate(self, *ops, axis=0):
        """
        Returns the LazyLinOp for the concatenation of self and op.

        Args:
            axis: axis of concatenation (0 for rows, 1 for columns).
        """
        out = self
        for op in ops:
            if axis == 0:
                out = out.vstack(op)
            elif axis == 1:
                out = out.hstack(op)
            else:
                raise ValueError('axis must be 0 or 1')
        return out

    def _vstack_slice(self, op, indices):
        rslice = indices[0]
        if isinstance(rslice, int):
            rslice = slice(rslice, rslice+1, 1)
        if rslice.step is not None and rslice.step != 1:
            raise ValueError('Can\'t handle non-contiguous slice -- step > 1')
        if rslice.start is None:
            rslice = slice(0, rslice.stop, rslice.step)
        if rslice.stop is None:
            rslice = slice(rslice.start, self.shape[0] + op.shape[0],
                           rslice.step)
        if rslice.stop > self.shape[0] + op.shape[0]:
            raise ValueError('Slice overflows the row dimension')
        if rslice.start >= 0 and rslice.stop <= self.shape[0]:
            # the slice is completly in self
            return lambda: self._slice(indices)
        elif rslice.start >= self.shape[0]:
            # the slice is completly in op
            return lambda: op._slice((slice(rslice.start - self.shape[0],
                                            rslice.stop - self.shape[0]),
                                      indices[1]))
        else:
            # the slice is overlapping self and op
            self_slice = self._slice((slice(rslice.start, self.shape[0]),
                                      indices[1]))
            op_slice = op._slice((slice(0, rslice.stop - self.shape[0]),
                                  indices[1]))
            return lambda: self_slice.vstack(op_slice)

    def _vstack_mul_lambda(self, op, o):

        # def mul_mat(o):
        #     xp = _array_namespace(o)
        #     return xp.vstack((self @ o, op @ o))

        # def mul_vec(o):
        #     # self.shape[1] == op.shape[1] == vcat(self, op).shape[1]
        #     return mul_mat(o.reshape(self.shape[1], 1)).ravel()

        # def mul_mat_vec():
        #     return mul_vec(o) if len(o.shape) == 1 else mul_mat(o)

        def mul():
            if is_array_api_obj(o) or issparse(o) or _iscxsparse(o):
                if issparse(o):
                    import array_api_compat.numpy as xp
                elif _iscxsparse(o):
                    import array_api_compat.cupy as xp
                else:
                    xp = _array_namespace(o)
                if len(o.shape) == 1:
                    tmp_o = o.reshape(self.shape[1], 1)
                    return xp.vstack((self @ tmp_o, op @ tmp_o)).ravel()
                else:
                    return xp.vstack((self @ o, op @ o))
            else:
                return self.vstack(op) @ o

        return mul

    def vstack(self, op):
        """
        See lazylinop.vstack.
        """
        if self.shape[1] != op.shape[1]:
            raise ValueError('self and op numbers of columns must be the'
                             ' same')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self._vstack_mul_lambda(op, o)(),
                   'H': lambda: self.H.hstack(op.H),
                   'T': lambda: self.T.hstack(op.T),
                   'slice': lambda indices: self._vstack_slice(op, indices)()}
        new_shape = (self.shape[0] + op.shape[0], self.shape[1])
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=new_shape,
            root_obj=None,
            # dtype=binary_dtype(self.dtype, op.dtype),
            dtype=None)
        return new_op

    def _hstack_slice(self, op, indices):
        cslice = indices[1]
        if isinstance(cslice, int):
            cslice = slice(cslice, cslice+1, 1)
        if cslice.step is not None and cslice.step != 1:
            raise ValueError('Can\'t handle non-contiguous slice -- step > 1')
        if cslice.stop is None:
            cslice = slice(cslice.start, self.shape[1] + op.shape[1],
                           cslice.step)
        if cslice.start is None:
            cslice = slice(0, cslice.stop, cslice.step)
        if cslice.stop > self.shape[1] + op.shape[1]:
            raise ValueError('Slice overflows the row dimension')
        if cslice.start >= 0 and cslice.stop <= self.shape[1]:
            # the slice is completly in self
            return lambda: self._slice(indices)
        elif cslice.start >= self.shape[1]:
            # the slice is completly in op
            return lambda: op._slice((indices[0],
                                      slice(cslice.start - self.shape[1],
                                            cslice.stop - self.shape[1])))
        else:
            # the slice is overlapping self and op
            self_slice = self._slice((indices[0], slice(cslice.start,
                                                        self.shape[1])))
            op_slice = op._slice((indices[0], slice(0, cslice.stop -
                                                    self.shape[1])))
            return lambda: self_slice.hstack(op_slice)

    def _hstack_mul_lambda(self, op, o):

        # def mul_mat(o):
        #     s_ncols = self.shape[1]
        #     return self @ o[:s_ncols] + op @ o[s_ncols:]

        # def mul_vec(o):
        #     return mul_mat(o.reshape(op.shape[1] + self.shape[1], 1)).ravel()

        # def mul_mat_vec():
        #     return mul_vec(o) if len(o.shape) == 1 else mul_mat(o)

        def mul():
            if is_array_api_obj(o) or issparse(o) or _iscxsparse(o):
                if len(o.shape) == 1:
                    tmp_o = o.reshape(op.shape[1] + self.shape[1], 1)
                    s_ncols = self.shape[1]
                    return (self @ tmp_o[:s_ncols] + op @ tmp_o[s_ncols:]).ravel()
                else:
                    s_ncols = self.shape[1]
                    return self @ o[:s_ncols] + op @ o[s_ncols:]
            else:
                return self.hstack(op) @ o

        return mul

    def hstack(self, op):
        """
        See lazylinop.hstack.
        """
        if self.shape[0] != op.shape[0]:
            raise ValueError('self and op numbers of rows must be the'
                             ' same')
        if not LazyLinOp.islazylinop(op):
            op = LazyLinOp._create_from_op(op)
        lambdas = {'@': lambda o: self._hstack_mul_lambda(op, o)(),
                   'H': lambda: self.H.vstack(op.H),
                   'T': lambda: self.T.vstack(op.T),
                   'slice': lambda indices: self._hstack_slice(op, indices)()}
        new_op = LazyLinOp._create_LazyLinOp(
            lambdas=lambdas,
            shape=(self.shape[0], self.shape[1] + op.shape[1]),
            root_obj=None,
            # dtype=binary_dtype(self.dtype, op.dtype),
            dtype=None)
        return new_op

    @property
    def real(self):
        """
        The :py:class:`LazyLinOp` for real part of this
        :py:class:`LazyLinOp`.
        """
        lambdas = {'@': lambda o: (self @ o.real).real +
                   (self @ o.imag * 1j).real if is_array_api_obj(o) or issparse(o) or _iscxsparse(o) else (self @ o).real,
                   'H': lambda: self.T.real,
                   'T': lambda: self.T.real,
                   'slice': lambda indices: self._slice(indices).real}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    @property
    def imag(self):
        """
        The :py:class:`LazyLinOp` for the imaginary part of this
        :py:class:`LazyLinOp`.
        """
        lambdas = {'@': lambda o: (self @ o.real).imag +
                   (self @ (1j * o.imag)).imag if is_array_api_obj(o) or issparse(o) or _iscxsparse(o) else (self @ o).imag,
                   'H': lambda: self.T.imag,
                   'T': lambda: self.T.imag,
                   'slice': lambda indices: self._slice(indices).imag}
        new_op = LazyLinOp._create_LazyLinOp(lambdas=lambdas,
                                             shape=tuple(self.shape),
                                             root_obj=None)
        return new_op

    def __neg__(self):
        """
        Returns the negative ::py:class:`LazyLinOp` of self.

        Example:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12).astype('float32')
            >>> lM = aslazylinop(M)
            >>> -lM
            <10x12 LazyLinOp with unspecified dtype>
        """
        return self * -1

    def __pos__(self):
        """
        Returns the positive ::py:class:`LazyLinOp` of self.

        Example:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12).astype('float32')
            >>> lM = aslazylinop(M)
            >>> +lM
            <10x12 LazyLinOp with dtype=float32>
        """
        return self

    def __pow__(self, n):
        """
        Returns the :py:class:`LazyLinOp` for the n-th power of ``self``.

        - ``L**n == L @ L @ ... @ L`` (n-1 multiplications).

        Raises:
            The :py:class:`.LazyLinOp` is not square.

        Example:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 10).astype('float32')
            >>> lM = aslazylinop(M)
            >>> lM
            <10x10 LazyLinOp with dtype=float32>
            >>> np.allclose((lM**2).toarray(), M @ M)
            True
        """
        if n < 0:
            raise ValueError("n must be > 0.")

        if self.shape[0] != self.shape[1]:
            raise Exception("The LazyLinOp is not square.")

        if n == 0:
            from . import eye
            return eye(self.shape[0], self.shape[1], k=0)

        def _matmat(L, n, x):
            output = L @ x
            if n > 1:
                for _ in range(1, n):
                    output = L @ output
            return output

        return LazyLinOp(
            shape=self.shape,
            matmat=lambda x: _matmat(self, n, x),
            rmatmat=lambda x: _matmat(self.H, n, x),
            dtype=self.dtype
        )

    @staticmethod
    def islazylinop(obj):
        """
        Returns ``True`` if ``obj`` is a ``LazyLinOp``, ``False`` otherwise.
        """
        return isinstance(obj, LazyLinOp)

    def check(self, array_namespace=np, dtype: str = 'float64',
              device=None):
        r"""
        Verifies validity assertions on any :py:class:`LazyLinOp`.

        **Notations**:

        - Let ``op`` a :py:class:`LazyLinOp`,
        - ``u``, ``v`` vectors such that ``u.shape[0] == op.shape[1]``
          and ``v.shape[0] == op.shape[0]``,
        - ``X``, ``Y`` 2d-arrays such that ``X.shape[0] == op.shape[1]``
          and ``Y.shape[0] == op.shape[0]``.

        The function verifies:

            - Consistency of operator/adjoint product shape:

                1.

                    a. ``(op @ u).shape == (op.shape[0],)``,
                    b. ``(op.H @ v).shape == (op.shape[1],)``,
                2.

                    a. ``(op @ X).shape == (op.shape[0], X.shape[1])``,
                    b. ``(op.H @ Y).shape == (op.shape[1], Y.shape[1])``,

            - Consistency of operator & adjoint products:

                3. ``(op @ u).conj().T @ v == u.conj().T @ op.H @ v``

            - Consistency of operator-by-matrix & operator-by-vector products:

                4. ``op @ X`` is equal to the horizontal concatenation of all
                   ``op @ X[:, j]`` ($0 \le j  < X.shape[1]$).

                   (it implies also that ``(op @ X).shape[1] == X.shape[1]``,
                   as previously verified in 2.a)

            - Consistency of adjoint-by-matrix & adjoint-by-vector products:

                5. ``op.H @ Y`` is equal to the horizontal concatenation of all
                   ``op.H @ Y[:, j]`` ($0 \le j  < Y.shape[1]$).

                   (it implies also that ``(op.H @ Y).shape[1] == Y.shape[1]``,
                   as previously verified in 2.b)

            - Linearity:

                6. ``op @ (a1 * u1 + a2 * u2) == a1 * (op @ u1) + a2 * (op @ u2)``.

            - Device:

                7. ``array_api_compat.device(x) == array_api_compat.device(op @ x)

        Raises:
            - ``Exception("Operator shape[0] and operator-by-vector
              product shape must agree")`` (assertion 1.a)
            - ``Exception("Operator shape[1] and adjoint-by-vector
              product shape must agree")`` (assertion 1.b)
            - ``Exception("Operator-by-matrix product shape and
              operator/input-matrix shape must agree")`` (assertion 2.a)
            - ``Exception("Operator-by-matrix & operator-by-vector
              products must agree")`` (assertion 2.b)
            - ``Exception("Operator and adjoint products do not match")``
              (assertion 3)
            - ``Exception("Operator-by-matrix & operator-by-vector
              products must agree")`` (assertion 4)
            - ``Exception("Adjoint-by-matrix product shape and
              adjoint/input-matrix shape must agree")`` (assertion 5)


        .. admonition:: Computational cost
            :class: warning

            This function has a computational cost of several
            matrix products.
            It shouldn't be used into an efficient implementation but
            only to test a :py:class:`.LazyLinOp` implementation is
            valid.

        .. admonition:: Necessary condition but not sufficient
            :class: admonition-note

            This function is able to detect an inconsistent :class:`.LazyLinOp`
            according to the assertions above but it cannot ensure a
            particular operator computes what someone is excepted this operator
            to compute.
            In other words, the operator can be consistent but not correct at
            the same time. Thus, this function is not enough by itself to write
            unit tests for an operator, complementary tests are necessary.

        Args:
            self: (:py:class:`LazyLinOp`)
                Operator to test.
            array_namespace: ``namespace``, optional
                Namespace of the input to test ``self``.

                - NumPy namespace (default value).
                - CuPy namespace.
                - PyTorch namespace.
                - ``None`` NumPy/CuPy and PyTorch namespaces.
            dtype: ``str``, optional
                dtype of the input that will be used
                to test ``self``.
            device: optional
                Use device ``device`` to run ``self.check(...)``.
                Default value is ``None``.

        Example:
            >>> import numpy as np
            >>> from numpy.random import rand
            >>> from lazylinop import aslazylinop, LazyLinOp
            >>> M = rand(12, 14)
            >>> # numpy array M is OK as a LazyLinOp
            >>> aslazylinop(M).check(array_namespace=np)
            >>> # the next LazyLinOp is not
            >>> L2 = LazyLinOp((5, 2), matmat=lambda x: np.ones((6, 7)))
            >>> L2.check(array_namespace=np) # doctest:+ELLIPSIS
            Traceback (most recent call last):
            ...
            TypeError: ...

        .. seealso::
            :py:func:`aslazylinop`,
            :py:class:`LazyLinOp`
        """

        def _randx(M, N=None, xp=np, dtype: str = 'float',
                   device=None):
            if 'numpy' in str(xp.__package__):
                _randn = xp.random.randn
            elif 'torch' in str(xp.__package__):
                _randn = xp.randn
                _dtype = xp.from_numpy(
                    np.random.randn(3).astype(dtype)).dtype
            elif 'cupy' in str(xp.__package__):
                _randn = xp.random.randn
            else:
                raise Exception("Unknown array namespace.")
            n = 1 if N is None else N
            if dtype == 'complex':
                tmp = _randn(M, n) + 1j * _randn(M, n)
            else:
                tmp = _randn(M, n)
            if 'torch' in str(xp.__package__):
                tmp = tmp.to(dtype=_dtype, device=device)
            elif 'cupy' in str(xp.__package__):
                with xp.cuda.Device(device):
                    tmp = tmp.astype(dtype)
            else:
                tmp = tmp.astype(dtype)
            return tmp.reshape(-1) if n == 1 else tmp

        # Loop over NumPy/CuPy and PyTorch input.
        if array_namespace is None:
            import array_api_compat.numpy as xp1
            import array_api_compat.cupy as xp2
            import array_api_compat.torch as xp3
            xps = [xp1, xp2, xp3]
        else:
            xps = [array_namespace]
        for p in xps:
            # Random vectors and matrices.
            u = _randx(self.shape[1], xp=p, dtype=dtype, device=device)
            v = _randx(self.shape[0], xp=p, dtype=dtype, device=device)
            X = _randx(self.shape[1], 3, xp=p, dtype=dtype, device=device)
            Y = _randx(self.shape[0], 3, xp=p, dtype=dtype, device=device)
            a = _randx(1, xp=p, dtype=dtype, device=device)[0]
            a2 = _randx(1, xp=p, dtype=dtype, device=device)[0]
            u2 = _randx(self.shape[1], xp=p, dtype=dtype, device=device)
            xp = _array_namespace(u)
            # CuPy default device.
            if 'cupy' in str(xp.__package__) and device is not None:
                xp.cuda.runtime.setDevice(device)
            if 'torch' in str(xp.__package__):
                # Check against torch tensor.
                # Torch does not support multiplication of
                # two tensors with different dtype.
                try:
                    z = self @ u
                except RuntimeError:
                    print("Torch does not support multiplication of" +
                          " two tensors with different dtype:" +
                          f" do not check against {u.dtype}.")
                    continue
            # Check device
            self_u = self @ u
            self_v = self.H @ v
            if _device(self_u) != _device(u):
                raise Exception(
                    "y = op @ x and x are not on the same device.")
            # Check operator - vector product dimension
            if self_u.shape != (self.shape[0],):
                raise Exception("Operator shape[0] and operator-by-vector"
                                " product shape must agree")
            # Check operator adjoint - vector product dimension
            if self_v.shape != (self.shape[1],):
                raise Exception("Operator shape[1] and adjoint-by-vector"
                                " product shape must agree")
            # Check operator - matrix product consistency
            AX = self @ X
            if AX.shape != (self.shape[0], X.shape[1]):
                raise Exception("Operator-by-matrix product shape and"
                                " operator/input-matrix shape must agree")
            for i in range(X.shape[1]):
                if not xp.allclose(AX[:, i], self @ X[:, i]):
                    raise Exception("Operator-by-matrix & operator-by-vector"
                                    " products must agree")
            # Check operator transpose/adjoint dimensions
            AY = self.H @ Y
            if (AY.shape != (self.shape[1], Y.shape[1]) or
                (self.T @ Y).shape != (self.shape[1], Y.shape[1])):
                raise Exception("Adjoint-by-matrix product shape and"
                                " adjoint/input-matrix shape must agree")

            # Check operator adjoint on matrix product
            for i in range(Y.shape[1]):
                if not xp.allclose(AY[:, i], self.H @ Y[:, i]):
                    raise Exception("Adjoint-by-matrix & adjoint-by-vector"
                                    " products must agree")
            del AY
            # Dot test to check forward - adjoint consistency
            if 'torch' in str(xp.__package__):
                # Torch does not support multiplication of
                # two tensors with different dtype.
                # fft of float tensor returns complex tensor.
                promote = xp.promote_types(self_u.dtype, self_v.dtype)
                if not xp.allclose(
                        (self_u.conj().T @ v.to(dtype=self_u.dtype)).to(dtype=promote),
                        (u.conj().T.to(dtype=self_v.dtype) @ self_v).to(dtype=promote)):
                    raise Exception("Operator and adjoint products do not match")
            else:
                if not xp.allclose(self_u.conj().T @ v, u.conj().T @ self_v):
                    raise Exception("Operator and adjoint products do not match")
            # Check linearity op @ (a * u + a2 * u2) = a * op @ u + a2 * op @ u2.
            y = self @ (a * u + a2 * u2)
            z = a * self_u + a2 * (self @ u2)
            if not xp.allclose(y, z):
                raise Exception("Operator is not linear.")


def binary_dtype(A_dtype, B_dtype):
    """
    Returns the "greatest" dtype in size between A_dtype and B_dtype.
    If one dtype is complex the returned dtype is too.
    """
    if isinstance(A_dtype, str):
        A_dtype = np.dtype(A_dtype)
    if isinstance(B_dtype, str):
        B_dtype = np.dtype(B_dtype)
    if A_dtype is None and B_dtype is None:
        return None
    # ('complex', None) always gives 'complex'
    # because whatever None is hiding
    # the binary op result will be complex
    # but (real, None) gives None
    # because a None might or might not hide
    # a complex type
    if A_dtype is None:
        if 'complex' in str(B_dtype):
            return B_dtype
        return None
    if B_dtype is None:
        if 'complex' in str(A_dtype):
            return A_dtype
        return None
    # simply rely on numpy dtype
    np_res = (np.array([1], dtype=A_dtype) * np.array([1], dtype=B_dtype))
    return np_res.dtype


_binary_dtype = binary_dtype  # temporary private alias for retro-compat.


def sanitize_op(op, op_name='op'):
    if not hasattr(op, 'shape') or not hasattr(op, 'ndim'):
        raise TypeError(op_name+' must have shape and ndim attributes')


_sanitize_op = sanitize_op  # temporary private alias for retro-compat.


def islazylinop(obj):
    """
    Returns ``True`` if ``obj`` is a ``LazyLinOp``, ``False`` otherwise.
    """
    return LazyLinOp.islazylinop(obj)


def aslazylinop(op, shape=None):
    r"""
    Returns ``op`` as a :class:`LazyLinOp`.

    If ``shape`` is ``None`` the function relies on ``op.shape``.
    This argument allows to override ``op.shape`` if for any reason it
    is not well defined.
    See below, the example of ``pylops.Symmetrize`` defective shape.

    .. code-block:: python

        # Using the "shape" argument on a "defective" case:
        # To illustrate the use of the optional "shape" parameter,
        # let us consider implementing a lazylinearoperator
        # associated with the pylops.Symmetrize linear operator,
        # (version 2.1.0 is used here)
        # which is designed to symmetrize a vector, or a matrix,
        # along some coordinate axis.
        from pylops import Symmetrize
        M = np.random.rand(22, 2)
        # Here we want to symmetrize M
        # vertically (axis == 0), so we build the corresponding
        # symmetrizing operator Sop
        Sop = Symmetrize(M.shape, axis=0)
        # Applying the operator to M works, and the symmetrized matrix
        # has 43 = 2*22-1 rows, and 2 columns (as many as M) as expected!
        (Sop @ M).shape
        (43, 2)
        # Since it maps matrices with 22 rows to matrices with 43 rows,
        # as we intend the "shape" of Sop should be (43,22).
        # However, the "shape" as provided by pylops is inconsistent
        Sop.shape
        (86, 44)
        # To use Sop as a LazyLinOp we cannot rely on the “shape”
        # given by pylops (otherwise the LazyLinOp-matrix product
        # wouldn't be properly defined)
        # Thanks to the optional "shape" parameter of aslazylinop,
        # this can be fixed.
        lSop = aslazylinop(Sop, shape=(43, 22))
        # Now lSop.shape is consistent
        lSop.shape
        (43, 22)
        (lSop @ M).shape
        (43, 2)
        # Besides, Sop @ M is equal to lSop @ M, so all is fine!
        np.allclose(lSop @ M, Sop @ M)
        True

    Args:
        op: (``object``)
            May be of any type compatible with `scipy.sparse.linalg.
            aslinearoperator <https://docs.scipy.org/doc/scipy/reference/
            generated/scipy.sparse.linalg.aslinearoperator.html#scipy.sparse.
            linalg.aslinearoperator>`_
            (e.g. a ``numpy.ndarray``, a `scipy <https://docs.scipy.org/doc/
            scipy/tutorial/linalg.html>`_ matrix, a `scipy.LinearOperator
            <https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.
            linalg.LinearOperator.html#scipy.sparse.linalg.LinearOperator>`_,
            a `pyfaust.Faust <https://faustgrp.gitlabpages.inria.fr/faust/
            last-doc/html/classpyfaust_1_1Faust.html>`_ object, …).

            See the :class:`.LazyLinOp` documentation for additional
            information.

        shape: (``tuple[int, int]``)
            The shape of the resulting :class:`LazyLinOp`.
            If ``None`` the function relies on ``op.shape``.
            This argument allows to override ``op.shape`` if for
            any reason it is not well defined.


    Returns:
        A :class:`LazyLinOp` instance based on ``op``.

    **Examples**:

        Creating a :class:`LazyLinOp` based on a numpy array:
            >>> from lazylinop import aslazylinop
            >>> import numpy as np
            >>> M = np.random.rand(10, 12).astype('float64')
            >>> lM = aslazylinop(M)
            >>> lM
            <10x12 LazyLinOp with dtype=float64>
            >>> twolM = lM + lM
            >>> twolM
            <10x12 LazyLinOp with unspecified dtype>


        Creating a :class:`LazyLinOp` based on a ``np.random.randn``:
            >>> import numpy as np
            >>> F = np.random.randn(10, 12).astype('float32')
            >>> lF = aslazylinop(F)
            >>> lF
            <10x12 LazyLinOp with dtype=float32>
            >>> twolF = lF + lF
            >>> twolF
            <10x12 LazyLinOp with unspecified dtype>


        Creating a :class:`LazyLinOp` based on a ``sp.sparse.eye``:
            >>> import numpy as np
            >>> import scipy as sp
            >>> E = sp.sparse.eye(10, 12).astype('float32')
            >>> L = aslazylinop(E)
            >>> L
            <10x12 LazyLinOp with dtype=float32>
            >>> twoL = L + L
            >>> twoL
            <10x12 LazyLinOp with unspecified dtype>

    .. seealso::
        `pyfaust.rand
        <https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#abceec3d0838435ceb3df1befd1e29acc>`_,
        `pylops.Symmetrize
        <https://pylops.readthedocs.io/en/latest/api/generated/pylops.Symmetrize.html>`_.
        `scipy.sparse.linalg.aslinearoperator <https://docs.scipy.org/doc/
        scipy/reference/generated/scipy.sparse.linalg.aslinearoperator.html
        #scipy.sparse.linalg.aslinearoperator>`_

    """
    if islazylinop(op):
        return op
    elif (is_array_api_obj(op) or issparse(op) or _iscxsparse(op)
          or isinstance(op, LinearOperator)):
        L = LazyLinOp._create_from_op(op, shape)
        L._dtype = op.dtype
        if is_array_api_obj(op):
            L._device = _device(op)
        if is_torch_array(op):
            # FIXME: LinearOperator does not work with torch.dtype.
            L.dtype = None
        else:
            L.dtype = op.dtype
    else:
        L = LazyLinOp._create_from_op(op, shape)
    return L


def aslazylinops(*ops):
    """
    Returns the list of aslazylinop(ops[i]).

    .. seealso::

        :func:`.aslazylinop`
    """
    return [aslazylinop(op) for op in ops]

# below are deprecated names


def aslazylinearoperator(op, shape=None):
    from warnings import warn
    warn("aslazylinearoperator is a deprecated name and will disappear in a"
         " next version. Please use aslazylinop.")
    return aslazylinop(op, shape)


def isLazyLinearOp(obj):
    from warnings import warn
    warn("isLazyLinearOp is a deprecated name and will disappear in a"
         " next version. Please use islazylinop.")
    return islazylinop(obj)


class LazyLinearOp(LazyLinOp):

    def __init__(self, *args, **kwargs):
        from warnings import warn
        warn("LazyLinearOp is a deprecated name and will disappear in a"
             " next version. Please use LazyLinOp.")
        super(LazyLinearOp, self).__init__(*args, **kwargs)


def _seye(N: int, v: Union[np.ndarray, list] = None):
    r"""
    Returns a :class:`.LazyLinOp` ``L`` for the sparse eye matrix.

    Shape of ``L`` is $\left(M,~N\right)$ where $M$ is the size of ``v``
    and $N$ is the size of the input.

    Args:
        N: ``int``
            Size of the input.
        v: ``np.ndarray``, ``torch.Tensor`` or ``list``
            Diagonal indices such that the element is non-zero.
    """

    if is_array_api_obj(v):
        ne = _size(v)
    else:
        ne = len(v)

    def _matmat(x):
        if v is None:  # or ne == N:
            return x
        else:
            return x[v, :]

    def _rmatmat(x):
        if v is None:  # or ne == N:
            return x
        else:
            xp = _array_namespace(x)
            y = xp.zeros((N, x.shape[1]), dtype=x.dtype,
                         device=x.device)
            y[v, :] = x
            return y

    return LazyLinOp(
        shape=(ne, N),
        matmat=lambda x: _matmat(x),
        rmatmat=lambda x: _rmatmat(x)
    )
