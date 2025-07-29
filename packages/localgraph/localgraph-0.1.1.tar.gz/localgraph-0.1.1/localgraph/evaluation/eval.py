# Functions for evaluating local graph estimation performance

from collections import deque

import numpy as np

def subgraph_within_radius(A, target_nodes, radius):
	"""
	Returns a subgraph of nodes and edges that are at most `radius` distance from the target nodes.

	Parameters:
	- A: Adjacency matrix (numpy array) of the graph.
	- radius: Maximum distance from the target nodes.
	- target_nodes: List of target node indices.

	Returns:
	- A_r: Symmetric adjacency matrix of the subgraph.
	"""
	n = A.shape[0]  # Number of nodes in the graph
	visited = set()  # Nodes within the radius
	queue = deque()

	if isinstance(target_nodes, int):
		target_nodes = [target_nodes]

	# Initialize the queue with target nodes
	for node in target_nodes:
		queue.append((node, 0))  # (node, distance from target)
		visited.add(node)

	# Perform BFS to find all nodes within the radius
	while queue:
		current_node, current_distance = queue.popleft()
		if current_distance >= radius:
			continue  # Stop if we exceed the radius

		# Explore neighbors
		for neighbor in np.where(A[current_node] > 0)[0]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append((neighbor, current_distance + 1))

	# Create the subgraph adjacency matrix
	visited = sorted(visited)  # Sort for consistent indexing
	A_r = np.zeros_like(A)  # Initialize the subgraph matrix

	# Fill the subgraph matrix
	for i in visited:
		for j in visited:
			A_r[i, j] = A[i, j]  # Copy edges from the original graph

	return A_r

def tp_and_fp(A, A_true, target_features, radius=None):
	"""
	Compute the number of true and false edges in an estimated graph

	Parameters:
	- A : dict or np.ndarray
		Estimated adjacency structure, either as a dictionary of edge q-values 
		or a binary adjacency matrix.
	- A_true : np.ndarray
		Ground-truth binary adjacency matrix.
	- target_features : list of int
		Indices of target nodes around which the local subgraph is evaluated.
	- radius : int or None, optional
		Radius of the local neighborhood around target features. If None, counts
		are computed over the full graph.

	Returns:
	- tp : int
		Number of true positive edges.
	- fp : int
		Number of false positive edges.

	Notes:
		- If `radius` is specified, edges are evaluated within the radius neighborhood 
			of target nodes, excluding edges between two nodes at the outermost radius.
	"""

	# Convert dictionary of q-values to a matrix
	if isinstance(A, dict):
		p = A_true.shape[0]
		A_matrix = np.zeros((p,p))
		for (i,j), q in A.items():
			A_matrix[i,j] = q
			A_matrix[j,i] = q
		A = A_matrix

	A = (A != 0).astype(int)
	p = A.shape[0]
	if not np.all(A == A.T):
		num_asymmetric = np.sum(A != A.T)
		max_diff = np.max(np.abs(A - A.T))
		print(f"A is not symmetric: {num_asymmetric} asymmetric entries.")
		print(f"Maximum absolute difference: {max_diff}")
		raise ValueError(f'A is not symmetric.')
	if not np.all(A_true == A_true.T):
		raise ValueError(f'A_true is not symmetric.')

	if radius is None:
		tp, fp = 0, 0
		for i in range(p):
			for j in range(i+1,p):
				if A[i,j] == 1:
					if A_true[i,j] == 1:
						tp += 1
					else:
						fp += 1
	else:
		A_true = subgraph_within_radius(A_true, target_features, radius)

		visited = np.zeros(p, dtype=bool)
		nodes_within_radius = set()
		nodes_at_outer_radius = set()

		# Perform BFS to identify all nodes within the given radius
		for target in target_features:
			queue = deque([(target, 0)])  # (node, current_distance)
			while queue:
				node, dist = queue.popleft()
				if dist > radius or visited[node]:
					continue
				visited[node] = True
				if dist < radius:
					nodes_within_radius.add(node)
				elif dist == radius:
					nodes_at_outer_radius.add(node)

				for neighbor in range(p):
					if A[node, neighbor] == 1 and not visited[neighbor]:
						queue.append((neighbor, dist + 1))

		# Reset visited to reuse for the TP/FP calculation
		visited.fill(False)

		tp, fp = 0, 0
		# Check edges in the subgraph, but **exclude edges between two outer radius nodes**
		for i in nodes_within_radius | nodes_at_outer_radius:
			for j in range(i + 1, p):  # Upper triangular part
				if j in nodes_within_radius | nodes_at_outer_radius and A[i, j] == 1:
					if i in nodes_at_outer_radius and j in nodes_at_outer_radius:
						continue  # Exclude edges between outer radius nodes
					if A_true[i, j] == 1:
						tp += 1
					else:
						fp += 1

	return tp, fp


