#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def distance(p1, p2):
    """
    Euclidian distance

    Arguments:
    p1 -- (x, y) : Tuple containing the x, y, of the first point.
    p2 -- (x, y) : Tuple containing the x, y, of the second point.

    Returns:
    Return the euclidian distance between *p1* and *p2*
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[0] - p2[0]) ** 2)

if __name__ == '__main__':
    nodes = [(0, 0), (1, 1)]
    needs = [1, 1]
    needs_nodes = [(n, h) for n, h in sorted(zip(nodes, needs),
        key=lambda (_, h): h) if h > 0]
    nodes = [n for n, h in needs_nodes if h == needs_nodes[0][1]]

    ship = [(4, 3), (2, 1)]
    for s in ship:
        index, nearest = zip(*sorted(enumerate(nodes),
            key=lambda (i, p): distance(p, s)))
        nodes.pop(index[0])
        print s, '->', nearest[0]

