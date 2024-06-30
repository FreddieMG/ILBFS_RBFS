# import networkx as nx
# import matplotlib.pyplot as plt
import random
import time
import tracemalloc

# from memory_profiler import memory_usage

def profile_memory(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        tracemalloc.start()
        
        result = func(*args, **kwargs),
        
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        runtime = time.time() - start_time
        return  result[0], peak, runtime
    return wrapper

def generate_random_state_from_goal(goal_state, n_actions):
    def get_neighbors(state):
        neighbors = []
        blank_index = state.index(0)
        row, col = divmod(blank_index, 3)

        # Define possible moves (up, down, left, right)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_index = new_row * 3 + new_col
                new_state = state[:]
                new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
                neighbors.append(new_state)
        return neighbors

    current_state = goal_state[:]
    for _ in range(n_actions):
        neighbors = get_neighbors(current_state)
        current_state = random.choice(neighbors)

    return current_state


def generate_random_state_from_goal(goal_state, n_actions):
    state = goal_state[:]
    blank_pos = state.index(0)
    n = int(len(state) ** 0.5)
    last_move = None

    moves = []
    for _ in range(n_actions):
        valid_moves = []

        if blank_pos % n > 0 and last_move != 'R':
            valid_moves.append('L')
        if blank_pos % n < n - 1 and last_move != 'L':
            valid_moves.append('R')
        if blank_pos // n > 0 and last_move != 'D':
            valid_moves.append('U')
        if blank_pos // n < n - 1 and last_move != 'U':
            valid_moves.append('D')

        move = random.choice(valid_moves)
        moves.append(move)
        last_move = move

        if move == 'L':
            state[blank_pos], state[blank_pos - 1] = state[blank_pos - 1], state[blank_pos]
            blank_pos -= 1
        elif move == 'R':
            state[blank_pos], state[blank_pos + 1] = state[blank_pos + 1], state[blank_pos]
            blank_pos += 1
        elif move == 'U':
            state[blank_pos], state[blank_pos - n] = state[blank_pos - n], state[blank_pos]
            blank_pos -= n
        elif move == 'D':
            state[blank_pos], state[blank_pos + n] = state[blank_pos + n], state[blank_pos]
            blank_pos += n

    return state

# def draw_search_tree_hierarchical(tree):
#     G = nx.DiGraph()

#     def add_node_and_children(node, depth=0):
#         state_str = str(node.state.state)
#         node_label = f"State: {state_str}\nEval: {node.evaluation_function}\nF: {node.F}"
#         G.add_node(node, label=node_label, depth=depth)

#         if node in tree:
#             for child in tree[node]:
#                 G.add_edge(node, child)
#                 add_node_and_children(child, depth + 1)

#     root = next(iter(tree))
#     add_node_and_children(root)

#     # Custom hierarchical layout
#     pos = {}
#     nodes_at_depth = {}
#     for node, data in G.nodes(data=True):
#         depth = data['depth']
#         if depth not in nodes_at_depth:
#             nodes_at_depth[depth] = []
#         nodes_at_depth[depth].append(node)

#     max_depth = max(nodes_at_depth.keys())
#     for depth, nodes in nodes_at_depth.items():
#         y = 1 - (depth / max_depth)
#         width = len(nodes)
#         for i, node in enumerate(nodes):
#             x = (i + 1) / (width + 1)
#             pos[node] = (x, y)

#     plt.figure(figsize=(20, 10))
#     nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightblue',
#             font_size=18, font_weight='bold', arrows=True)

#     labels = nx.get_node_attributes(G, 'label')
#     nx.draw_networkx_labels(G, pos, labels, font_size=9)

#     plt.title("Hierarchical Search Tree")
#     plt.axis('off')
#     plt.tight_layout()
#     plt.show()
