import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [['A', 'B'], ['B', 'C'], ['B', 'D']]
G.add_edges_from(edges)

pos = nx.spring_layout(G)

print(G.edges())

fig, ax = plt.subplots(figsize=(1,1))

nx.draw(G, pos, ax = ax, with_labels = True, font_size = 5, node_size = 200, node_color = 'lightgreen', labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels={('A', 'B'): 'AB', 
                 ('B', 'C'): 'BC', 
                 ('B', 'D'): 'BD'},
    font_color='red'
)
plt.axis('off')
plt.show()