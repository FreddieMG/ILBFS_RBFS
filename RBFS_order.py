from tile_puzzle import *
from sys import maxsize
from utils import *

@profile_memory
def recursive_best_first_search_with_order(initial_state):
    node, _ = RBFS_search_with_order(EightPuzzleNode(EightPuzzleState(state=initial_state)), f_limit=maxsize)
    result = node.find_solution() if node else None
    return result

def RBFS_search_with_order(node, f_limit):
    successors = []
    if node.goal_test():
        return node, None
    children = node.generate_child()
    # children = children[::-1]
    if not len(children):
        return None, maxsize
    count = 0
    for child in children:
        count -= 1
        if node.evaluation_function < node.F:
            child.F = max(child.F, node.F)
        successors.append((child.F, count, child))
    while len(successors):

        successors.sort()
        best_node = successors[0][2]
        if best_node.F > f_limit:
            return None, best_node.F
        alternative = successors[1][0]


        result, best_node.F = RBFS_search_with_order(best_node, min(f_limit, alternative))
        successors[0] = (best_node.F, successors[0][1], best_node)
        if result is not None:
            break
    return result, None