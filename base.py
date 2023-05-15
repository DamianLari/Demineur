import random

class Cell:
    def __init__(self, is_bomb):
        self.is_bomb = is_bomb
        self.revealed = False
        self.adjacent_bombs = 0

    def __str__(self):
        if not self.revealed:
            return "*"
        elif self.is_bomb:
            return "B"
        else:
            return str(self.adjacent_bombs)

class Board:
    def __init__(self, size, num_bombs):
        self.size = size
        self.num_bombs = num_bombs
        self.board = self.generate_board()
        self.calculate_adjacent_bombs()

    def generate_board(self):
        board = [[Cell(False) for _ in range(self.size)] for _ in range(self.size)]
        bombs = self.generate_bombs()

        for bomb in bombs:
            board[bomb[0]][bomb[1]].is_bomb = True

        return board

    def generate_bombs(self):
        bombs = []

        while len(bombs) < self.num_bombs:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)

            if (x, y) not in bombs:
                bombs.append((x, y))

        return bombs

    def calculate_adjacent_bombs(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].is_bomb:
                    continue

                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        if 0 <= i + dx < self.size and 0 <= j + dy < self.size and self.board[i + dx][j + dy].is_bomb:
                            self.board[i][j].adjacent_bombs += 1

    def reveal(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if self.board[x][y].revealed:
            return False
        self.board[x][y].revealed = True
        return not self.board[x][y].is_bomb

    def __str__(self):
        board_str = ""
        for row in self.board:
            for cell in row:
                board_str += str(cell) + " "
            board_str += "\n"
        return board_str

def play_game():
    board = Board(5, 5)
    while True:
        print(board)
        x = int(input("Entrez l'index de ligne (commençant par 0): "))
        y = int(input("Entrez l'index de colonne (commençant par 0): "))

        if not board.reveal(x, y):
            print("BOOM! Vous avez trouvé une bombe. Game Over.")
            break

if __name__ == "__main__":
    play_game()
