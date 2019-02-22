#!/usr/bin/python

import sys
from collections import namedtuple
from collections import defaultdict

Item = namedtuple('Item', ['index', 'size', 'value'])
sys.setrecursionlimit(1500)


class Combo:
    def __init__(self, value=0, size=0, items=[]):
        self.value = value
        self.size = size
        self.items = items

    def add_item(self, item):
        (index, size, value) = item

        return Combo(
            value=self.value + value,
            size=self.size + size,
            items=self.items + [index]
        )

    def __repr__(self):
        return 'value: {}, size: {}, items: {}'.format(self.value, self.size, self.items)


def knapsack_solver(items, capacity):
    def helper(i, capacity, cache):
        item = items[i]
        (index, size, value) = item

        # first, check cache
        cached = cache[i][capacity]

        if cached is not None:
            return cached

        elif capacity < 0:
            combo = Combo()

        elif i == 0:
            if capacity - size >= 0:
                combo = Combo().add_item(item)
            else:
                combo = Combo()

        else:
            # compare two options
            #  - same capacity with one fewer items
            #  - this item + remaining capacity and one fewer item
            last_max = helper(i - 1, capacity, cache)
            if capacity - size >= 0:
                new_candidate = helper(
                    i - 1, capacity - size, cache).add_item(item)
            else:
                new_candidate = Combo()

            combo = last_max if last_max.value > new_candidate.value else new_candidate

        cache[i][capacity] = combo
        return combo

    cache = defaultdict(lambda: defaultdict(lambda: None))
    best = helper(len(items) - 1, capacity, cache)
    return {'Value': best.value, 'Chosen': sorted(best.items)}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        capacity = int(sys.argv[2])
        file_location = sys.argv[1].strip()
        file_contents = open(file_location, 'r')
        items = []

        for line in file_contents.readlines():
            data = line.rstrip().split()
            items.append(Item(int(data[0]), int(data[1]), int(data[2])))

        file_contents.close()
        print(knapsack_solver(items, capacity))
    else:

        print('Usage: knapsack.py [filename] [capacity]')

# items = [
#     Item(1, 42, 81),
#     Item(2, 42, 42),
#     Item(3, 68, 56),
#     Item(4, 68, 25),
#     Item(5, 77, 14),
# ]
# knapsack_solver(items, 100)
