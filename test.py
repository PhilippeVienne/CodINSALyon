#!/usr/bin/env python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    nodes = {1, 2, 3}
    neighbours = {1: [2, 3], 2: [1], 3: [1]}
    most_neighbours = max(nodes, key = lambda n : len(neighbours[n]))

    print most_neighbours