"""
math functions and miscellaneous calculations
"""

import os
from functools import lru_cache
from math import pi
from typing import List, Optional, Union

import numpy as np
import sympy
import tensorflow as tf
from scipy.optimize import brentq
from scipy.special import spherical_jn

from ...m3gnet.config import DataType

CWD = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=128)
def get_spherical_bessel_roots() -> np.ndarray:
    """
    Get precomputed Spherical Bessel function roots. The results is a
    2D matrix with dimension [128, 128]. The n-th (0-based index） root of
    order l Spherical Bessel function is the `[l, n]` entry

    Returns: 2D matrix of pre-computed roots

    """
    return np.loadtxt(os.path.join(CWD, "sb_roots.txt"))


@lru_cache(maxsize=128)
def spherical_bessel_roots(max_l: int, max_n: int):
    """
    Calculate the spherical Bessel roots. The n-th root of the l-th
    spherical bessel function is the `[l, n]` entry of the return matrix.
    The calculation is based on the fact that the n-root for l-th
    spherical Bessel function `j_l`, i.e., `z_{j, n}` is in the range
    `[z_{j-1,n}, z_{j-1, n+1}]`. On the other hand we know precisely the
    roots for j0, i.e., sinc(x)

    Args:
        max_l: max order of spherical bessel function
        max_n: max number of roots
    Returns: root matrix of size [max_l, max_n]
    """
    temp_zeros = np.arange(1, max_l + max_n + 1) * pi  # j0
    roots = [temp_zeros[:max_n]]
    for i in range(1, max_l):
        roots_temp = []
        for j in range(max_n + max_l - i):
            low = temp_zeros[j]
            high = temp_zeros[j + 1]
            root = brentq(lambda x, v: spherical_jn(v, x), low, high, (i,))
            roots_temp.append(root)
        temp_zeros = np.array(roots_temp)
        roots.append(temp_zeros[:max_n])
    return np.array(roots)


class SphericalBesselFunction:
    """
    Calculate the spherical Bessel function based on the sympy + tensorflow
    implementations
    """

    def __init__(self, max_l: int, max_n: int = 5, cutoff: float = 5.0, smooth: bool = False):
        """
        Args:
            max_l: int, max order (excluding l)
            max_n: int, max number of roots used in each l
            cutoff: float, cutoff radius
        """
        self.max_l = max_l
        self.max_n = max_n
        self.cutoff = cutoff
        self.smooth = smooth
        if smooth:
            self.funcs = self._calculate_smooth_symbolic_funcs()
        else:
            self.funcs = self._calculate_symbolic_funcs()

        self.zeros = tf.cast(get_spherical_bessel_roots(), dtype=DataType.tf_float)

    @lru_cache(maxsize=128)
    def _calculate_symbolic_funcs(self) -> List:
        """
        Spherical basis functions based on Rayleigh formula. This function
        generates
        symbolic formula.

        Returns: list of symbolic functions

        """
        x = sympy.symbols("x")
        funcs = [sympy.expand_func(sympy.functions.special.bessel.jn(i, x)) for i in range(self.max_l + 1)]
        return [sympy.lambdify(x, func, "tensorflow") for func in funcs]

    @lru_cache(maxsize=128)
    def _calculate_smooth_symbolic_funcs(self) -> List:
        return _get_lambda_func(max_n=self.max_n, cutoff=self.cutoff)

    def __call__(self, r: tf.Tensor) -> tf.Tensor:
        """
        Args:
            r: tf.Tensor, distance Tensor, 1D


        Returns: [n, max_n * max_l] spherical Bessel function results

        """
        if self.smooth:
            return self._call_smooth_sbf(r)
        return self._call_sbf(r)

    def _call_smooth_sbf(self, r: tf.Tensor) -> tf.Tensor:
        results = [i(r) for i in self.funcs]
        return tf.transpose(tf.stack(results))

    def _call_sbf(self, r: tf.Tensor) -> tf.Tensor:
        roots = self.zeros[: self.max_l, : self.max_n]

        results = []
        factor = tf.cast(tf.sqrt(2.0 / self.cutoff**3), dtype=DataType.tf_float)
        for i in range(self.max_l):
            root = roots[i]
            func = self.funcs[i]
            func_add1 = self.funcs[i + 1]
            results.append(
                func(r[:, None] * root[None, :] / self.cutoff) * factor / tf.math.abs(func_add1(root[None, :]))
            )
        return tf.concat(results, axis=1)

    @staticmethod
    def rbf_j0(r: tf.Tensor, cutoff: float = 5.0, max_n: int = 3) -> tf.Tensor:
        """
        Spherical Bessel function of order 0, ensuring the function value
        vanishes at cutoff

        Args:
            r: tf.Tensor tensorflow tensors
            cutoff: float, the cutoff radius
            max_n: int max number of basis
        Returns: basis function expansion using first spherical Bessel function
        """
        n = tf.cast(tf.range(1, max_n + 1), dtype=DataType.tf_float)[None, :]
        r = r[:, None]
        return tf.math.sqrt(2.0 / cutoff) * tf.math.sin(n * pi / cutoff * r) / r


def _y00(theta, phi):
    r"""
    Spherical Harmonics with `l=m=0`

    ..math::
        Y_0^0 = \frac{1}{2} \sqrt{\frac{1}{\pi}}

    Args:
        theta: tf.Tensor, the azimuthal angle
        phi: tf.Tensor, the polar angle

    Returns: `Y_0^0` results

    """
    dtype = theta.dtype
    return 0.5 * tf.ones_like(theta) * tf.cast(tf.math.sqrt(1.0 / pi), dtype=dtype)


def _conjugate(x):
    return tf.math.conj(x)


class Gaussian:
    """
    Gaussian expansion function
    """

    def __init__(self, centers: Union[tf.Tensor, np.ndarray], width: float, **kwargs):
        """
        Args:
            centers (tf.Tensor or np.ndarray): Gaussian centers for the
                expansion
            width (float): Gaussian width
            **kwargs:
        """
        self.centers = np.array(centers)
        self.width = width

    def __call__(self, r: tf.Tensor) -> tf.Tensor:
        """
        Convert the radial distances into Gaussian functions
        Args:
            r (tf.Tensor): radial distances
        Returns: Gaussian expanded vectors

        """
        return tf.exp(-((r[:, None] - self.centers[None, :]) ** 2) / self.width**2)


class SphericalHarmonicsFunction:
    """
    Spherical Harmonics function
    """

    def __init__(self, max_l: int, use_phi: bool = True):
        """
        Args:
            max_l: int, max l (excluding l)
            use_phi: bool, whether to use the polar angle. If not,
                the function will compute `Y_l^0`
        """
        self.max_l = max_l
        self.use_phi = use_phi
        self.funcs = self._calculate_symbolic_funcs()

    def _calculate_symbolic_funcs(self):
        funcs = []
        theta, phi = sympy.symbols("theta phi")
        for lval in range(self.max_l):
            if self.use_phi:
                m_list = range(-lval, lval + 1)
            else:
                m_list = [0]
            for m in m_list:
                func = sympy.functions.special.spherical_harmonics.Znm(lval, m, theta, phi).expand(func=True)
                funcs.append(func)
        # replace all theta with cos(theta)
        costheta = sympy.symbols("costheta")
        funcs = [i.subs({theta: sympy.acos(costheta)}) for i in funcs]
        self.orig_funcs = [sympy.simplify(i).evalf() for i in funcs]
        results = [
            sympy.lambdify([costheta, phi], i, [{"conjugate": _conjugate}, "tensorflow"]) for i in self.orig_funcs
        ]
        results[0] = _y00
        return results

    def __call__(self, costheta, phi: Optional[tf.Tensor] = None):
        """
        Args:
            theta: tf.Tensor, the azimuthal angle
            phi: tf.Tensor, the polar angle

        Returns: [n, m] spherical harmonic results, where n is the number
            of angles. The column is arranged following
            `[Y_0^0, Y_1^{-1}, Y_1^{0}, Y_1^1, Y_2^{-2}, ...]`
        """
        costheta = tf.cast(costheta, dtype=tf.dtypes.complex64)
        phi = tf.cast(phi, dtype=tf.dtypes.complex64)
        results = tf.stack([func(costheta, phi) for func in self.funcs], axis=1)
        results = tf.cast(results, dtype=DataType.tf_float)
        return results


def _block_repeat(array, block_size, repeats):
    col_index = tf.range(tf.shape(array)[1])
    indices = []
    start = 0

    for i, b in enumerate(block_size):
        indices.append(tf.tile(col_index[start : start + b], [repeats[i]]))
        start += b
    indices = tf.concat(indices, axis=0)
    return tf.gather(array, indices, axis=1)


def combine_sbf_shf(sbf: tf.Tensor, shf: tf.Tensor, max_n: int, max_l: int, use_phi: bool):
    """
    Combine the spherical Bessel function and the spherical Harmonics function
    For the spherical Bessel function, the column is ordered by
        [n=[0, ..., max_n-1], n=[0, ..., max_n-1], ...], max_l blocks,

    For the spherical Harmonics function, the column is ordered by
        [m=[0], m=[-1, 0, 1], m=[-2, -1, 0, 1, 2], ...] max_l blocks, and each
        block has 2*l + 1
        if use_phi is False, then the columns become
        [m=[0], m=[0], ...] max_l columns

    Args:
        sbf: tf.Tensor spherical bessel function results
        shf: tf.Tensor spherical harmonics function results
        max_n: int, max number of n
        max_l: int, max number of l
        use_phi: whether to use phi
    Returns:
    """
    if tf.shape(sbf)[0] == 0:
        return sbf

    if not use_phi:
        repeats_sbf = [1] * max_l * max_n
        block_size = [1] * max_l
    else:
        # [1, 1, 1, ..., 1, 3, 3, 3, ..., 3, ...]
        repeats_sbf = np.repeat(2 * np.arange(max_l) + 1, repeats=max_n)
        # tf.repeat(2 * tf.range(max_l) + 1, repeats=max_n)
        block_size = 2 * np.arange(max_l) + 1
        # 2 * tf.range(max_l) + 1
    expanded_sbf = tf.repeat(sbf, repeats=repeats_sbf, axis=1)
    expanded_shf = _block_repeat(shf, block_size=block_size, repeats=[max_n] * max_l)
    shape = max_n * max_l
    if use_phi:
        shape *= max_l
    return tf.reshape(expanded_sbf * expanded_shf, [-1, shape])


def _sinc(x):
    return tf.math.sin(x) / x


@tf.function
def spherical_bessel_smooth(r, cutoff: float = 5.0, max_n: int = 10):
    """
    This is an orthogonal basis with first
    and second derivative at the cutoff
    equals to zero. The function was derived from the order 0 spherical Bessel
    function, and was expanded by the different zero roots

    Ref:
        https://arxiv.org/pdf/1907.02374.pdf

    Args:
        r: tf.Tensor distance tensor
        cutoff: float, cutoff radius
        max_n: int, max number of basis, expanded by the zero roots

    Returns: expanded spherical harmonics with derivatives smooth at boundary

    """
    n = tf.cast(tf.range(max_n), dtype=DataType.tf_float)[None, :]
    r = r[:, None]
    fnr = (
        (-1) ** n
        * tf.math.sqrt(2.0)
        * pi
        / cutoff**1.5
        * (n + 1)
        * (n + 2)
        / tf.math.sqrt(2 * n**2 + 6 * n + 5)
        * (_sinc(r * (n + 1) * pi / cutoff) + _sinc(r * (n + 2) * pi / cutoff))
    )
    en = n**2 * (n + 2) ** 2 / (4 * (n + 1) ** 4 + 1)
    dn = [tf.constant(1.0)]
    for i in range(1, max_n):
        dn.append(1 - en[0, i] / dn[-1])
    dn = tf.stack(dn)
    gn = [fnr[:, 0]]
    for i in range(1, max_n):
        gn.append(1 / tf.math.sqrt(dn[i]) * (fnr[:, i] + tf.sqrt(en[0, i] / dn[i - 1]) * gn[-1]))
    return tf.transpose(tf.stack(gn))


@lru_cache(maxsize=128)
def _get_lambda_func(max_n, cutoff: float = 5.0):
    r = sympy.symbols("r")
    d0 = 1.0
    en = []
    for i in range(max_n):
        en.append(i**2 * (i + 2) ** 2 / (4 * (i + 1) ** 4 + 1))

    dn = [d0]
    for i in range(1, max_n):
        dn.append(1 - en[i] / dn[-1])

    fnr = []
    for i in range(max_n):
        fnr.append(
            (-1) ** i
            * sympy.sqrt(2.0)
            * sympy.pi
            / cutoff**1.5
            * (i + 1)
            * (i + 2)
            / sympy.sqrt(1.0 * (i + 1) ** 2 + (i + 2) ** 2)
            * (
                sympy.sin(r * (i + 1) * sympy.pi / cutoff) / (r * (i + 1) * sympy.pi / cutoff)
                + sympy.sin(r * (i + 2) * sympy.pi / cutoff) / (r * (i + 2) * sympy.pi / cutoff)
            )
        )

    gnr = [fnr[0]]
    for i in range(1, max_n):
        gnr.append(1 / sympy.sqrt(dn[i]) * (fnr[i] + sympy.sqrt(en[i] / dn[i - 1]) * gnr[-1]))

    return [sympy.lambdify([r], sympy.simplify(i), "tensorflow") for i in gnr]
