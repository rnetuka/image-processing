class Matrix:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def edge_values(self):
        lowest = float('inf')
        highest = float('-inf')

        for x, y in self:
            if self[x][y] < lowest:
                lowest = self[x][y]

            if self[x][y] > highest:
                highest = self[x][y]

        return lowest, highest

    def __iter__(self):
        return MatrixIterator(self)

    def __getitem__(self, x):
        return None


class MatrixIterator:

    def __init__(self, matrix):
        self.max_x = matrix.width - 1
        self.max_y = matrix.height - 1
        self.x = 0
        self.y = 0

    def __next__(self):
        x = self.x
        y = self.y

        if y > self.max_y:
            raise StopIteration

        if x >= self.max_x:
            self.x = 0
            self.y += 1
        else:
            self.x += 1

        return x, y
