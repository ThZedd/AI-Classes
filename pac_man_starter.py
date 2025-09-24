import pygame
import random
from collections import deque
from queue import PriorityQueue
import math

# Inicializar pygame
pygame.init()

# Definir constantes
GRID_SIZE = 10
CELL_SIZE = 50
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
WALL_COLOR = (0, 0, 255)
PILL_COLOR = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 255)

# Definir posições iniciais [x, y]
pacman_position = [0, 0]
ghost_positions = [[8, 8], [8, 1]]
pill_positions = [[1, 3], [5, 5], [7,2]]
visited_positions = []


# Definir paredes (Exemplo: [(1,1), (2,3)] são posições com muros)
walls = [(3, 3), (4, 4), (6, 6), (7, 7), (2, 5), (5, 2)]

# Definir o ecrã
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption('Pac-Man Turn-Based')

# Definir o score inicial
score = 0

# Função para verificar se uma posição é válida
def is_valid_position(position):
    x, y = position
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and (x, y) not in walls

# Função para desenhar o Pac-Man
def draw_pacman(position):
    x, y = position
    center_x = y * CELL_SIZE + CELL_SIZE // 2
    center_y = x * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, PACMAN_COLOR, (center_x, center_y), CELL_SIZE // 2)
    pygame.draw.polygon(screen, BACKGROUND_COLOR, [(center_x, center_y), 
                                                   (center_x + CELL_SIZE // 2, center_y - CELL_SIZE // 4), 
                                                   (center_x + CELL_SIZE // 2, center_y + CELL_SIZE // 4)])

# Função para desenhar um fantasma
def draw_ghost(position):
    x, y = position
    center_x = y * CELL_SIZE + CELL_SIZE // 2
    center_y = x * CELL_SIZE + CELL_SIZE // 2
    # Desenhar corpo do fantasma
    pygame.draw.circle(screen, GHOST_COLOR, (center_x, center_y - CELL_SIZE // 6), CELL_SIZE // 2)
    pygame.draw.rect(screen, GHOST_COLOR, (center_x - CELL_SIZE // 2, center_y - CELL_SIZE // 6, CELL_SIZE, CELL_SIZE // 2))

# Função para desenhar o jogo
def draw_game():
    screen.fill(BACKGROUND_COLOR)
    
    # Desenhar paredes
    for wall in walls:
        x, y = wall
        pygame.draw.rect(screen, WALL_COLOR, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Desenhar Pac-Man
    draw_pacman(pacman_position)

    # Desenhar fantasmas
    for ghost in ghost_positions:
        draw_ghost(ghost)

    # Desenhar a pílula
    for pos in pill_positions:
        pygame.draw.circle(screen, PILL_COLOR, 
                        (pos[1] * CELL_SIZE + CELL_SIZE // 2, 
                         pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
    
    # Desenhar o layout do labirinto (linhas)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, (50, 50, 50), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Mostrar o score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()


# Função para mover Pac-Man
def move_pacman_reative():
    global score
    move = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
    if move == 'UP':
        new_position = [pacman_position[0] - 1, pacman_position[1]]
    elif move == 'DOWN':
        new_position = [pacman_position[0] + 1, pacman_position[1]]
    elif move == 'LEFT':
        new_position = [pacman_position[0], pacman_position[1] - 1]
    elif move == 'RIGHT':
        new_position = [pacman_position[0], pacman_position[1] + 1]

    return new_position

def move_pacman_towards_pill():
    global score
    # Se o comprimento da lista for 0 entao o PacMan move-se aleatoriamente
    if len(pill_positions) == 0 : 
        return move_pacman_reative()

    min_dist = float('inf') #Isto guarda a distancia da pilula mais proxima
    save_pill =[] #isto guarda a posicao da pilula mais proxima
    for pill in pill_positions:
        closest_pill = abs(pacman_position[0] - pill[0]) + abs(pacman_position[1] - pill[1]) #isto faz um simples calculo para verificar a distancia da pilula mais proxima
        if closest_pill < min_dist: # caso o valor da pilula mais proxima for menor que o da distancia da pilula mais proxima entao
            min_dist = closest_pill # a pilula mais proxima agora é essa pilula
            save_pill = pill # guarda a posicao dessa pilula
            if min_dist == 0: # caso a distancia a que a pilula se encontra for 0 entao verifica se o pacman comeu a pilula ou nao
                check_pos_pill(pill)
    if pacman_position[0] > save_pill[0]: # caso a posicao da linha for maior que a posicao da pilula mais proxima entao ele move-se para cima
        new_position =  [pacman_position[0] - 1, pacman_position[1]] # move "UP"
        if is_valid_position(new_position) and new_position not in visited_positions: # verifica se a nova posicao é valida, se for retorna a nova posicao, se nao move-se aleatoriamente 
            return new_position
        else:
            return move_pacman_reative()
        
    elif pacman_position[0] < save_pill[0]:  # caso a posicao da linha for menor que a posicao da pilula mais proxima entao ele move-se para baixo
        new_position = [pacman_position[0] + 1, pacman_position[1]] # move "DOWN"
        if is_valid_position(new_position) and new_position not in visited_positions: # verifica se a nova posicao é valida, se for retorna a nova posicao, se nao move-se aleatoriamente 
            return new_position
        else:
            return move_pacman_reative()
        
    elif pacman_position[1] > save_pill[1]:  # caso a posicao da coluna for maior que a posicao da pilula mais proxima entao ele move-se para a esquerda
        new_position = [pacman_position[0], pacman_position[1] - 1] # move "LEFT"
        if is_valid_position(new_position) and new_position not in visited_positions: # verifica se a nova posicao é valida, se for retorna a nova posicao, se nao move-se aleatoriamente 
            return new_position
        else:
            return move_pacman_reative()
        
    elif pacman_position[1] < save_pill[1]:  # caso a posicao da coluna for menor que a posicao da pilula mais proxima entao ele move-se para a direita
        new_position = [pacman_position[0], pacman_position[1] + 1] # move "RIGHT"
        if is_valid_position(new_position) and new_position not in visited_positions: # verifica se a nova posicao é valida, se for retorna a nova posicao, se nao move-se aleatoriamente 
            return new_position
        else:
            return move_pacman_reative()
        
    else:
        return move_pacman_reative() #caso nenhuma das condicoes acima funcione move-se aleatoriamente

    
             

# Função para mover Pac-Man
def move_pacman_models():
    global score
    new_position = move_pacman_towards_pill()

    if is_valid_position(new_position) and new_position not in ghost_positions and new_position not in visited_positions:
        pacman_position[:] = new_position
        visited_positions.append(new_position)
    
    
             
# Função para mover fantasmas aleatoriamente
def move_ghosts():
    for ghost in ghost_positions:
        move = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        if move == 'UP':
            new_position = [ghost[0] - 1, ghost[1]]
        elif move == 'DOWN':
            new_position = [ghost[0] + 1, ghost[1]]
        elif move == 'LEFT':
            new_position = [ghost[0], ghost[1] - 1]
        elif move == 'RIGHT':
            new_position = [ghost[0], ghost[1] + 1]

        # Verificar se a nova posição é válida
        if is_valid_position(new_position):
            ghost[:] = new_position

# Função para verificar se o Pac-Man se mover para a posicao pos come a pílula
def check_pos_pill(position):
    global score
    for pos in pill_positions:
        if position == pos:
            check_pill(position)
            print(f"score: {score}")
            pill_positions.remove(pos)
            return True
    return False


# Função para verificar se o Pac-Man comeu a pílula
def check_pill(position):
    global score
    for pos in pill_positions:
        if position == pos:
            score += 10  # Adicionar 10 pontos quando come a pílula
            return True
    return False

# Função para verificar se Pac-Man foi capturado por um fantasma
def check_ghosts():
    return pacman_position in ghost_positions

# Ciclo do jogo
def game_loop():
    global score
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
        # Verificar se Pac-Man comeu a pílula
       
        #move_pacman_reative()
        move_pacman_models()
        #move_pacman_towards_pill()
        print(f"Nova posição: {pacman_position}")
        print(f"Visitado: {visited_positions}")
        # Mover os fantasmas depois de Pac-Man
        move_ghosts()
        
        """if check_pill():
            print("Pac-Man ganhou!")
            print(f'Score final: {score}')    
        """
        # Verificar se Pac-Man foi capturado
        if check_ghosts():
            print("Pac-Man foi capturado pelos fantasmas!")
            print(f'Score final: {score}')
            running = False

        draw_game()
        clock.tick(5)  # Controla o frame rate do jogo (turn-based)

    pygame.quit()

# Iniciar o jogo
game_loop()
