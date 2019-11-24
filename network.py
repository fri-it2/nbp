import networkx as nx
import pandas as pd
import matplotlib.patches as mpatches


red_patch = mpatches.Patch(color='red', label='2Mbps')
blue_patch = mpatches.Patch(color='blue', label='10Mbps')
gray_patch = mpatches.Patch(color='gray', label='1200kbps')
yellow_patch = mpatches.Patch(color='yellow', label='4Mbps')

import matplotlib.pyplot as plt
edgelist = pd.read_csv('/home/home/Documents/nbp-doktorat/omrezje.csv')
nodelist = pd.read_csv('/home/home/Documents/nbp-doktorat/vozlisce.csv')
g = nx.Graph()
for i, elrow in edgelist.iterrows():
    g.add_edge(elrow[0], elrow[1], attr_dict=elrow[2:].to_dict())
for i, nlrow in nodelist.iterrows():
    g.node[nlrow['id']] = nlrow[1:].to_dict()
#node_positions = {node[0]: (node[1]['x'], -node[1]['y']) for node in g.nodes(data=True)}
#print(node_positions)
edge_colors = [e[2]['color'] for e in g.edges(data=True)]
plt.figure(figsize=(8, 6))
path = dict(nx.all_pairs_shortest_path(g))
print(path)
print(edge_colors)
#nx.draw(g, edge_color=edge_colors, node_size=5, node_color='black',with_labels=True, distance=True, weight=True,pos=nx.spring_layout(g),prog='neato')
nx.draw(g, edge_color=edge_colors, node_size=5, node_color='black',with_labels=True, distance=True, weight=True)
plt.legend(handles=[red_patch,blue_patch,gray_patch,yellow_patch])
plt.title('NBP omrezje', size=20)
plt.show()
