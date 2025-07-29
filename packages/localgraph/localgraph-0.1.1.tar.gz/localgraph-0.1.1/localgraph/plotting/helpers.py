# Helper functions for plot_graph.py

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def assign_node_colors(G, target_features, n_layers, colors=None):
	if colors is not None:
		if isinstance(colors, dict):
			return [colors.get(node, 'gray') for node in G.nodes()]
		elif isinstance(colors, (list, np.ndarray)):
			return [colors[node] if node < len(colors) else 'gray' for node in G.nodes()]
		else:
			raise ValueError("`colors` must be a dict, list, or None.")

	if isinstance(target_features, int):
		target_features = [target_features]

	# Default: color by distance from target_features
	color_map = {}
	standout_color = 'yellow'
	default_colors = generate_colors(n_layers)
	shortest_paths_from_roots = {
		r: nx.single_source_shortest_path_length(G,r) for r in target_features if r in G
	}

	for node in G.nodes():
		if node in target_features:
			color_map[node] = standout_color
		else:
			min_dist = min(
				paths.get(node, float('inf')) for paths in shortest_paths_from_roots.values()
			)
			if min_dist < float('inf'):
				color_map[node] = default_colors[min(min_dist - 1, len(default_colors) - 1)]
			else:
				color_map[node] = 'skyblue'

	return [color_map[node] for node in G.nodes()]

def generate_colors(n):
	"""Generate a yellow-green-blue gradient from 'gist_rainbow', skipping red/magenta."""
	colormap = plt.cm.get_cmap('gist_rainbow')
	colors = []
	for i in range(n):
		t = 0 if n == 1 else i / (n - 1)  # Normalize to [0,1]
		# Remap t to skip red and magenta sections (keep yellow-green-blue)
		t_new = 0.4 + 0.4 * t  # Maps t from [0.4, 0.8] in colormap
		# Get color from colormap
		color = np.array(colormap(t_new)[:3])
		# Reduce saturation as nodes get farther
		fade_factor = 0.65 - 0.55 * t  # High at t=0 (closer), fades at t=1 (farther)
		color = color * fade_factor + (1 - fade_factor)  # Desaturate progressively
		# Convert to hex
		colors.append('#%02x%02x%02x' % tuple(int(255 * c) for c in color))
	return colors


