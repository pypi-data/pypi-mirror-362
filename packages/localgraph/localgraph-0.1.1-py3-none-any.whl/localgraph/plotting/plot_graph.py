# Plot a local subgraph around target features, with flexible graph input

import copy

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from .helpers import assign_node_colors, generate_colors

def plot_graph(
	graph, target_features, radius, feature_names=None, true_graph=None,
	graph_layout='kk', node_size=1500, font_size=10, edge_font_size=None, edge_digits=2, edge_widths=1, colors=None,
	show_weights=True, include_outer_edges=False, figsize=(16,8), ax=None, pos=None,
	save_fig=False, save_graph=False, graph_name=None, dpi=300
):
	"""
	Inputs:
		Required
		----------------
		graph: input graph, either as a dictionary of edge weights, a numpy array (adjacency matrix), or NetworkX graph
		target_features: list of indices of the target features
		radius: maximum radius of the local graph

		Optional
		----------------
		# Labeling
		feature_names: list of feature names for labeling nodes
		true_graph: ground truth adjacency matrix, if known (used to color true/false edges black/red)
		
		# Visualization
		graph_layout: layout algorithm (several options from NetworkX; default is kamada-kawai)
		node_size: size of nodes in the plot
		font_size: size of node labels
		edge_font_size: size of edge weight labels
		edge_digits: number of digits to round edge weights
		edge_widths: width of edges (float for uniform width; 'q_value' to scale by q-values)
		colors: list of custom colors for nodes (default: color by distance from target nodes)
		show_weights: whether to display edge weights
		include_outer_edges: whether to include edges between outermost nodes
		figsize: size of the figure (width, height)
		ax: matplotlib axis object (for use in subplots or custom figures)
		pos: dictionary of node positions (overrides automatic layout)

		# Saving
		save_fig: whether to save the figure as a PNG
		save_graph: whether to save the graph as a GraphML file
		graph_name: name of the output file if saving
		dpi: resolution of the saved figure

	Outputs:
		Returns a dictionary containing:
			- 'feature_radius_list': list of (feature_name, radius) pairs for each node in the plotted subgraph
			- 'graph': NetworkX graph object for the plotted subgraph
			- 'positions': dictionary mapping nodes to their 2D coordinates in the plot
	"""

	if edge_font_size is None:
		edge_font_size = font_size

	# Create networkx graph G from graph
	if isinstance(graph, nx.Graph):
		G = graph.copy()
	elif isinstance(graph, dict):
		G = nx.Graph()
		for (i,j), q in graph.items():
			G.add_edge(i, j, weight=q)
	elif isinstance(graph, np.ndarray):
		G = nx.Graph()
		for i in range(graph.shape[0]):
			for j in range(graph.shape[1]):
				weight = graph[i,j]
				if weight != 0:
					G.add_edge(i, j, weight=weight)
	else:
		raise TypeError("Unsupported graph input type. Must be a NetworkX graph, dict, or numpy array.")

	# Find nodes within the specified radius
	reachable_nodes = set()
	node_distances = {}

	if isinstance(target_features, int):
		target_features = [target_features]

	for root in target_features:
		if G.has_node(root):
			path_lengths = nx.single_source_shortest_path_length(G, root, cutoff=radius)
			reachable_nodes.update(path_lengths.keys())
			for node, dist in path_lengths.items():
				if node not in node_distances or dist < node_distances[node]:
					node_distances[node] = dist

	# Remove edges between outermost nodes if requested
	if not include_outer_edges:
		outer_nodes = {node for node, dist in node_distances.items() if dist == radius}
		G.remove_edges_from([(u, v) for u, v in G.edges() if u in outer_nodes and v in outer_nodes])

	# Create subgraph
	G = G.subgraph(reachable_nodes).copy()

	if G.number_of_nodes() == 0:
		print("Empty graph: All root nodes are isolated.")
		return

	# Handle plotting
	own_figure = False
	if ax is None:
		fig, ax = plt.subplots(figsize=figsize)
		own_figure = True

	# Graph layout selection
	if pos is not None:
		pos = {node: (float(x), float(y)) for node, (x, y) in pos.items()}
	else:
		if graph_layout == 'circular':
			pos = nx.circular_layout(G)
		elif graph_layout in ['kk', 'kamada_kawai']:
			pos = nx.kamada_kawai_layout(G, weight=False)
		elif graph_layout == 'multipartite':
			pos = nx.multipartite_layout(G)
		elif graph_layout == 'planar':
			pos = nx.planar_layout(G)
		elif graph_layout == 'spectral':
			pos = nx.spectral_layout(G)
		elif graph_layout == 'spring':
			pos = nx.spring_layout(G, weight=None)
		else:
			raise ValueError(f"Unsupported graph format: {graph_layout}")

	# Assign node colors
	node_color = assign_node_colors(G, target_features, radius, colors=colors)

	# Get weights
	weights = [G[u][v]['weight'] for u, v in G.edges()]
	max_weight = max(weights) if weights else 1

	# Assign edge colors based on whether they exist in true_graph
	if true_graph is not None:
		true_edges = set()
		for i in range(true_graph.shape[0]):
			for j in range(true_graph.shape[1]):
				if true_graph[i,j] != 0:
					true_edges.add((i,j))
					true_edges.add((j,i))
		edge_colors = ['black' if (u,v) in true_edges else 'red' for u, v in G.edges()]
	else:
		edge_colors = ['black' for u, v, in G.edges()]

	# Node sizes
	node_sizes = [node_size * 1.5 if node in target_features else node_size for node in G.nodes()]

	# Edge widths
	edge_widths_clean = str(edge_widths).replace('-', '_').lower()
	if edge_widths_clean in ['by_q_value', 'q_value']:
		q_vals = [G[u][v]['weight'] for u, v in G.edges()]
		q_min, q_max = min(q_vals), max(q_vals)
		if q_max == q_min:
			edge_widths = 1
		else:
			def rescale(q):
				t = (q - q_min) / (q_max - q_min)
				return max(5 * (1 - t), 1)
			edge_widths = [rescale(G[u][v]['weight']) for u, v in G.edges()]

	# Draw nodes and edges
	nx.draw(G, pos, ax=ax, with_labels=False, node_color=node_color, node_size=node_sizes, edge_color=edge_colors,
			edgecolors='black', linewidths=1, alpha=1, width=edge_widths)

	if show_weights:
		edge_labels = {(u, v): f'{G[u][v]["weight"]:.{edge_digits}f}' for u, v in G.edges()}
		text_items = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=edge_font_size, ax=ax)
		# Manually update colors
		for (u,v), text in text_items.items():
			if true_graph is not None:
				edge_color = 'black' if (u,v) in true_edges else 'red'
			else:
				edge_color = 'black'
			text.set_color(edge_color)  # Change label color dynamically

	# Add custom node labels
	if feature_names is None:
		node_labels = {node: f'$X_{{{node + 1}}}$' for node in reachable_nodes}
	else:
		node_labels = {node: feature_names[node] for node in reachable_nodes}

	# Custom node labels with individual font sizes
	for node, (x,y) in pos.items():
		label = node_labels[node]
		node_font_size = int(font_size * 1.25) if node in target_features else font_size
		ax.text(x, y, label, fontsize=node_font_size, ha='center', va='center', 
				bbox=dict(facecolor='white', edgecolor='none', alpha=0))  # Background for readability

	# Collect (feature_name, radius) pairs
	assigned_nodes = set()
	radius_groups = {}

	for r in range(max(node_distances.values()) + 1):
		nodes_at_r = {node for node, dist in node_distances.items() if dist == r}
		new_nodes = nodes_at_r - assigned_nodes
		if new_nodes:
			radius_groups[r] = new_nodes
			assigned_nodes.update(new_nodes)

	feature_radius_list = []
	for r in sorted(radius_groups):
		for node in sorted(radius_groups[r]):
			name = node_labels[node]
			feature_radius_list.append((name, r))

	if own_figure:
		plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
		if save_fig:
			if graph_name is None:
				print(f'Warning: graph_name not provided. Setting graph_name = my_graph')
				graph_name = 'my_graph'
			plt.savefig(f'{graph_name}.png', dpi=dpi)
		plt.show()

	if save_graph:
		if graph_name is None:
			print(f'Warning: graph_name not provided. Setting graph_name = my_graph')
			graph_name = 'my_graph'
		for node, (x, y) in pos.items():
			G.nodes[node]['x'] = float(x)
			G.nodes[node]['y'] = float(y)
		nx.write_graphml(G, f'{graph_name}.graphml')

	result = {'feature_radius_list':feature_radius_list, 'graph':G, 'positions':pos}
	if own_figure:
		result['figure'] = fig

	return result




