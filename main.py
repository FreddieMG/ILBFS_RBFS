from sys import maxsize
import time
import time
import pickle
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

import random
import sys
from ilbfs import *
from ilbfs_order import *
from RBFS import *
from RBFS_order import *

sys.setrecursionlimit(2000)





goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
required_runs_per_bin = 10
target_bins = [1, 2, 3,  4, 5, 6,  7, 9, 11, 13, 15]
#
results = defaultdict(lambda: {'rbfs': [], 'ilbfs_sift_down': [], 'ilbfs_heapify': []})

# Generate data for each target bin
for n_actions in target_bins:
    while len(results[n_actions + 1]['rbfs']) < required_runs_per_bin:
        random_state = generate_random_state_from_goal(goal_state, n_actions)

        # RBFS
        start_time = time.time()
        solution, expanded_nodes = recursive_best_first_search_with_order(random_state)
        rbfs_time = time.time() - start_time
        rbfs_solution_length = len(solution)

        # ILBFS with Sift Down
        start_time = time.time()
        ilbfs_sift_down_solution = ilbfs_with_order_sift_down(random_state, expanded_nodes)
        ilbfs_sift_down_time = time.time() - start_time

        # ILBFS with Heapify
        start_time = time.time()
        ilbfs_heapify_solution = ilbfs_with_order_heapify(random_state, expanded_nodes)
        ilbfs_heapify_time = time.time() - start_time

        print(rbfs_solution_length)

        results[rbfs_solution_length]['rbfs'].append(rbfs_time)
        results[rbfs_solution_length]['ilbfs_sift_down'].append(ilbfs_sift_down_time)
        results[rbfs_solution_length]['ilbfs_heapify'].append(ilbfs_heapify_time)


# Save results to a file
results = dict(results)
with open('search_results.pkl', 'wb') as f:
    pickle.dump(results, f)





# Load results from the file
with open('search_results.pkl', 'rb') as f:
    results = pickle.load(f)

# Calculate average runtimes
average_times = {
    length: {
        'rbfs': np.mean(times['rbfs']),
        'ilbfs_sift_down': np.mean(times['ilbfs_sift_down']),
        'ilbfs_heapify': np.mean(times['ilbfs_heapify'])
    } for length, times in results.items() if len(times['rbfs']) >= required_runs_per_bin
}

# Extract data for plotting
lengths = sorted(average_times.keys())
rbfs_times = [average_times[length]['rbfs'] for length in lengths]
ilbfs_sift_down_times = [average_times[length]['ilbfs_sift_down'] for length in lengths]
ilbfs_heapify_times = [average_times[length]['ilbfs_heapify'] for length in lengths]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(lengths, rbfs_times, label='RBFS', marker='o')
plt.plot(lengths, ilbfs_sift_down_times, label='ILBFS (Sift Down)', marker='x')
plt.plot(lengths, ilbfs_heapify_times, label='ILBFS (Heapify)', marker='s')

plt.xlabel('Solution Length')
plt.ylabel('Average Runtime (seconds)')
plt.title('Comparison of Average Runtimes by Solution Length')
plt.legend()
plt.grid(True)
plt.show()

