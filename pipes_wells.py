from typing import List

class UnionFind:
    def __init__(self, size: int):
        # Initialize parent pointers and rank for Union-Find
        self.parent = list(range(size + 1))
        self.rank = [0] * (size + 1)

    def find(self, i: int) -> int:
        # Path compression
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        # Union by rank
        root_i = self.find(i)
        root_j = self.find(j)
        
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

def minCostSupplyWater(n: int, wells: List[int], pipes: List[List[int]]) -> int:
    edges = []
    
    # 1. Add edges from the virtual node (0) to each house for the wells
    for i, cost in enumerate(wells):
        edges.append((cost, 0, i + 1))
    
    # 2. Add the existing pipes as edges
    for u, v, cost in pipes:
        edges.append((cost, u, v))
        
    # 3. Kruskal's Algorithm: Sort all edges by cost
    edges.sort()
    
    uf = UnionFind(n)
    min_cost = 0
    edges_used = 0
    
    # 4. Greedily pick the smallest edges that don't form a cycle
    for cost, u, v in edges:
        if uf.union(u, v):
            min_cost += cost
            edges_used += 1
            # A spanning tree has exactly 'n' edges for 'n+1' nodes (including node 0)
            if edges_used == n:
                break
                
    return min_cost

# ==========================================
# Testing the Code
# ==========================================
if __name__ == "__main__":
    print("Running test cases...\n")
    
    # Testing Case 1
    ans1 = minCostSupplyWater(3, [1, 2, 2], [[1, 2, 1], [2, 3, 1]])
    print(f"Testing Case 1 Output: {ans1} (Expected: 3)")
    
    # Testing Case 2
    ans2 = minCostSupplyWater(4, [1, 2, 2, 1], [[1, 2, 1], [1, 2, 3], [2, 3, 2], [3, 4, 3], [1, 4, 2]])
    print(f"Testing Case 2 Output: {ans2} (Expected: 5)")
    
    # Testing Case 3 (Note: Added the missing '[' to the pipes array from the prompt)
    ans3 = minCostSupplyWater(5, [10, 2, 2, 10, 2], [[1, 2, 1], [2, 3, 1], [3, 4, 1], [1, 4, 2], [2, 5, 2]])
    print(f"Testing Case 3 Output: {ans3} (Expected: 7)")
