from matplotlib import pyplot as plt
import matplotlib.colors as colors
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import networkx as nx
import numpy as np

from utils import synthetic_structsim
from utils import featgen

plt.switch_backend('agg')

def perturb_new(graph_list, p):
    ''' Perturb the list of graphs by adding/removing edges.
    Args:
        p_add: probability of adding edges. If None, estimate it according to graph density,
            such that the expected number of added edges is equal to that of deleted edges.
        p_del: probability of removing edges
    Returns:
        A list of graphs that are perturbed from the original graphs
    '''
    perturbed_graph_list = []
    for G_original in graph_list:
        G = G_original.copy()
        edge_remove_count = 0
        for (u, v) in list(G.edges()):
            if np.random.rand()<p:
                G.remove_edge(u, v)
                edge_remove_count += 1
        # randomly add the edges back
        for i in range(edge_remove_count):
            while True:
                u = np.random.randint(0, G.number_of_nodes())
                v = np.random.randint(0, G.number_of_nodes())
                if (not G.has_edge(u,v)) and (u!=v):
                    break
            G.add_edge(u, v)
        perturbed_graph_list.append(G)
    return perturbed_graph_list

    

#####
#
# Generate input graph
#
#####
def gen_syn1(feature_generator=None):
    basis_type = 'ba'
    nb_shapes = 30
    list_shapes = [['house']] * nb_shapes
    width_basis = 150

    fig = plt.figure(figsize=(8,6), dpi=300)

    G, role_id, plugins = synthetic_structsim.build_graph(width_basis, basis_type, list_shapes, start=0)
    print(role_id)
    G = perturb_new([G], 0.05)[0]

    if feature_generator is None:
        feature_generator = featgen.ConstFeatureGen(1)
    feature_generator.gen_node_features(G)

    name = basis_type + '_' + str(width_basis) + '_' + str(nb_shapes)

    return G, name

def preprocess_input_graph(G, normalize_adj=False):
    adj = np.array(nx.to_numpy_matrix(G))
    if normalize_adj:
        sqrt_deg = np.diag(1.0 / np.sqrt(np.sum(adj, axis=0, dtype=float).squeeze()))
        adj = np.matmul(np.matmul(sqrt_deg, adj), sqrt_deg)

    feat_dim = G.node[0]['feat'].shape(0)
    f = np.zeros((self.max_num_nodes, self.feat_dim), dtype=float)
    for i, u in enumerate(G.nodes()):
        f[i, :] = G.node[u]['feat']

    data = {'adj': adj, 'feat': f}

if __name__ == "__main__":
    G, name = gen_syn1(feature_generator=featgen.ConstFeatureGen(np.ones(5, dtype=float)))

    fig = plt.figure(figsize=(8,6), dpi=300)
    nx.draw(G, node_size=50, node_color='#336699',
                edge_color='grey', width=0.5, alpha=0.7)
    fig.canvas.draw()

    plt.savefig('syn/graph_' + name)
    plt.close()

