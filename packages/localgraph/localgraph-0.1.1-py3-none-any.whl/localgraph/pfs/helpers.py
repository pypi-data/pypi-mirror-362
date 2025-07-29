# Helper functions for the main PFS function, main.py

import heapq

def lightest_paths(Q, target_features, new_features):
	"""
	Computes the lightest path (minimum cumulative q-value) from any target feature 
	to all new features using Dijkstra's algorithm.

	Parameters:
		Q (dict): Dictionary of edge q-values {(i, j): q}.
		target_features (set): Set of initial target features.
		new_features (set): Set of features for which to compute the lightest paths.

	Returns:
		dict: {feature: minimum cumulative q-value path} for all new_features.
	"""
	if isinstance(target_features, int):
		target_features = [target_features]

	pq = [(0, f) for f in target_features]  # Priority queue: (cumulative q-value, feature)
	heapq.heapify(pq)
	min_q_path = {f: 0 for f in target_features}  # Store minimum path values

	while pq:
		q_path, feature = heapq.heappop(pq)

		# Stop early if all new_features have been reached
		if new_features.issubset(min_q_path):
			break

		for neighbor in {j for i, j in Q.keys() if i == feature} | {i for i, j in Q.keys() if j == feature}:
			q_edge = Q[(feature, neighbor)]
			new_q_path = q_path + q_edge

			if neighbor not in min_q_path or new_q_path < min_q_path[neighbor]:
				min_q_path[neighbor] = new_q_path
				heapq.heappush(pq, (new_q_path, neighbor))

	# Return only computed paths for `new_features`
	return {f: min_q_path[f] for f in new_features}

def prune_graph(Q, target_features, qpath_max, fdr_local, max_radius, custom_nbhd=None, feature_names=None):
	"""
	Prunes the estimated graph by enforcing local FDR and pathwise q-value constraints.

	This function takes a dictionary of edge-level q-values and prunes it to retain only edges that:
		(1) satisfy local false discovery rate (FDR) thresholds at each radius, and
		(2) lie on a path from a target feature whose cumulative q-value does not exceed qpath_max.

	Inputs
	----------
	Q : dict
		Dictionary of edge-level q-values. Keys are (i,j) tuples and values are q-values.
	target_features : int or list of int
		Indices of target features around which the local graph is built.
	qpath_max : float
		Maximum allowed sum of q-values along any path from a target to another feature.
	fdr_local : list of float
		List of local FDR thresholds for each radius (length must equal max_radius).
	max_radius : int
		Maximum radius for local graph expansion.
	custom_nbhd : dict, optional
		Dictionary specifying custom FDR thresholds for specific features or substrings (default: None).
	feature_names : list of str, optional
		List of feature names (required if custom_nbhd is not None).

	Outputs
	-------
	Q_pruned : dict
		Dictionary of pruned edges (i,j) with their corresponding q-values.
	"""

	if not Q:
		return {}

	Q_pruned = {}

	if isinstance(target_features, int):
		target_features = [target_features]

	cumulative_q = {i: qpath_max + 1 for i in range(max(Q.keys(), key=lambda x: x[1])[1] + 1)}
	for feature in target_features:
		cumulative_q[feature] = 0

	current_set = set(target_features)
	radius = 0

	while current_set and radius < max_radius:
		next_set = set()

		for current in current_set:
			cutoff = fdr_local[radius]
			# Current custom neighborhood
			customize = False
			if custom_nbhd is not None:
				if feature_names is None:
					raise ValueError('Feature names must be provided if custom_nbhd is not None.')
				current_feature_name = feature_names[current]
				if current_feature_name in custom_nbhd:
					current_custom_nbhd = custom_nbhd[current_feature_name]
					current_custom_nbhd.setdefault('nbhd_fdr', cutoff)
					customize = True
			for (i,j), q in Q.items():
				# Only proceed if i is the index of the current feature
				if i != current:
					continue

				current_cutoff = cutoff

				# Apply custom FDR threshold based on matched feature name substrings
				if customize:
					current_cutoff = current_custom_nbhd['nbhd_fdr']
					for string, custom_fdr in custom_nbhd[current_feature_name].items():
						if string != 'nbhd_fdr' and string in feature_names[j]:
							current_cutoff = custom_fdr
							break

				if j in current_set and radius > 0:
					if q > current_cutoff:
						continue
					elif (j, current) in Q_pruned:
						Q_pruned[(current, j)] = min(q, Q_pruned[(j,current)])
					else:
						Q_pruned[(current, j)] = q
				elif q > current_cutoff:
					continue
				else:
					new_cumulative_q = cumulative_q[current] + q
					if new_cumulative_q <= qpath_max:
						if (j, current) in Q_pruned:
							Q_pruned[(current, j)] = min(q, Q_pruned[(j,current)])
						else:
							Q_pruned[(current, j)] = q
						if new_cumulative_q < cumulative_q[j]:
							cumulative_q[j] = new_cumulative_q
							next_set.add(j)

		current_set = next_set
		radius += 1

	return Q_pruned
