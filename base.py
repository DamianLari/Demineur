import pygame
import random

# taille de la grille
GRID_SIZE = 5
# nombre de bombes
NUM_BOMBS = 5
# taille de chaque cellule en pixels
CELL_SIZE = 40
# couleur de fond pour les cellules révélées et non révélées
REVEALED_COLOR = (200, 200, 200)
UNREVEALED_COLOR = (50, 50, 50)
# couleur du texte
TEXT_COLOR = (0, 0, 0)

class Cell:
    def __init__(self, is_bomb, x, y):
        self.is_bomb = is_bomb
        self.revealed = False
        self.adjacent_bombs = 0
        self.x = x
        self.y = y

    def draw(self, surface):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, REVEALED_COLOR if self.revealed else UNREVEALED_COLOR, rect)
        if self.revealed and not self.is_bomb:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.adjacent_bombs), 1, TEXT_COLOR)
            surface.blit(text, rect.move(CELL_SIZE // 2, CELL_SIZE // 2))

class Board:
    def __init__(self, grid_size, num_bombs):
        self.grid_size = grid_size
        self.num_bombs = num_bombs
        self.board = self.generate_board()
        self.calculate_adjacent_bombs()

    def generate_board(self):
        board = [[Cell(False, x, y) for y in range(self.grid_size)] for x in range(self.grid_size)]
        bombs = self.generate_bombs()

        for bomb in bombs:
            board[bomb[0]][bomb[1]].is_bomb = True

        return board

    def generate_bombs(self):
        bombs = []

        while len(bombs) < self.num_bombs:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)

            if (x, y) not in bombs:
                bombs.append((x, y))

        return bombs

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
        self.board[x][y].revealed = True
        return not self.board[x][y].is_bomb
    
    def draw(self, surface):
        for row in self.board:
            for cell in row:
                cell.draw(surface)
                
def play_game():
    pygame.init()
    size = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Démineur")

    board = Board(GRID_SIZE, NUM_BOMBS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if not board.reveal(grid_x, grid_y):
                    print("BOOM! Vous avez trouvé une bombe. Game Over.")
                    running = False

        screen.fill((255, 255, 255))
        board.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    play_game()
