"""
Artificial Intelligence Assignment
Topic: Problem Solving by Search - Uninformed (Blind) Search
Algorithms: BFS, DFS, DLS, IDDFS, UCS
"""

from collections import deque
import heapq

# ---------------------------------------------------------------
# Input (Tree) - unweighted, used by BFS, DFS, DLS, IDDFS
#
#            A
#          /   \
#         B     C
#        / \   / \
#       D   E F   G
#       |
#       H
# ---------------------------------------------------------------
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': [],
    'G': [],
    'H': [],
}

# ---------------------------------------------------------------
# Input (Weighted Graph) - used by UCS
# ---------------------------------------------------------------
weighted_graph = {
    'S': [('A', 1), ('B', 4)],
    'A': [('B', 2), ('C', 5)],
    'B': [('C', 1)],
    'C': [('G', 3)],
    'G': [],
}


# 1. Breadth First Search (BFS) - uses a Queue (FIFO)
def bfs(graph, start):
    visited = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            queue.extend(graph[node])
    return visited


# 2. Depth First Search (DFS) - uses a Stack (LIFO)
def dfs(graph, start):
    visited = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            # reversed so the left-most child is explored first
            stack.extend(reversed(graph[node]))
    return visited


# 3. Depth Limited Search (DLS) - DFS with a depth limit
def dls(graph, node, goal, limit, path=None):
    path = (path or []) + [node]
    if node == goal:
        return path
    if limit == 0:
        return None
    for child in graph[node]:
        result = dls(graph, child, goal, limit - 1, path)
        if result:
            return result
    return None


# 4. Iterative Deepening DFS (IDDFS) - DLS with limit 0, 1, 2, ...
def iddfs(graph, start, goal, max_depth=10):
    for depth in range(max_depth + 1):
        result = dls(graph, start, goal, depth)
        if result:
            return result, depth
    return None, None


# 5. Uniform Cost Search (UCS) - Priority Queue ordered by path cost
def ucs(graph, start, goal):
    frontier = [(0, start, [start])]  # (cost, node, path)
    explored = set()
    while frontier:
        cost, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, cost
        if node in explored:
            continue
        explored.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + weight, neighbor, path + [neighbor]))
    return None, None


# ---------------------------------------------------------------
# Output
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("Tree: A -> (B, C), B -> (D, E), C -> (F, G), D -> (H)")
    print("=" * 50)

    print("\n1. BFS Traversal :", bfs(tree, 'A'))
    print("2. DFS Traversal :", dfs(tree, 'A'))

    print("\n3. DLS (goal = H)")
    for limit in (2, 3):
        res = dls(tree, 'A', 'H', limit)
        print(f"   limit = {limit} ->", res if res else "Goal not found")

    path, depth = iddfs(tree, 'A', 'G')
    print("\n4. IDDFS (goal = G)")
    print("   Path  :", path)
    print("   Depth :", depth)

    path, cost = ucs(weighted_graph, 'S', 'G')
    print("\n5. UCS (start = S, goal = G)")
    print("   Path       :", path)
    print("   Total Cost :", cost)
