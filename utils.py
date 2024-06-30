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

