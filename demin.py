import pygame
import random

GRID_SIZE = 20
# nombre de bombes
BOMB_RATIO = 0.2
NUM_BOMBS = int(GRID_SIZE ** 2 * 0.2)
# taille de chaque cellule en pixels
CELL_SIZE = 40
# épaisseur de la bordure en pixels
BORDER_WIDTH = 2
# couleur de fond pour les cellules révélées et non révélées
REVEALED_COLOR = (200, 200, 200)
UNREVEALED_COLOR = (50, 50, 50)
# couleur du texte
TEXT_COLOR = (255, 255, 255)  # Blanc
# couleur de la bordure
BORDER_COLOR = (255, 255, 255)
# couleur des cellules selon le nombre de bombes adjacentes
COLORS = [
    (200, 200, 200),  # Gris clair pour 0 bombes adjacentes
    (0, 191, 255),  # Bleu profond ciel pour 1 bombe adjacente
    (34, 139, 34),  # Vert forêt pour 2 bombes adjacentes
    (255, 0, 0),  # Rouge pour 3 bombes adjacentes
    (0, 0, 128),  # Bleu marine pour 4 bombes adjacentes
    (128, 0, 0),  # Bordeaux pour 5 bombes adjacentes
    (128, 0, 128),  # Violet pour 6 bombes adjacentes
    (0, 0, 0),  # Noir pour 7 bombes adjacentes
    (169, 169, 169)  # Gris foncé pour 8 bombes adjacentes
]


class Cell:
    def __init__(self, is_bomb, x, y):
        self.is_bomb = is_bomb
        self.revealed = False
        self.adjacent_bombs = 0
        self.x = x
        self.y = y

    def draw(self, surface):
        outer_rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, BORDER_COLOR, outer_rect)
        
        color = COLORS[self.adjacent_bombs] if self.revealed else UNREVEALED_COLOR
        inner_rect = pygame.Rect(self.x * CELL_SIZE + BORDER_WIDTH, self.y * CELL_SIZE + BORDER_WIDTH, CELL_SIZE - 2 * BORDER_WIDTH, CELL_SIZE - 2 * BORDER_WIDTH)
        pygame.draw.rect(surface, color, inner_rect)
        
        if self.revealed and not self.is_bomb and self.adjacent_bombs > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.adjacent_bombs), 1, TEXT_COLOR)
            text_rect = text.get_rect(center=inner_rect.center)
            surface.blit(text, text_rect)


class Board:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.num_bombs = int(grid_size * grid_size * 0.2)
        self.board = [[Cell(False, x, y) for y in range(grid_size)] for x in range(grid_size)]
        self.first_click = True
        

    def generate_board(self):
        board = [[Cell(False, x, y) for y in range(self.grid_size)] for x in range(self.grid_size)]
        return board

    def generate_bombs(self, exclude_x, exclude_y):
        available_positions = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if max(abs(x - exclude_x), abs(y - exclude_y)) > 1]
        bomb_positions = random.sample(available_positions, NUM_BOMBS)
        for x, y in bomb_positions:
            self.board[x][y].is_bomb = True
        self.calculate_adjacent_bombs()


    def calculate_adjacent_bombs(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j].is_bomb:
                    continue

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if 0 <= i + dx < self.grid_size and 0 <= j + dy < self.grid_size and self.board[i + dx][j + dy].is_bomb:
                            self.board[i][j].adjacent_bombs += 1
    def reveal(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False
        if self.board[x][y].revealed:
            return False

        # Générer les bombes après le premier clic
        if self.first_click:
            self.first_click = False
            self.generate_bombs(x, y)

        self.board[x][y].revealed = True

        if self.board[x][y].is_bomb:
            return False

        if self.board[x][y].adjacent_bombs == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.reveal(x + dx, y + dy)
        return True
    
   
    
    def draw(self, surface):
        for row in self.board:
            for cell in row:
                cell.draw(surface)
                
def play_game(grid_size):   
    pygame.init()
    screen = pygame.display.set_mode((grid_size * CELL_SIZE, grid_size * CELL_SIZE))
    pygame.display.set_caption("Démineur")
    running = True
    board = Board(grid_size)
    revealed_cells = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                safe = board.reveal(grid_x, grid_y)
                
                if not safe:
                    print("BOOM! Vous avez trouvé une bombe. Game Over.")
                    running = False

        screen.fill((255, 255, 255))
        board.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return revealed_cells, grid_size * grid_size - int(grid_size * grid_size * BOMB_RATIO)

if __name__ == "__main__":
    play_game(GRID_SIZE)



