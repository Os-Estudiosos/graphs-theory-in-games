import networkx as nx

def find_most_difficult_items(graph):
    """
    Encontra os itens mais difíceis de serem craftados em um grafo de crafting (DAG),
    considerando o total de itens únicos necessários para produzi-los.
    """
    # Verifica se o grafo é um DAG
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("O grafo fornecido não é um DAG!")

    # Dicionário para armazenar o conjunto de dependências únicas de cada vértice
    total_dependencies = {node: set() for node in graph.nodes}

    # Função para contar predecessores únicos usando DFS
    def count_unique_predecessors(node):
        # Se já calculado return
        if total_dependencies[node]:
            return total_dependencies[node]

        # Procura todos os predecessores únicos
        dependencies = set()
        for predecessor in graph.predecessors(node):
            dependencies.add(predecessor)  # Adiciona o predecessor 
            dependencies.update(count_unique_predecessors(predecessor))  # Adiciona predecessores indiretos

        total_dependencies[node] = dependencies
        return dependencies

    # Calcular o total de predecessores únicos 
    for node in graph.nodes:
        count_unique_predecessors(node)

    # Determinar o número máximo de itens necessários
    max_dependencies = max(len(dependencies) for dependencies in total_dependencies.values())

    # Encontrar todos os itens com o maior número de dependências
    most_difficult_items = [node for node, dependencies in total_dependencies.items() if len(dependencies) == max_dependencies]

    return most_difficult_items, max_dependencies

if __name__ == "__main__":
    # Caso do crafting dado no exemplo no paper
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

    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Encontra os itens
    items, total = find_most_difficult_items(G)
    print(f"O(s) item que precisa(m) da maior quantidade de item(s) para ser craftado(s) é(são) {items} com um total de {total} itens necessários.")
