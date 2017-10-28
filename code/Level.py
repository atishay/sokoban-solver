import os
import copy


class Matrix(list):
    """
    A Matrix represents a game state.
    It contains not only the grid information but also
    utility methods
    """
    size = None
    def getSize(self):
        """
        Gets the size of the matrix (The maximum width/height)
        """
        return self.size

    def getPlayerPosition(self):
        """
        Gets the position of the player in the current state
        """
        # Iterate all Rows
        for i in range(0, len(self)):
            # Iterate all columns
            for k in range(0, len(self[i]) - 1):
                if self[i][k] == "@":
                    return [k, i]

    def getBoxes(self):
        """
        Gets the position of all the boxes on screen
        """
        # Iterate all Rows
        boxes = []
        for i in range(0, len(self)):
            # Iterate all columns
            for k in range(0, len(self[i]) - 1):
                if self[i][k] == "$":
                    boxes.append([k, i])
        return boxes

    def isEnd(self):
        """
        Checks if the current state is the end state of the game.
        """
        return len(self.getBoxes()) == 0


class Level:
    matrix = Matrix()
    matrix_history = []

    def __init__(self,set,level_num):

        del self.matrix[:]
        del self.matrix_history[:]

        # Create level
        with open(os.path.dirname(os.path.abspath(__file__)) + '/levels/' + set + '/level' + str(level_num), 'r') as f:
                for row in f.read().splitlines():
                    self.matrix.append(list(row))

        max_row_length = 0
        # Iterate all Rows
        for i in range(0, len(self.matrix)):
            # Iterate all columns
            row_length = len(self.matrix[i])
            if row_length > max_row_length:
                max_row_length = row_length
        self.matrix.size = [max_row_length, len(self.matrix)]
        self.matrix.width = max_row_length
        self.matrix.height = len(self.matrix)

    def __del__(self):
        "Destructor to make sure object shuts down, etc."

    def getMatrix(self):
        return self.matrix

    def addToHistory(self,matrix):
        self.matrix_history.append(copy.deepcopy(matrix))

    def getLastMatrix(self):
        if len(self.matrix_history) > 0:
            lastMatrix = self.matrix_history.pop()
            self.matrix = lastMatrix
            return lastMatrix
        else:
            return self.matrix


