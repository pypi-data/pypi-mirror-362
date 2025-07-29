# A simple example of local graph estimation with pathwise feature selection (PFS)

from localgraph import pfs, plot_graph
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------
# Setup
#--------------------------------
np.random.seed(302)
n, p = 100, 50

#--------------------------------
# Generate true graph and samples
#--------------------------------
# define nonlinear function
def f(x):
	return np.exp(-x**2 / 2)

# generate data
def generate_data(n, p, target_feature=0, snr=2):
	X = np.random.normal(0, 1, size=(n,p))

	# radius 2 (linear realtionships)
	X[:,1] += X[:,3] + X[:,5]
	X[:,2] += X[:,4] + X[:,6]

	# radius 1 (nonlinear relationships)
	signal = f(X[:,1]) + f(X[:,2])
	sigma2 = np.var(signal) / snr
	X[:,target_feature] = signal + np.random.normal(0, np.sqrt(sigma2), size=n)

	# Construct true adjacency matrix
	A_true = np.zeros((p,p))
	true_edges = [(3,1), (5,1), (4,2), (6,2), (1,target_feature), (2,target_feature)]
	for i, j in true_edges:
		A_true[i,j] = 1
		A_true[j,i] = 1

	return X, target_feature, A_true

# generate data
X, target_feature, A_true = generate_data(n,p)

#--------------------------------
# Run PFS
#--------------------------------
qpath_max = 0.1
max_radius = 2
Q = pfs(X, target_feature, qpath_max=qpath_max, max_radius=max_radius, verbose=True)

#--------------------------------
# Plot true and estimated local graphs
#--------------------------------
fig, axes = plt.subplots(1, 2, figsize=(18,8))

# Plot true graph
plot_graph(graph=A_true, target_features=target_feature, radius=max_radius, edge_widths=3, ax=axes[0], show_weights=False)
axes[0].set_title('True Graph', fontsize=24)

# Plot estimated graph
plot_graph(graph=Q, target_features=target_feature, radius=max_radius, true_graph=A_true, edge_widths=3, ax=axes[1])
axes[1].set_title('Estimated Graph', fontsize=24)

plt.tight_layout()
plt.show()
