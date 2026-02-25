import networkx as nx
import random

LETTERS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + [a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def create_maze(rows, cols, n_cycles):
    G = nx.Graph()
    for row in range(rows):
        for col in range(cols):
            G.add_node((row, col))
            if row > 0:
                G.add_edge((row, col), (row - 1, col), weight=random.randint(1, 100))
            if col > 0:
                G.add_edge((row, col), (row, col - 1), weight=random.randint(1, 100))
    edges = G.edges()
    G_mst = nx.minimum_spanning_tree(G)
    discarded_edges = []

    for edge in edges:
        if not G_mst.has_edge(edge[0], edge[1]):
            discarded_edges.append(edge)

    edges_to_restore = random.sample(discarded_edges, min(n_cycles, len(discarded_edges)))

    for edge in edges_to_restore:
        G_mst.add_edge(*edge)

    return G_mst

def draw_maze_terminal(G, rows, cols, path=None, start=None, end=None):
    path_set = set(path) if path else set()

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    ORANGE  = "\033[93m"
    RESET   = "\033[0m"

    header = "     "
    for col in range(cols):
        header += f"  {LETTERS[col]}  " if col <= 26 else f" {LETTERS[col]}  "
    print(header)

    for row in range(rows):
        top = "     "
        for col in range(cols):
            has_wall_above = (row == 0) or not G.has_edge((row, col), (row - 1, col))
            top += "+" + ("----" if has_wall_above else "    ")
        top += "+"
        print(top)

        cell_row = f" {row + 1:3} "
        for col in range(cols):
            has_wall_left = (col == 0) or not G.has_edge((row, col), (row, col - 1))
            cell_row += "|" if has_wall_left else " "

            node = (row, col)
            if node == start:
                cell_row += f" {GREEN}SS{RESET} "
            elif node == end:
                cell_row += f" {RED}EE{RESET} "
            elif node in path_set:
                cell_row += f" {ORANGE}XX{RESET} "
            else:
                cell_row += "    "
        cell_row += "|"
        print(cell_row)

    bottom = "     "
    for col in range(cols):
        bottom += "+----"
    bottom += "+"
    print(bottom)

def parse_input(tmp):
    i = 0
    col_part = ""
    while i < len(tmp) and tmp[i].isalpha():
        col_part += tmp[i]
        i += 1

    col = LETTERS.index(col_part.upper())

    row = int(tmp[i:].strip()) - 1
    return (row, col)

def bfs(G, start, end):
    queue = [(start, [start])]
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.pop(0)

        if current == end:
            return path

        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None

### Main ###
print(parse_input("a1"))

row_size = int(input("Entrez nombre de lignes : "))
col_size = int(input("Entrez nombre de colonnes : "))
n_cycle = int(input("Entrez le nombre de cycles : "))

G = create_maze(row_size, col_size, n_cycle)
draw_maze_terminal(G, row_size, col_size)

tmp = input("Entrez le point de départ (ex: A1) : ").strip()
start = parse_input(tmp)

tmp = input("Entrez le point d'arrivée (ex: C3) : ").strip()
end = parse_input(tmp)

path = bfs(G, start, end)

draw_maze_terminal(G, row_size, col_size, path, start, end)
print(f"Chemin trouvé en {len(path) - 1} étapes.")