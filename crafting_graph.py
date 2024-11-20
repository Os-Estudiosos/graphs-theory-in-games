import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle

# Criando o grafo
G = nx.DiGraph()

# Adicionando os vértices
nodes = [
    "Madeira", "Tábua", "Graveto", "Picareta de Pedra", "Pedra",
    "Fornalha", "Ferro Bruto", "Barra de Ferro", "Espada de Ferro"
]
G.add_nodes_from(nodes)

# Adicionando as conexões (arestas)
edges = [
    ("Madeira", "Tábua"),
    ("Tábua", "Graveto"),
    ("Graveto", "Picareta de Pedra"),
    ("Pedra", "Picareta de Pedra"),
    ("Pedra", "Fornalha"),
    ("Fornalha", "Barra de Ferro"),
    ("Ferro Bruto", "Barra de Ferro"),
    ("Barra de Ferro", "Espada de Ferro"),
    ("Picareta de Pedra", "Ferro Bruto"),
    ("Graveto", "Espada de Ferro")
]
G.add_edges_from(edges)

# Configurando as posições dos nós na mão
pos = {
    "Madeira": (0, 2),
    "Tábua": (1, 2),
    "Graveto": (2, 2),
    "Picareta de Pedra": (0, 1),
    "Pedra": (0, 0),
    "Fornalha": (1, 0),
    "Ferro Bruto": (1, 1),
    "Barra de Ferro": (2, 1),
    "Espada de Ferro": (4, 1)
}

# Ajustando as posições dos textos (rótulos dos nós) para cima - pois nos lugares padrão a seta estava aparecendo por cima
label_pos = {node: (x, y + 0.2) for node, (x, y) in pos.items()}

plt.figure(figsize=(12, 8))
ax = plt.gca()  # Pegando o eixo atual

# Borda
ax.add_patch(Rectangle((-0.5, -0.5), 5, 3, fill=None, edgecolor='black', lw=2))  # Ajuste da borda

nx.draw(
    G, pos, with_labels=False, node_color="lightblue",
    node_size=3000, font_size=10, font_weight="bold", arrowsize=20
)

# Adicionando os rótulos ajustados
nx.draw_networkx_labels(
    G, label_pos, font_size=10, font_weight="bold"
)

# Salvando o grafo como imagem
plt.savefig(os.path.join(os.getcwd(), 'output', "grafo_crafting.png"), bbox_inches='tight', dpi=300)

plt.show()