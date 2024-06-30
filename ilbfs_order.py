from tile_puzzle import *
import heapq
from utils import *


@profile_memory
def ilbfs_with_order_heapify(initial_state):
    root = EightPuzzleNode(EightPuzzleState(initial_state))
    open_list = []
    heapq.heappush(open_list, root)
    tree = {}
    old_best = None
    counter = 0
    order_count = 0
    test = True
    recently_collapsed = False
    while open_list:

        best = heapq.heappop(open_list)
    
        if best.goal_test():
            return best.find_solution()

        while old_best and best.parent and best.parent != old_best:
            recently_collapsed = True

            min_val = float("inf")
            for child in tree[old_best]:

                if child.F < min_val:
                    min_val = child.F

                if child in open_list:
                    open_list.remove(child)

            old_best.F = min_val
            heapq.heappush(open_list, old_best)
            del tree[old_best]
            old_best = old_best.parent

        if recently_collapsed:
            heapq.heapify(open_list)
            recently_collapsed = False

        tree[best] = []
        for child in best.generate_child():
            child.creation_time = counter
            counter += 1
            if best.F > best.evaluation_function and best.F > child.F:
                child.F = best.F

            heapq.heappush(open_list, child)
            tree[best].append(child)

        old_best = best


@profile_memory
def ilbfs_with_order_sift_down(initial_state):
    root = EightPuzzleNode(EightPuzzleState(initial_state))
    open_list = []
    heapq.heappush(open_list, root)
    tree = {}
    old_best = None
    counter = 0
    collapse_flag = True
    order_count = 0
    test = True
    while open_list:

        best = heapq.heappop(open_list)

        if best.goal_test():
            return best.find_solution()

        while old_best and best.parent and best.parent != old_best:

            min_val = float("inf")
            for child in tree[old_best]:

                if child.F < min_val:
                    min_val = child.F

                if child in open_list:
                    i = open_list.index(child)
                    open_list[i] = open_list[-1]
                    open_list.pop()

                    if i < len(open_list):
                        heapq._siftup(open_list, i)
                        heapq._siftdown(open_list, 0, i)

            old_best.F = min_val
            heapq.heappush(open_list, old_best)

            del tree[old_best]

            old_best = old_best.parent

        tree[best] = []
        for child in best.generate_child():
            child.creation_time = counter
            counter += 1
            if best.F > best.evaluation_function and best.F > child.F:
                child.F = best.F

            heapq.heappush(open_list, child)
            tree[best].append(child)

        old_best = best
