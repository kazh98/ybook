#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import itertools
from sympy.core.expr import AtomicExpr
from sympy.core.symbol import Symbol
from sympy.utilities import lambdify
from typing import List, Callable, Iterable, Optional

__all__ = ['iiduka2012']


def _P(w: np.ndarray, b: float) -> Callable[[np.ndarray], np.ndarray]:
    def T(x: np.ndarray) -> np.ndarray:
        det = np.dot(w, x)
        if det <= b:
            return x
        return x - ((det - b) / np.dot(w, w)) * w
    return T


def iiduka2012(
        var_list: List[Symbol],
        fun: AtomicExpr,
        A: np.ndarray,
        b: np.ndarray,
        n_iter: int=1000,
        x0: Optional[np.ndarray]=None,
        l_seq: Optional[Iterable[float]]=None,
        a_seq: Optional[Iterable[float]]=None,
        b_seq: Optional[Iterable[float]]=None
):
    """H. Iiduka: Fixed point optimization algorithm and its application to network bandwidth allocation. Journal of
    Computational and Applied Mathematics 236(7). pp.1733-1742. (2012)"""

    n = len(var_list)
    dfuns = [lambdify(var_list, fun.diff(var_list[i])) for i in range(n)]

    def df(x: np.ndarray) -> np.ndarray:
        return np.array([dfun(*x) for dfun in dfuns])

    projs = [_P(w, bk) for w, bk in zip(A, b)]

    def trans(x: np.ndarray) -> np.ndarray:
        # w = sum(proj(x) for proj in projs) / len(projs)
        w = x
        for proj in projs:
            w = proj(w)
        w = np.fmax(0, w)
        return w

    if l_seq is None:
        l_seq = map(lambda k: 1e-1 / (k ** 0.25), itertools.count(1))
    if a_seq is None:
        a_seq = map(lambda k: 1.0 / (k ** 0.5), itertools.count(1))
    if b_seq is None:
        b_seq = map(lambda k: 1.0 / (k + 1), itertools.count(1))
    if x0 is None:
        x0 = np.ones(n)
    x = x0
    d = df(x)
    for k, l, a, b in zip(range(n_iter), l_seq, a_seq, b_seq):
        y = trans(x + l * d)
        x = a * x0 + (1 - a) * y
        d = df(x) + b * d
    return x

if __name__ == '__main__':
    import numpy as np
    from sympy import *
    x0, x1, x2 = symbols("x0 x1 x2")
    print(iiduka2012([x0, x1, x2], log(x0) + log(x1) + log(x2), np.array([[1, 0, 1], [0, 1, 1]]), np.array([2., 3.])))
