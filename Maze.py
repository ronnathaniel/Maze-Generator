import pygame as py
from pygame.key import get_pressed
from pygame import *
from random import choice
from Cell import Cell


class Maze:

    def pygame_setup(self):
        py.init()
        self.screen = py.display.set_mode((400, 400))
        py.display.set_caption("")

    def setup_board(self):
        self.board = []
        self.rows, self.cols = int(400/Cell.side), int(400/Cell.side)
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.cols):
                self.board[i].append(Cell(i, j))

        self.start_pos = self.board[0][0]
        self.start_stack = []

        self.end_pos = self.board[len(self.board)-1][len(self.board)-1]
        self.end_stack = []

        self.solved = []
        self.solved_vicinity = []
        self.solve = False
        self.cur = self.board[0][0]
        self.stop = self.board[len(self.board) - 1][len(self.board) - 1]

    def setup(self):
        self.pygame_setup()
        self.setup_board()

    def empty(self) -> bool:
        for arr in self.board:
            for cell in arr:
                if not cell.visited:
                    return False
        return True

    def get_vicinity(self, i, j) -> list:
        vicinity = []
        if j > 0 and not self.board[i][j].wall_up and self.board[i][j-1] not in self.solved:
            vicinity.append('up')
        if j < self.cols - 1 and not self.board[i][j].wall_down and self.board[i][j+1] not in self.solved:
            vicinity.append('down')
        if i < self.rows - 1 and not self.board[i][j].wall_right and self.board[i+1][j] not in self.solved:
            vicinity.append('right')
        if i > 0 and not self.board[i][j].wall_left and self.board[i-1][j] not in self.solved:
            vicinity.append('left')
        return vicinity

    def get_neighbors(self, i, j) -> list:
        neighbors = []
        if j > 0 and not self.board[i][j - 1].visited:
            neighbors.append('up')
        if j < self.cols - 1 and not self.board[i][j + 1].visited:
            neighbors.append('down')
        if i < self.rows - 1 and not self.board[i + 1][j].visited:
            neighbors.append('right')#self.board[i + 1][j])
        if i > 0 and not self.board[i - 1][j].visited:
            neighbors.append('left')#self.board[i - 1][j])
        return neighbors

    def next_walls(self, chosen, i, j) -> Cell:
        if chosen == 'up':
            self.board[i][j].wall_up = None
            self.board[i][j - 1].wall_down = None
            return self.board[i][j - 1]

        elif chosen == 'down':
            self.board[i][j].wall_down = None
            self.board[i][j + 1].wall_up = None
            return self.board[i][j + 1]

        elif chosen == 'right':
            self.board[i][j].wall_right = None
            self.board[i + 1][j].wall_left = None
            return self.board[i + 1][j]

        elif chosen == 'left':
            self.board[i][j].wall_left = None
            self.board[i - 1][j].wall_right = None
            return self.board[i - 1][j]

    def next_move(self, *, pos, stack):
        for i in range(self.rows):
            for j in range(self.rows):
                if self.board[i][j] == pos:
                    neighbors = self.get_neighbors(i, j)
                    if neighbors:
                        next = choice(neighbors)
                        return self.next_walls(next, i, j)
                    #up to here everything works


                    else:
                        if len(stack) > 1:
                            stack.pop()
                            return stack.pop()
                        else:
                            vicinity = self.get_vicinity(i, j)
                            next = choice(vicinity)
                            return self.next_walls(next, i, j)

    def move(self):
        self.start_pos.visited = 1
        self.end_pos.visited = 1
        self.start_stack.append(self.start_pos)
        self.end_stack.append(self.end_pos)
        self.start_pos = self.next_move(pos=self.start_pos, stack=self.start_stack)
        self.end_pos = self.next_move(pos=self.end_pos, stack=self.end_stack)

    def draw_background(self):
        surface = self.screen
        color = (0, 0, 0)
        rect = Rect(0, 0, 400, 400)
        py.draw.rect(surface, color, rect)

    def draw_lines(self, cell):
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
        py.draw.line(surface, color, cell.top_left, cell.bot_left)

    def draw_visited(self):
        for arr in self.board:
            for cell in arr:
                if cell.visited:
                    surface = self.screen
                    color = (138, 43, 226)
                    rect = (cell.x, cell.y, Cell.side, Cell.side)
                    py.draw.rect(surface, color, rect)

                    self.draw_lines(cell)

    def draw(self):
        py.display.flip()
        py.time.Clock().tick(30)
        self.draw_background()
        self.draw_visited()
        
    def main(self):
        while 1:
            for event in py.event.get():
                if event.type == py.QUIT:
                    break
            if get_pressed()[K_ESCAPE]:
                break
            if get_pressed()[K_SPACE]:
                self.setup()

            if not self.empty():
                self.move()
            self.draw()

    def __init__(self):
        self.setup()
        self.main()


if __name__ == '__main__':
    Maze()
