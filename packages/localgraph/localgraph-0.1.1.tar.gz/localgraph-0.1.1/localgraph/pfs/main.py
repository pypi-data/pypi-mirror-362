# Pathwise feature selection (PFS)

from ipss import ipss
import numpy as np

from .helpers import lightest_paths, prune_graph

def pfs(X, target_features, qpath_max, max_radius=3, fdr_local=None, custom_nbhd=None, feature_names=None, 
	criterion='min', selector='gb', ipss_args=None, verbose=False):
	"""
	Inputs:
		Required
		----------------
		X: n-by-p data matrix (n = number of samples, p = number of features)
		target_features: list of indices of the target features
		qpath_max: maximum allowed sum of q-values along paths

		Optional
		----------------
		max_radius: maximum radius of the estimated local graph
		fdr_local: neighborhood FDR threshold at each radius (list of length max_radius)
		custom_nbhd: dictionary of custom neighborhood FDR thresholds for user-specified features
		feature_names: names of the features, used if custom_nbhd is provided
		criterion:
		selector: base method for computing q-values
		ipss_args: additional arguments passed to the IPSS function
		verbose: whether to print progress during selection

	Outputs:
		A dictionary containing:
			- 'Q': dict mapping edge tuples to q-values
			- 'A': adjusted sparse adjacency matrix (dict of dicts or matrix)
	"""

	if fdr_local is None:
		fdr_local = [qpath_max] * max_radius

	if ipss_args is None:
		ipss_args = {}
	ipss_args['selector'] = selector

	if isinstance(target_features, int):
		target_features = [target_features]

	current_features = set(target_features)
	all_visited = set(target_features)
	radius = 0
	Q = {}

	while current_features and radius < max_radius:

		if verbose:
			n_current = len(current_features)
			ipss_iteration = 1
			print(f'current features: {current_features} (radius = {radius + 1}/{max_radius})')

		cutoff = fdr_local[radius]

		new_features = set()

		for current in current_features:

			if verbose:
				print(f' - iteration {ipss_iteration}/{len(current_features)}')
				ipss_iteration += 1

			# current custom neighborhood
			customize = False
			if custom_nbhd is not None:
				if feature_names is None:
					raise ValueError('Feature names must be provided if custom_nbhd is not None.')
				current_feature_name = feature_names[current]
				if current_feature_name in custom_nbhd:
					current_custom_nbhd = custom_nbhd[current_feature_name]
					current_custom_nbhd.setdefault('nbhd_fdr', cutoff)
					customize = True

			# compute q-values
			X_minus_current = np.delete(X, current, axis=1)
			result = ipss(X_minus_current, X[:,current], **ipss_args)

			efp_scores = result['efp_scores']
			q_values = result['q_values']

			for feature_idx, q_value in q_values.items():
				# reindex feature to account for deletion of current feature in X_minus_current
				feature_idx = feature_idx if feature_idx < current else feature_idx + 1

				if customize:
					# start with user-specified neighborhood fdr threshold
					current_cutoff = current_custom_nbhd.get('nbhd_fdr', cutoff)
					# override if any matching keyword is in the neighbor feature name
					for string, custom_fdr in current_custom_nbhd.items():
						if string != 'nbhd_fdr' and string in feature_names[feature_idx]:
							current_cutoff = custom_fdr
							break
				else:
					current_cutoff = cutoff

				# update if feature is entirely new
				if q_value <= current_cutoff and feature_idx not in all_visited:
					Q[(current, feature_idx)] = Q[(feature_idx, current)] = q_value
					new_features.add(feature_idx)

				# update if feature in same layer as current
				elif feature_idx in current_features:
					if q_value <= current_cutoff:
						if (feature_idx, current) not in Q:
							Q[(current, feature_idx)] = Q[(feature_idx, current)] = q_value
						elif Q[(feature_idx, current)] > q_value:
							Q[(current, feature_idx)] = Q[(feature_idx, current)] = q_value					

				# update edge with minimum q-value if criterion is 'min'
				elif q_value <= current_cutoff and criterion == 'min':
					if (feature_idx, current) not in Q:
						Q[(current, feature_idx)] = Q[(feature_idx, current)] = q_value
					elif Q[(feature_idx, current)] > q_value:
						Q[(current, feature_idx)] = Q[(feature_idx, current)] = q_value

		q_paths = lightest_paths(Q, target_features, new_features)
		new_features = {idx for idx, q_value_sum in q_paths.items() if q_value_sum <= qpath_max}

		current_features = new_features
		all_visited.update(new_features)
		radius += 1

	# Compute final Q by applying pathwise threshold qpath_max
	Q = prune_graph(Q, target_features, qpath_max, fdr_local, max_radius, custom_nbhd=custom_nbhd, feature_names=feature_names)

	return Q




