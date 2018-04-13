#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
from typing import Iterable, Tuple

__all__ = ['draw']


def draw(limits: np.ndarray, links: Iterable[Tuple[int, int]], values: np.ndarray) -> None:
    if values.dtype != np.float64:
        values = values.astype(np.float64)
    fig, axes = plt.subplots()
    stat = np.zeros_like(limits, dtype=np.float64)
    
    u_rsv = [set() for _ in range(limits.shape[0])]
    l_rsv = [set() for _ in range(limits.shape[0])]
    for n, (b, e) in zip(count(), links):
        li, hi = min(b, e), max(b, e)
        stat[li:hi] += values[n]
        for lev in count():
            if all(lev not in u_rsv[i] for i in range(li, hi)):
                for i in range(li, hi):
                    u_rsv[i].add(lev)
                low, high = lev / 2 + 0.5, lev / 2 + 0.8
                tposv = low
                break
            if all(lev not in l_rsv[i] for i in range(li, hi)):
                for i in range(li, hi):
                    l_rsv[i].add(lev)
                low, high = -(lev / 2 + 0.5), -(lev / 2 + 0.8)
                tposv = high + 0.2
                break
        if b <= e:
            bt, et = b + 0.6, e + 0.4
            bp, ep = bt + 0.25, et - 0.25
            tposh = bt + 0.1
        else:
            et, bt = e + 0.6, b + 0.4
            ep, bp = et + 0.25, bt - 0.25
            tposh = ep
        axes.add_artist(plt.Line2D([bt, bp, ep, et], [low, high, high, low], c='g'))
        axes.add_artist(plt.Line2D([ep, et, et], [low, low, high], c='g'))
        axes.annotate("x%d" % n, xy=(tposh, tposv))
    
    axes.set_aspect('equal')
    axes.set_xlim([0, limits.shape[0] + 1])
    axes.set_ylim([-(1 + max(max(l_rsv[i], default=0) for i in range(limits.shape[0])) / 2),
                   1 + max(max(u_rsv[i], default=0) for i in range(limits.shape[0])) / 2])
    
    for i in range(limits.shape[0]):
        color = '0.5'
        if 0 < stat[i]:
            color = 'k'
        if limits[i] < stat[i]:
            color = 'r'
        axes.add_artist(plt.Line2D([i + 0.75, i + 1.25], [0, 0], linewidth=3, c=color))
        axes.annotate("c%d" % i, xy=(i + 0.75, -0.2))
    for i in range(limits.shape[0] + 1):
        axes.add_artist(plt.Circle((i + 0.5, 0), 0.25, linewidth=2, fc='w', ec='b'))
    
    print('===== LINK STATUS =====')
    for n in range(limits.shape[0]):
        print('  * c%d = %.8f (<= %.8f)' % (n, stat[n], limits[n]))
    print()
    print('===== FLOW STATUS =====')
    for n in range(len(values)):
        print('  * x%d = %.8f' % (n, values[n]))
    
    return
