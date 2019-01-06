import pygame as py
from random import choice
from Cell import Cell


class Maze:
    # sets up pygame
    def setup_pygame(self):
        py.init()
        self.screen = py.display.set_mode((400, 400))
        py.display.set_caption("")

    # sets up the board
    def setup_maze(self):
        self.stack = []
        self.board = []
        self.rows, self.cols = int(400/Cell.side), int(400/Cell.side)
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(Cell(i, j))
        self.pos = self.board[0][0]

    # returns unvisited neighbors of given cell
    def get_neighbors(self, i, j) -> list:
        neighbors = []
        if j > 0 and not self.board[i][j - 1].visited:
            neighbors.append('up')
        if j < self.cols-1 and not self.board[i][j + 1].visited:
            neighbors.append('down')
        if i < self.rows-1 and not self.board[i + 1][j].visited:
            neighbors.append('right')
        if i > 0 and not self.board[i - 1][j].visited:
            neighbors.append('left')
        return neighbors

    # returns visited neighbors without walls in between of given cell
    def next_walls(self, next, i, j) -> Cell:
        if next == 'up':
            self.board[i][j].wall_up = None
            self.board[i][j - 1].wall_down = None
            return self.board[i][j - 1]

        elif next == 'down':
            self.board[i][j].wall_down = None
            self.board[i][j + 1].wall_up = None
            return self.board[i][j + 1]

        elif next == 'right':
            self.board[i][j].wall_right = None
            self.board[i + 1][j].wall_left = None
            return self.board[i + 1][j]

        elif next == 'left':
            self.board[i][j].wall_left = None
            self.board[i - 1][j].wall_right = None
            return self.board[i - 1][j]

    # returns next move
    def next_move(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == self.pos:
                    neighbors = self.get_neighbors(i, j)
                    if neighbors:
                        next = choice(neighbors)
                    else:
                        if len(self.stack) > 1:
                            self.stack.pop()
                            return self.stack.pop()
                        return

                    return self.next_walls(next, i, j)

    # execuutes the move
    def move(self):
        self.pos.visited = 1
        self.stack.append(self.pos)
        self.pos = self.next_move()

    # draws black background
    def draw_background(self):
        surface = self.screen
        color = (0, 0, 0)
        rect = py.Rect(0, 0, 400, 400)
        py.draw.rect(surface, color, rect)

    # draws walls in between cells
    def draw_walls(self, cell):
        surface = self.screen
        if cell.wall_up:
            color = (255, 255, 255)
        else:
            color = (138, 43, 226)
        py.draw.line(surface, color, cell.top_left, cell.top_right)
        if cell.wall_down:
            color = (255, 255, 255)
        else:
            color = (138, 43, 226)
        py.draw.line(surface, color, cell.bot_left, cell.bot_right)
        if cell.wall_right:
            color = (255, 255, 255)
        else:
            color = (138, 43, 226)
        py.draw.line(surface, color, cell.top_right, cell.bot_right)
        if cell.wall_left:
            color = (255, 255, 255)
        else:
            color = (138, 43, 226)
        py.draw.line(surface, color, cell.top_left, cell.bot_left, 2)

    # draws each visited cell as purple
    def draw_visited(self):
        for arr in self.board:
            for cell in arr:
                if cell.visited:
                    surface = self.screen
                    color = (138, 43, 226)
                    rect = py.Rect(cell.x, cell.y, Cell.side, Cell.side)
                    py.draw.rect(surface, color, rect)

                self.draw_walls(cell)

    # executes the draw
    def draw(self):
        py.display.flip()
        self.draw_background()
        self.draw_visited()

    # while loop
    def main(self):
        while 1:
            for event in py.event.get():
                if event.type == py.QUIT:
                    break
            if py.key.get_pressed()[py.K_LEFT]:
                break
            if py.key.get_pressed()[py.K_SPACE]:
                self.__init__()
                print(Cell.side)

            if self.pos:
                self.move()
            self.draw()

    # sets up pygame and board, runs the animation
    def __init__(self):
        self.setup_pygame()
        self.setup_maze()
        self.main()


if __name__ == "__main__":
    Maze()