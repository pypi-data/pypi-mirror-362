from warnings import warn

try:
    import torch

    found_pytorch = True
except ImportError:
    warn("Did not find PyTorch, therefore use NumPy/SciPy.")
    found_pytorch = False
try:
    from einops import rearrange

    found_einops = True
except ImportError:
    found_einops = False
    warn("Did not find einops, therefore use NumPy.")
import os
import numpy as np


if "GB_DISABLE_EINOPS" in dict(os.environ).keys():
    found_einops = os.environ["GB_DISABLE_EINOPS"] == 0
    if not found_einops:
        print("Disable einops.")


def twiddle_mul_twiddle(l_twiddle, r_twiddle, l_param,
                        r_param, backend: str = 'numpy'):
    """Compute the product of two compatible twiddles.

    Args:
        l_twiddle: ``numpy.array`` or ``torch.tensor``
            Tensors of order 4.
        r_twiddle: ``numpy.array`` or ``torch.tensor``
            Tensors of order 4.
        backend: ``str``, optional
            Use numpy (default) or pytorch to compute
            SVD and QR decompositions.

    Returns:
        A tensor of order 4 (twiddle) (``numpy.array``
        or ``torch.tensor``).
    """
    a1, b1, c1, d1, p1, q1 = l_param
    a2, b2, c2, d2, p2, q2 = r_param
    if found_einops:
        l_twiddle = rearrange(
            l_twiddle, "a1 d1 b1 (c1 q1) -> (a1 c1) d1 b1 q1", c1=c1
        )
        r_twiddle = rearrange(
            r_twiddle, "a2 d2 (p2 b2) c2 -> a2 (b2 d2) p2 c2", b2=b2
        )
    else:
        a1, d1, b1, tmp = l_twiddle.shape
        q1 = tmp // c1
        l_twiddle = (
            l_twiddle.reshape(a1, d1, b1, c1, q1)
            .swapaxes(2, 3)
            .swapaxes(1, 2)
            .reshape(a1 * c1, d1, b1, q1)
        )
        a2, d2, tmp, c2 = r_twiddle.shape
        p2 = tmp // b2
        r_twiddle = (
            r_twiddle.reshape(a2, d2, p2, b2, c2)
            .swapaxes(2, 3)
            .swapaxes(1, 2)
            .reshape(a2, b2 * d2, p2, c2)
        )
    if backend == 'pytorch' and found_pytorch:
        result = torch.matmul(l_twiddle.float(), r_twiddle.float())
    else:
        result = l_twiddle.astype(np.float64) @ r_twiddle.astype(np.float64)
    if found_einops:
        result = rearrange(
            result, "(a c1) (b2 d) b1 c2 -> a d (b1 b2) (c1 c2)", c1=c1, b2=b2
        )
    else:
        tmp1, tmp2, b1, c2 = result.shape
        a = tmp1 // c1
        d = tmp2 // b2
        result = (
            result.reshape(a, c1, b2, d, b1, c2)
            .swapaxes(2, 3)
            .swapaxes(1, 2)
            .swapaxes(2, 4)
            .reshape(a, d, b1 * b2, c1 * c2)
        )
    return result


def twiddle_to_dense(twiddle, backend: str = 'numpy'):
    """Convert twiddle to the dense form.

    Args:
        twiddle: ``np.ndarray`` or ``torch.tensor``
            Twiddle to convert to dense format.
        backend: ``str``, optional
            Use numpy (default) or pytorch to compute
            SVD and QR decompositions.

    Returns:
        Dense form of twiddle (``np.ndarray`` or ``torch.tensor``).
    """
    if backend == 'pytorch' and found_pytorch:
        a, d, b, c = twiddle.size()
        n = a * d * c
        output = torch.eye(n)
    else:
        a, d, b, c = twiddle.shape
        n = a * d * c
        output = np.eye(n)
    if backend == 'pytorch' and found_pytorch:
        t = twiddle.view(a * d, b, c)
        output = (
            output.reshape(a, c, d, n).permute(0, 2, 1, 3).reshape(a * d, c, n)
        )
        output = torch.bmm(t, output)
        return (
            output.reshape(a, d, b, n)
            .permute(0, 2, 1, 3)
            .reshape(a * d * b, n)
        )
    else:
        t = twiddle.reshape(a * d, b, c)
        output = (
            output.reshape(a, c, d, n).swapaxes(1, 2).reshape(a * d, c, n)
        )
        output = np.einsum("ijk,ikl->ijl", t, output)
        return output.reshape(a, d, b, n).swapaxes(1, 2).reshape(a * d * b, n)
