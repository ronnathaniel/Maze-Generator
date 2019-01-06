class Cell:
    side = 21

    def __init__(self, x, y):
        self.x = x * self.side
        self.y = y * self.side
        self.visited = None

        self.top_left = (self.x, self.y)
        self.top_right = (self.x + self.side, self.y)
        self.bot_right = (self.x + self.side, self.y + self.side)
        self.bot_left = (self.x, self.y + self.side)

        self.wall_up = 1
        self.wall_down = 1
        self.wall_right = 1
        self.wall_left = 1
        

if __name__ == "__main__":
    print("Missing File")
