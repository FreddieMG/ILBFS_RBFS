




class EightPuzzleState:
    def __init__(self, state):
        self.state = state
        self.n = len(state)

    def is_goal(self):
        # Check if the state is in ascending order with 0 at the end
        return self.state == [1, 2, 3, 4, 5, 6, 7, 8, 0]

    def get_state_as_list(self):
        return list(self.state)

    def get_neighbors(self):
        neighbors = []
        blank_index = self.state.index(0)
        row, col = divmod(blank_index, 3)

        # Define possible moves (up, down, left, right)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_blank_index = new_row * 3 + new_col
                new_state = self.state[:]
                new_state[blank_index], new_state[new_blank_index] = new_state[new_blank_index], new_state[blank_index]
                neighbors.append((new_state, 1))
        return neighbors


class EightPuzzleNode:
    def __init__(self, state, parent=None, action=None, path_cost=0, needs_heuristic=True):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.creation_time = None
        self.needs_heuristic = needs_heuristic
        self.evaluation_function = self.path_cost + self.heuristic() if needs_heuristic else self.path_cost
        self.F = self.evaluation_function

    def __repr__(self):
        return f"State: {self.state.state}, f:{self.evaluation_function}, F:{self.F}"

    def __hash__(self):
        return hash((tuple(self.state.state), self.parent))

    def __eq__(self, other):
        return self.state.state == other.state.state and self.creation_time == other.creation_time

    def __lt__(self, other):
        if self.F < other.F:
            return True

        if self.F == other.F:
            criterion = self.creation_time > other.creation_time
            return criterion

        return False

    def heuristic(self):
        # Manhattan distance heuristic
        goal_positions = [(i // 3, i % 3) for i in range(0, 8)]
        current_positions = [(self.state.state.index(i) // 3, self.state.state.index(i) % 3) for i in range(1, 9)]
        return sum(
            abs(current_positions[i][0] - goal_positions[i][0]) + abs(current_positions[i][1] - goal_positions[i][1])
            for i in range(8))




    def goal_test(self):
        return self.state.is_goal()

    def generate_child(self):
        children = []
        for neighbor, cost in self.state.get_neighbors():
            child_state = EightPuzzleState(neighbor)
            child_node = EightPuzzleNode(child_state, parent=self, path_cost=self.path_cost + cost)
            children.append(child_node)
        return children

    def find_solution(self):
        solution = []
        node = self
        while node:
            solution.append(node.state.get_state_as_list())
            node = node.parent
        return solution[::-1]

    def draw_search_tree_hierarchical(tree):
        G = nx.DiGraph()

        def add_node_and_children(node, depth=0):
            state_str = str(node.state.state)
            node_label = f"State: {state_str}\nEval: {node.evaluation_function}\nF: {node.F}"
            G.add_node(node, label=node_label, depth=depth)

            if node in tree:
                for child in tree[node]:
                    G.add_edge(node, child)
                    add_node_and_children(child, depth + 1)

        root = next(iter(tree))
        add_node_and_children(root)

        # Custom hierarchical layout
        pos = {}
        nodes_at_depth = {}
        for node, data in G.nodes(data=True):
            depth = data['depth']
            if depth not in nodes_at_depth:
                nodes_at_depth[depth] = []
            nodes_at_depth[depth].append(node)

        max_depth = max(nodes_at_depth.keys())
        for depth, nodes in nodes_at_depth.items():
            y = 1 - (depth / max_depth)
            width = len(nodes)
            for i, node in enumerate(nodes):
                x = (i + 1) / (width + 1)
                pos[node] = (x, y)

        plt.figure(figsize=(20, 10))
        nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightblue',
                font_size=18, font_weight='bold', arrows=True)

        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=9)

        plt.title("Hierarchical Search Tree")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

