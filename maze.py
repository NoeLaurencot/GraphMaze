import networkx as nx
import random

# Lookup table pour la position des colonnes
LETTERS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + [a + b for a in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for b in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

def arbre_couvrant(G):
    """
    Construit l'arbre couvrant minimal d'un graphe avec l'algorithme de Kruskal.

    On trie les arêtes par poids croissant, puis on les ajoute une par une
    en vérifiant qu'elles ne créent pas de cycle (avec Union-Find).

    :param G: Le graphe d'entrée avec des arêtes pondérées.
    :type G: nx.Graph
    :return: L'arbre couvrant minimal du graphe.
    :rtype: nx.Graph
    """
    def get_weight(edge):        
        return edge[2]['weight']
    
    def find(n):
        while parent[n] != n:
            parent[n] = parent[parent[n]]
            n = parent[n]
        return n

    def union(a, b):
        parent[find(a)] = find(b)

    mst = nx.Graph()
    mst.add_nodes_from(G.nodes())

    edges = sorted(G.edges(data=True), key=get_weight)
    
    parent = {}
    for node in G.nodes():
        parent[node] = node

    for u, v, data in edges:
        if find(u) != find(v):
            mst.add_edge(u, v, **data)
            union(u, v)

    return mst
    

def create_maze(rows, cols, n_cycles):
    """
    Génère un labyrinthe sous forme de graphe.

    On crée d'abord une grille complète avec des poids aléatoires,
    puis on calcule l'arbre couvrant minimal pour obtenir un labyrinthe
    sans cycles. Enfin, on rajoute quelques arêtes pour créer des cycles
    et rendre le labyrinthe plus intéressant.

    :param rows: Le nombre de lignes du labyrinthe.
    :type rows: int
    :param cols: Le nombre de colonnes du labyrinthe.
    :type cols: int
    :param n_cycles: Le nombre de cycles à ajouter dans le labyrinthe.
    :type n_cycles: int
    :return: Le graphe représentant le labyrinthe.
    :rtype: nx.Graph
    """
    G = nx.Graph()
    for row in range(rows):
        for col in range(cols):
            G.add_node((row, col))
            if row > 0:
                G.add_edge((row, col), (row - 1, col), weight=random.randint(1, 100))
            if col > 0:
                G.add_edge((row, col), (row, col - 1), weight=random.randint(1, 100))
    edges = G.edges()
    G_mst = arbre_couvrant(G)
    discarded_edges = []

    for edge in edges:
        if not G_mst.has_edge(edge[0], edge[1]):
            discarded_edges.append(edge)

    edges_to_restore = random.sample(discarded_edges, min(n_cycles, len(discarded_edges)))

    for edge in edges_to_restore:
        G_mst.add_edge(*edge)

    return G_mst

def draw_maze_terminal(G, rows, cols, path=None, start=None, end=None, point_list=None):
    """
    Affiche le labyrinthe dans le terminal avec des couleurs.

    Le point de départ est affiché en vert (SS), l'arrivée en rouge (EE),
    les points intermédiaires en bleu (OO) et le chemin en orange (XX).

    :param G: Le graphe représentant le labyrinthe.
    :type G: nx.Graph
    :param rows: Le nombre de lignes du labyrinthe.
    :type rows: int
    :param cols: Le nombre de colonnes du labyrinthe.
    :type cols: int
    :param path: La liste des noeuds formant le chemin à afficher, optionnel.
    :type path: list, optional
    :param start: Le noeud de départ, optionnel.
    :type start: tuple, optional
    :param end: Le noeud d'arrivée, optionnel.
    :type end: tuple, optional
    :param point_list: La liste des points intermédiaires à afficher, optionnel.
    :type point_list: list, optional
    """

    path_set = set(path) if path else set()

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    ORANGE  = "\033[93m"
    BLUE    = "\033[94m"
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
            elif point_list is not None and node in point_list:
                cell_row += f" {BLUE}OO{RESET} "
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
    """
    Convertit une entrée utilisateur comme "A1" en coordonnées (ligne, colonne).

    La partie alphabétique correspond à la colonne, la partie numérique
    correspond à la ligne. Par exemple, "B3" devient (2, 1).

    :param tmp: La chaîne de caractères entrée par l'utilisateur (ex: "A1").
    :type tmp: str
    :return: Les coordonnées du noeud sous forme (ligne, colonne).
    :rtype: tuple
    """
    i = 0
    col_part = ""
    while i < len(tmp) and tmp[i].isalpha():
        col_part += tmp[i]
        i += 1

    col = LETTERS.index(col_part.upper())

    row = int(tmp[i:].strip()) - 1
    return (row, col)

def bfs(G, start, end):
    """
    Trouve le chemin le plus court entre deux noeuds avec un parcours en largeur (BFS).

    On explore les noeuds voisins niveau par niveau jusqu'à atteindre
    le noeud d'arrivée. Ça garantit que le chemin trouvé est le plus court.

    :param G: Le graphe dans lequel on cherche le chemin.
    :type G: nx.Graph
    :param start: Le noeud de départ.
    :type start: tuple
    :param end: Le noeud d'arrivée.
    :type end: tuple
    :return: La liste des noeuds formant le chemin le plus court, ou None si aucun chemin n'existe.
    :rtype: list or None
    """
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

def main():
    """
    Initialise intéractivement le labyrinthe et les points par lesquels passer
    puis affiche le chemin
    """
    row_size = 0
    col_size = 0
    point_list = []
    devi_point_list = []
    path = []

    while row_size < 1:
        row_size = int(input("Entrez nombre de lignes : "))

    while col_size < 1 or col_size > 701:
        col_size = int(input("Entrez nombre de colonnes : "))

    n_cycle = int(input("Entrez le nombre de cycles : "))

    G = create_maze(row_size, col_size, n_cycle)
    draw_maze_terminal(G, row_size, col_size)

    tmp = input("Voulez-vous passer par plusieurs points? (y/n) ")

    hasMultiplePoints = False
    if tmp == "y":
        hasMultiplePoints = True
        nPoints = int(input("Entrez le nombre de points par lesquels passer : ").strip())

    tmp = input("Entrez le point de départ (ex: A1) : ").strip()
    start = parse_input(tmp)
    point_list.append(start)

    if hasMultiplePoints:
        for i in range(nPoints):
            tmp = input("Entrez le point par lequel passer (ex: B2) : ").strip()
            point_list.append(parse_input(tmp))
            devi_point_list.append(parse_input(tmp))

    tmp = input("Entrez le point d'arrivée (ex: C3) : ").strip()
    end = parse_input(tmp)
    point_list.append(end)

    if hasMultiplePoints:
        for i in range(len(point_list) - 1):
            path += bfs(G, point_list[i], point_list[i + 1])
        draw_maze_terminal(G, row_size, col_size, path, start, end, devi_point_list)
    else:
        path = bfs(G, start, end)
        draw_maze_terminal(G, row_size, col_size, path, start, end)

    print(f"Chemin trouvé en {len(path) - 1} étapes")

if __name__ == "__main__": main()