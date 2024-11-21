import networkx as nx
import pygame


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

# Lista que descreve onde as paredes ficam
wall_map = [
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 3, 0, 2, 2, 0, 1],
    [1, 0, 0, 2, 3, 2, 0, 2, 0, 1],
    [1, 2, 0, 2, 3, 0, 0, 3, 0, 1],
    [1, 2, 0, 0, 3, 0, 0, 3, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 3, 0, 1],
    [1, 2, 0, 2, 3, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Player:
    """Classe genérica responsável pelo player"""
    def __init__(self):
        self.rect = pygame.Rect(0,0,30,30)  # Retângulo que representa o player
        self.active_node = (0,0)  # O node onde o player se encontra
        self.direction = pygame.math.Vector2(0,0)  # Direção onde ele está indo
        self.speed = 5
        self.actual_speed = 5
    
    def update(self, walls_list, tiles_list):
        # Movimentação do player
        keys = pygame.key.get_pressed()

        self.direction = pygame.math.Vector2(  # Atualizando o vetor da direção
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )

        if self.direction.length() != 0:  # Normalizando
            self.direction.normalize()
        
        for tile in tiles_list:
            if self.rect.colliderect(tile):
                break
        else:
            self.actual_speed = self.speed
        
        self.rect.x += self.actual_speed*self.direction.x  # Atualizando o X

        for wall in walls_list:  # Fazendo a colisão lateral
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right

        self.rect.y += self.actual_speed*self.direction.y  # Atualizando o Y

        for wall in walls_list:  # Fazendo a colisão vertical
            if self.rect.colliderect(wall.rect):
                if self.direction.y > 0:
                    self.rect.bottom = wall.rect.top
                else:
                    self.rect.top = wall.rect.bottom
        
        self.active_node = (
            self.rect.centery // tile_size[1],  # Atualizo o nó de linha
            self.rect.centerx // tile_size[0]  # Atualizo o nó de coluna
        )
    
    def draw(self, screen):
        """Desenhando o player na tela"""
        pygame.draw.rect(screen, (0,0,255), self.rect)


class Enemy:
    """Classe genérica responsável por um objeto que segue o player"""
    def __init__(self):
        self.rect = pygame.Rect(0,0,30,30)  # Retângulo do Inimigo
        self.actual_node = [0,0]  # Vértice onde o player se encontra
        self.least_way = []  # O menor caminho até o player
        self.speed = 3
        self.actual_speed = 3

    def update(self, player_node: list[int], tiles_list):
        # Pego uma lista em ordem dos nós que o inimigo deve seguir para ir ao player
        self.least_way = nx.dijkstra_path(grafo_associado, tuple(self.actual_node), player_node)

        # Faço ele seguir em direção ao nó mais próximo
        direction = pygame.math.Vector2(0,0)

        if len(self.least_way) > 1:
            direction.x = self.least_way[1][1] - self.actual_node[1]
            direction.y = self.least_way[1][0] - self.actual_node[0]
        
        if direction.length() != 0:
            direction.normalize()

        for tile in tiles_list:
            if self.rect.colliderect(tile):
                break
        else:
            self.actual_speed = self.speed

        self.rect.x += direction.x*self.actual_speed

        for wall in walls_list:
            if self.rect.colliderect(wall.rect):
                if direction.x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right

        self.rect.y += self.actual_speed*direction.y

        for wall in walls_list:
            if self.rect.colliderect(wall.rect):
                if direction.y > 0:
                    self.rect.bottom = wall.rect.top
                else:
                    self.rect.top = wall.rect.bottom

        # Atualizando o nó atual do inimigo
        if direction.x > 0:
            self.actual_node[1] = self.rect.left // tile_size[0]  # Atualizo o nó de coluna        
        elif direction.x < 0:
            self.actual_node[1] = self.rect.right // tile_size[0]  # Atualizo o nó de coluna
        
        if direction.y > 0:
            self.actual_node[0] = self.rect.top // tile_size[1]  # Atualizo o nó de linha
        elif direction.y < 0:
            self.actual_node[0] = self.rect.bottom // tile_size[1]  # Atualizo o nó de linha
 
    def draw(self, screen):
        for i in range(len(self.least_way)-1):
            pygame.draw.line(screen, (0,0,0),
                (
                    self.least_way[i][1]*tile_size[0] + (tile_size[0]//2),
                    self.least_way[i][0]*tile_size[1] + (tile_size[1]//2)
                ),
                (
                    self.least_way[i+1][1]*tile_size[0] + (tile_size[0]//2),
                    self.least_way[i+1][0]*tile_size[1] + (tile_size[1]//2)
                )
            )
        pygame.draw.rect(screen, (255,0,0), self.rect)


class Wall:
    def __init__(self, pos_node = (0, 0)):
        self.rect = pygame.Rect(0,0,tile_size[0],tile_size[1])
        self.rect.x = pos_node[0]*tile_size[1]
        self.rect.y = pos_node[1]*tile_size[0]
    
    def draw(self, screen):
        pygame.draw.rect(screen, (40,40,40), self.rect)


class Water:
    def __init__(self, pos_node = (0, 0)):
        self.rect = pygame.Rect(0,0,tile_size[0],tile_size[1])
        self.rect.x = pos_node[0]*tile_size[1]
        self.rect.y = pos_node[1]*tile_size[0]
    
    def update(self, player, enemy):
        if self.rect.colliderect(player.rect):
            player.actual_speed = player.speed // 2
        
        if self.rect.colliderect(enemy.rect):
            enemy.actual_speed = enemy.speed // 2
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 212, 201), self.rect)


class Mud:
    def __init__(self, pos_node = (0, 0)):
        self.rect = pygame.Rect(0,0,tile_size[0],tile_size[1])
        self.rect.x = pos_node[0]*tile_size[1]
        self.rect.y = pos_node[1]*tile_size[0]
    
    def update(self, player, enemy):
        if self.rect.colliderect(player.rect):
            player.actual_speed = player.speed // 3
        
        if self.rect.colliderect(enemy.rect):
            enemy.actual_speed = enemy.speed // 3
    
    def draw(self, screen):
        pygame.draw.rect(screen, (94, 70, 33), self.rect)


walls_list = [  # Lista com todas as instâncias de Wall
]
tiles_list = [  # Lista com os tiles diferentes (Terrenos)

]

# Adicionando as arestas com os vizinhos
for i in range(m):
    for j in range(n):
        peso_aresta = 1

        # Lista de deslocamentos dos vizinhos
        vizinhos = [
            (i + 1, j), (i - 1, j), 
            (i, j + 1), (i, j - 1),
        ]

        if wall_map[i][j] == 2:
            tiles_list.append(Water((j, i)))
            peso_aresta= 2
        
        if wall_map[i][j] == 3:
            tiles_list.append(Mud((j, i)))
            peso_aresta = 3

        # Adicionando as arestas para os vizinhos válidos
        for vi, vj in vizinhos:
            if 0 <= vi < n and 0 <= vj < n:  # Verifica se está dentro da matriz
                grafo_associado.add_edge((i, j), (vi, vj), weight=peso_aresta)

for i in range(linhas_grafo):  # Adicionando paredes e tiles
    for j in range(colunas_grafo):
        if wall_map[i][j] == 1:
            walls_list.append(Wall((j, i)))
            grafo_associado.remove_node((i, j))

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

        player.update(walls_list, tiles_list)
        for tile in tiles_list:
            tile.update(player, enemy)
        enemy.update(player.active_node, tiles_list)

        for tile in tiles_list:
            tile.draw(display)
        player.draw(display)
        for wall in walls_list:
            wall.draw(display)
        enemy.draw(display)

        # Desenhando as linhas verticais e horizontais do mapa
        for i in range(int(map_size[0]/tile_size[0])):
            pygame.draw.line(display, (0,0,0), (tile_size[0]*(i+1), 0), (tile_size[0]*(i+1), map_size[0]))
            pygame.draw.line(display, (0,0,0), (0, tile_size[1]*(i+1)), (map_size[1], tile_size[1]*(i+1)))

        pygame.display.flip()


if __name__ == '__main__':
    main()
