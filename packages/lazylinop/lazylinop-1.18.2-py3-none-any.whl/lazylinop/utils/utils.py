import array_api_compat
try:
    import torch
except ModuleNotFoundError:
    torch = None
try:
    import cupyx as cpx
except ModuleNotFoundError:
    cpx = None
from scipy.sparse import issparse


__all__ = ['_iscxsparse', '_istsparse', '_issparse']


def _iscxsparse(x):
    if cpx is None:
        return False
    else:
        from cupyx.scipy.sparse import issparse
        return issparse(x)


def _istsparse(x):
    if torch is None:
        return False
    else:
        if hasattr(x, 'is_sparse') and hasattr(x, 'layout'):
            return x.is_sparse or x.layout == torch.sparse_csr
        else:
            return False


def _issparse(x):
    return issparse(x) or _iscxsparse(x) or _istsparse(x)
