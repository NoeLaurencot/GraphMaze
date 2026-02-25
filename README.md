# GraphMaze

## Projet théorie des graphes

Ce projet a été réalisé dans le cadre du BUT Informatique, semestre 2. Il met en pratique plusieurs notions de la théorie des graphes.

### Notions de théorie des graphes utilisées
- **Graphe non orienté** : représentation du labyrinthe sous forme de graphe où chaque case est un sommet et chaque passage une arête.
- **Arbre couvrant minimal** : génération du labyrinthe à l'aide d'un arbre couvrant minimal pour garantir que le labyrinthe ne sois pas coupé.
- **Parcours en largeur (BFS)** : recherche du chemin le plus court entre l'entrée et la sortie du labyrinthe.

### Dépendances
- Python 3
- networkx

Créer et activer un venv python :

**Linux / macOS**
```bash
python -m venv .venv && source .venv/bin/activate
```

**Windows**
```bat
python -m venv .venv
.venv\Scripts\activate
```

Installer les dépendences:

```bash
pip install -r requirements.txt
```

### Utilisation
Le script `maze.py` permet de :
- Générer un labyrinthe
- Ajouter un nombre défini de cycles
- Trouver et afficher le chemin le plus court entre deux noeuds

Pour l'éxecuter:
```bash
python maze.py
```