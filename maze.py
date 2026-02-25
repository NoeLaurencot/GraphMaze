import networkx as nx
import matplotlib.pyplot as plt
import random

def create_maze(rows, cols, percentWallRemoved):
    G = nx.Graph()
    for row in range(rows):
        for col in range(cols):
            G.add_node((row, col))
            if row > 0:
                G.add_edge((row, col), (row - 1, col), weight=random.randint(1, 2))
            if col > 0:
                G.add_edge((row, col), (row, col - 1), weight=random.randint(1, 2))
    edges = list(G.edges())
    for i in range(int(len(edges) * percentWallRemoved)):
        edge = random.choice(edges)
        if G.degree(edge[0]) > 2 and G.degree(edge[1]) > 2:
            edges.remove(edge)
            G.remove_edge(*edge)
            print(edge)
    return G

def draw_maze(G):
    pos = {(r, c): (c, -r) for r, c in G.nodes()}
    nx.draw(G, pos, with_labels=True)
    plt.show()

def pick_end_node(G, rows, cols):
    nodes = list(G.nodes())
    outside_nodes = []
    for node in nodes:
        if node[0] == 0 or node[0] == rows - 1 or node[1] == 0 or node[1] == cols -1:
            outside_nodes.append(node)
    end_node = random.choice(outside_nodes)
    return end_node

G = create_maze(6, 6, 0.6)
print(pick_end_node(G, 6, 6))
draw_maze(G)

# arbe courante de poid minimal
# labyeinthe parfait