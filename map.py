import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Exemplo de Simulador de Mapas P roceurais")
clock = pygame.time.Clock()

# Configurações do grafo
NUM_VERTICES = random.randint(8,15)
MIN_EDGE_LENGTH = 150
MAX_FORCE = 0.01

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 170)
GRAY = (200, 200, 200)

class Vertex:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.vx = 0
        self.vy = 0
        self.radius = 20
        self.dragging = False

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.id), True, WHITE)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self):
        if not self.dragging:
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.9  # 
            self.vy *= 0.9

    def is_hovered(self, pos):
        px, py = pos
        return math.hypot(px - self.x, py - self.y) <= self.radius

# Classe da aresta
class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight

    def draw(self):
        pygame.draw.line(screen, GRAY, (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), 2)
        mid_x = (self.v1.x + self.v2.x) / 2
        mid_y = (self.v1.y + self.v2.y) / 2
        font = pygame.font.SysFont(None, 20)
        text = font.render(f"{self.weight:.1f}", True, RED)
        screen.blit(text, (mid_x, mid_y))

# Gerar grafo conexo
def generate_graph():
    vertices = [Vertex(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), i) for i in range(NUM_VERTICES)]
    edges = []
    connected = set()
    connected.add(vertices[0])

    # Garantir que o grafo é conexo
    while len(connected) < NUM_VERTICES:
        v1 = random.choice(list(connected))
        v2 = random.choice([v for v in vertices if v not in connected])
        weight = random.uniform(1, 10)
        edges.append(Edge(v1, v2, weight))
        connected.add(v2)

    # Adicionar arestas extras para variar o grau
    for _ in range(NUM_VERTICES // 2):
        v1, v2 = random.sample(vertices, 2)
        if not any(e for e in edges if (e.v1 == v1 and e.v2 == v2) or (e.v1 == v2 and e.v2 == v1)):
            weight = random.uniform(1, 10)
            edges.append(Edge(v1, v2, weight))

    return vertices, edges

# Simular forças
def apply_forces(vertices, edges):
    for edge in edges:
        dx = edge.v2.x - edge.v1.x
        dy = edge.v2.y - edge.v1.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            continue
        force = (distance - MIN_EDGE_LENGTH) * edge.weight * 0.01
        fx, fy = force * dx / distance, force * dy / distance
        edge.v1.apply_force(fx, fy)
        edge.v2.apply_force(-fx, -fy)

    for i, v1 in enumerate(vertices):
        for j, v2 in enumerate(vertices):
            if i != j:
                dx = v2.x - v1.x
                dy = v2.y - v1.y
                distance = math.hypot(dx, dy)
                if distance < MIN_EDGE_LENGTH and distance > 0:
                    repulsion = (MIN_EDGE_LENGTH - distance) * 0.05
                    fx, fy = repulsion * dx / distance, repulsion * dy / distance
                    v1.apply_force(-fx, -fy)
                    v2.apply_force(fx, fy)

# Função principal
def main():
    vertices, edges = generate_graph()
    dragging_vertex = None

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for vertex in vertices:
                    if vertex.is_hovered(event.pos):
                        dragging_vertex = vertex
                        vertex.dragging = True
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_vertex:
                    dragging_vertex.dragging = False
                dragging_vertex = None

        if dragging_vertex:
            dragging_vertex.x, dragging_vertex.y = pygame.mouse.get_pos()

        apply_forces(vertices, edges)

        for edge in edges:
            edge.draw()
        for vertex in vertices:
            vertex.update()
            vertex.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
