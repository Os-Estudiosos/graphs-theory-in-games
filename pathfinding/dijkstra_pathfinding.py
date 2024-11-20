import networkx as nx
import pygame

# Esse código define um jogo num mapa 2D com 500x500 pixels de largura

tile_size = (50, 50)  # Definindo o tamanho de um tile
# Medidas do Mapa mxn
m = 10
n = 10
map_size = (tile_size[0]*m, tile_size[1]*n)  # Definindo o tamanho do mapa

display = pygame.display.set_mode(map_size)  # Definindo a janela 500x500
pygame.display.set_caption('Pathfinding Dijkstra')  # Nome da janela

grafo_associado = nx.Graph()  # Defino o grafo associado, inicialmente vazio

colunas_grafo = map_size[0]//tile_size[0]  # Quantas colunas de tiles há
linhas_grafo = map_size[1]//tile_size[1]  # Quantas linhas de tiles há
vertices_grafo = [ [(j, i) for i in range(colunas_grafo)] for j in range(linhas_grafo) ]
# Matriz que representa os vértices na posição de cada tile associado a ele

vizinhanca = [  # Defino como vai ser a vizinhança de um tile
    (0, 1),  # Abaixo do tile  (No pygame e em computação no geral, a tela tem o eixo Y invertido)
    (0, -1),  # Em cima do tile
    (1, 0),  # Direita do tile
    (-1, 0),  # Esquerda do tile
    (1, 1),  # Embaixo direita do tile
    (-1, -1),  # Acima esquerda do tile
    (1, -1),  # Direita acima do tile
    (-1, 1)  # Esquerda em baixo do tile
]

# Adicionando as arestas com os vizinhos
for i in range(m):
    for j in range(n):
        # Lista de deslocamentos dos vizinhos
        vizinhos = [
            (i + 1, j), (i - 1, j), 
            (i, j + 1), (i, j - 1), 
            (i + 1, j + 1), (i + 1, j - 1), 
            (i - 1, j + 1), (i - 1, j - 1)
        ]
        # Adicionando as arestas para os vizinhos válidos
        for vi, vj in vizinhos:
            if 0 <= vi < n and 0 <= vj < n:  # Verifica se está dentro da matriz
                grafo_associado.add_edge((i, j), (vi, vj))

# # Desenhar o grafo
# nx.draw(grafo_associado, with_labels=True, node_color='lightblue', node_size=700, font_size=10)

# # Mostrar o grafo
# plt.title("Grafo com Nós Alinhados em Forma de Matriz")
# plt.show()


class Player:
    """Classe genérica responsável pelo player"""
    def __init__(self):
        self.rect = pygame.Rect(0,0,30,30)
        self.active_node = [0,0]  # O node onde o player se encontra
    
    def update(self):
        # Movimentação do player
        keys = pygame.key.get_pressed()

        vector = pygame.math.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )

        if vector.length() != 0:
            vector.normalize()
        
        self.rect.x += 5*vector.x
        self.rect.y += 5*vector.y

        # Atualizando o nó atual
        self.active_node[0] = self.rect.y // tile_size[1]  # Atualizo o nó de linha
        self.active_node[1] = self.rect.x // tile_size[0]  # Atualizo o nó de coluna

        print(self.active_node)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,255), self.rect)


class Enemy:
    """Classe genérica responsável por um objeto que segue o player"""
    def __init__(self):
        self.rect = pygame.Rect(0,0,30,30)
        self.direction = pygame.math.Vector2()
    
    def update(self, player_pos):
        # Achando o tile onde o player se localiza
        player_pos
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)


player = Player()
enemy = Enemy()


def main():
    loop = True
    clock = pygame.time.Clock()

    while loop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
    
        display.fill((245, 210, 113))

        # Desenhando as linhas verticais e horizontais do mapa
        for i in range(int(map_size[0]/tile_size[0])):
            pygame.draw.line(display, (0,0,0), (tile_size[0]*(i+1), 0), (tile_size[0]*(i+1), map_size[0]))
            pygame.draw.line(display, (0,0,0), (0, tile_size[1]*(i+1)), (map_size[1], tile_size[1]*(i+1)))

        player.update()
        enemy.update(player.rect.center)

        player.draw(display)
        enemy.draw(display)

        pygame.display.flip()

if __name__ == '__main__':
    main()
