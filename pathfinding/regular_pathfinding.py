import networkx as nx
import pygame

# Esse código define um jogo num mapa 2D com 500x500 pixels de largura

tile_size = (50, 50)  # Definindo o tamanho de um tile
map_size = (500, 500)

display = pygame.display.set_mode(map_size)
pygame.display.set_caption('Pathfinding')

def main():
    loop = True

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
    
        display.fill((245, 210, 113))

        # Desenhando as linhas verticais e horizontais do mapa
        for i in range(int(map_size[0]/tile_size[0])):
            pygame.draw.line(display, (0,0,0), (tile_size[0]*(i+1), 0), (tile_size[0]*(i+1), map_size[0]))
            pygame.draw.line(display, (0,0,0), (0, tile_size[1]*(i+1)), (map_size[1], tile_size[1]*(i+1)))


        pygame.display.flip()


if __name__ == '__main__':
    main()
