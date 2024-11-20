import networkx as nx
import pygame

# Esse código define um jogo num mapa 2D com 500x500 pixels de largura

tile_size = (50, 50)  # Definindo o tamanho de um tile
map_size = (500, 500)

display = pygame.display.set_mode(map_size)
pygame.display.set_caption('Pathfinding')


class Player:
    def __init__(self):
        self.rect = pygame.Rect(0,0,30,30)
    
    def update(self):
        keys = pygame.key.get_pressed()

        vector = pygame.math.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )

        if vector.length() != 0:
            vector.normalize()
        
        self.rect.x += 5*vector.x
        self.rect.y += 5*vector.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,255), self.rect)


player = Player()


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

        player.draw(display)

        pygame.display.flip()

if __name__ == '__main__':
    main()
