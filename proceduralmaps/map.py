import pygame
import random
import math
import string
from collections import deque

# Inicializar pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Exemplo de Simulador de Mapas Procedurais")
clock = pygame.time.Clock()
# Configurações do grafo
NUM_VERTICES = random.randint(10, 12)
MIN_EDGE_LENGTH = 150
MAX_FORCE = 0.01
MIN_PATH_DISTANCE = 25  # Distância mínima em peso de arestas entre início e fim

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
START_COLOR = BLUE
END_COLOR = RED

class Vertex:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.vx = 0
        self.vy = 0
        self.radius = 25
        self.dragging = False
        self.is_start = False
        self.is_end = False

    def draw(self):
        color = START_COLOR if self.is_start else END_COLOR if self.is_end else YELLOW
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        font = pygame.font.SysFont(None, 28)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (self.x - text.get_width() // 2, self.y - text.get_height() // 2))

    def apply_force(self, fx, fy):
        self.vx += fx
        self.vy += fy

    def update(self):
        if not self.dragging:
            self.x += self.vx
            self.y += self.vy
            self.vx *= 0.9
            self.vy *= 0.9

    def is_hovered(self, pos):
        px, py = pos
        return math.hypot(px - self.x, py - self.y) <= self.radius

class Edge:
    def __init__(self, v1, v2, weight):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight

    def draw(self):
        pygame.draw.line(screen, WHITE, (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), 4)
        mid_x = (self.v1.x + self.v2.x) / 2
        mid_y = (self.v1.y + self.v2.y) / 2
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"{self.weight:.1f}", True, WHITE)
        screen.blit(text, (mid_x - text.get_width() // 2, mid_y - text.get_height() // 2))

def generate_graph():
    # Gerar nomes únicos para os vértices usando letras do alfabeto
    names = [string.ascii_uppercase[i % 26] + (i // 26) * "'" for i in range(NUM_VERTICES)]
    vertices = [Vertex(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), name) for name in names]
    edges = []
    connected = set()
    connected.add(vertices[0])

    while len(connected) < NUM_VERTICES:
        v1 = random.choice(list(connected))
        v2 = random.choice([v for v in vertices if v not in connected])
        weight = random.uniform(1, 10)
        edges.append(Edge(v1, v2, weight))
        connected.add(v2)

    for _ in range(NUM_VERTICES // 2):
        v1, v2 = random.sample(vertices, 2)
        if not any(e for e in edges if (e.v1 == v1 and e.v2 == v2) or (e.v1 == v2 and e.v2 == v1)):
            weight = random.uniform(1, 10)
            edges.append(Edge(v1, v2, weight))

    return vertices, edges

def bfs_shortest_path(vertices, edges, start, end):
    graph = {v: [] for v in vertices}
    for edge in edges:
        graph[edge.v1].append((edge.v2, edge.weight))
        graph[edge.v2].append((edge.v1, edge.weight))

    queue = deque([(start, 0)])
    visited = set()

    while queue:
        current, distance = queue.popleft()
        if current == end:
            return distance
        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph[current]:
            if neighbor not in visited:
                queue.append((neighbor, distance + weight))

    return float('inf')

def assign_start_and_end(vertices, edges):
    while True:
        start = random.choice(vertices)
        end = random.choice([v for v in vertices if v != start])
        path_distance = bfs_shortest_path(vertices, edges, start, end)
        if path_distance >= MIN_PATH_DISTANCE:
            start.is_start = True
            end.is_end = True
            break

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

def main():
    vertices, edges = generate_graph()
    assign_start_and_end(vertices, edges)
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

def draw_button(x, y, w, h, text, color, text_color, font_size=30):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (x + (w - text_surface.get_width()) // 2, y + (h - text_surface.get_height()) // 2))

def dijkstra(vertices, edges, start, end):
    distances = {v: float('inf') for v in vertices}
    distances[start] = 0
    previous = {v: None for v in vertices}
    unvisited = set(vertices)

    while unvisited:
        current = min(unvisited, key=lambda v: distances[v])
        unvisited.remove(current)

        if current == end or distances[current] == float('inf'):
            break

        for edge in edges:
            neighbor = None
            if edge.v1 == current:
                neighbor = edge.v2
            elif edge.v2 == current:
                neighbor = edge.v1
            if neighbor in unvisited:
                new_distance = distances[current] + edge.weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current

    path = []
    current = end
    while current:
        prev = previous[current]
        if prev:
            path.append((prev, current))
        current = prev

    return path[::-1]

def main():
    vertices, edges = generate_graph()
    assign_start_and_end(vertices, edges)
    dragging_vertex = None
    shortest_path_edges = []

    button_x, button_y, button_w, button_h = 20, 20, 200, 50

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_x <= event.pos[0] <= button_x + button_w and button_y <= event.pos[1] <= button_y + button_h:
                    start_vertex = next(v for v in vertices if v.is_start)
                    end_vertex = next(v for v in vertices if v.is_end)
                    shortest_path = dijkstra(vertices, edges, start_vertex, end_vertex)
                    shortest_path_edges = shortest_path

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
            if (edge.v1, edge.v2) in shortest_path_edges or (edge.v2, edge.v1) in shortest_path_edges:
                pygame.draw.line(screen, (0, 255, 0), (edge.v1.x, edge.v1.y), (edge.v2.x, edge.v2.y), 6)
            else:
                edge.draw()
        for vertex in vertices:
            vertex.update()
            vertex.draw()

        draw_button(button_x, button_y, button_w, button_h, "Calcular Caminho", GRAY, BLACK)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
