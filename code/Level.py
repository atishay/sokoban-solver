import os
import copy


class Matrix(list):
    """
    A Matrix represents a game state.
    It contains not only the grid information but also
    utility methods
    """
    size = None
    target_found = False
    _string = None
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

    def getTargets(self):
        """
        Gets the position of all the targets on screen
        """
        # Iterate all Rows
        boxes = []
        for i in range(0, len(self)):
            # Iterate all columns
            for k in range(0, len(self[i]) - 1):
                if self[i][k] == ".":
                    boxes.append([k, i])
        return boxes

    def isSuccess(self):
        """
        Checks if the current state is the end state of the game.
        """
        return len(self.getBoxes()) == 0

    def isFailure(self):
        return False

    def getPossibleActions(self):
        x = self.getPlayerPosition()[0]
        y = self.getPlayerPosition()[1]
        def update_valid(item, move, get_two_step):
            if item not in "*#$":
                return (move, 2)
            if item in "$*" and get_two_step() not in "*#$":
                # We really prefer pushing the blocks over just roaming around
                # We do not like moving blocks out of their respective targets
                return (move, 1) if item is '$' else (move, 10)
            return None
        moves = []
        action_cost = update_valid(self[y][x - 1], 'L', lambda: self[y][x - 2])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = update_valid(self[y][x + 1], 'R', lambda: self[y][x + 2])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = update_valid(self[y - 1][x], 'U', lambda: self[y - 2][x])
        if action_cost is not None:
            moves.append(action_cost)
        action_cost = update_valid(self[y + 1][x], 'D', lambda: self[y + 2][x])
        if action_cost is not None:
            moves.append(action_cost)
        return moves

    def successor(self, direction, performOnSelf=False):
        if performOnSelf:
            return self.successorInternal(self, direction)
        matrix = copy.deepcopy(self)
        self.successorInternal(matrix, direction)
        matrix._string = None
        return matrix

    def toString(self, clear=False):
        """
        Gives a string version of self that is cached with the assumption that
        the object has not been mutated. The value can be stale if clear is not true
        """
        if self._string is not None and clear is False:
            return self._string
        self._string = "\n".join(["".join(x) for x in self])
        return self._string

    def __hash__(self):
        return hash(self.toString())

    def __str__(self):
        return self.toString()

    def successorInternal(self, matrix, direction):
        x = matrix.getPlayerPosition()[0]
        y = matrix.getPlayerPosition()[1]

        # print boxes
        # print matrix.getBoxes()

        if direction == "L":
            # print "######### Moving Left #########"

            # if is_space
            if matrix[y][x - 1] == " ":
                # print "OK Space Found"
                matrix[y][x - 1] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y][x - 1] == "$":
                # print "Box Found"
                if matrix[y][x - 2] == " ":
                    matrix[y][x - 2] = "$"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "
                elif matrix[y][x - 2] == ".":
                    matrix[y][x - 2] = "*"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y][x - 1] == "*":
                # print "Box on target Found"
                if matrix[y][x - 2] == " ":
                    matrix[y][x - 2] = "$"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

                elif matrix[y][x - 2] == ".":
                    matrix[y][x - 2] = "*"
                    matrix[y][x - 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

            # if is_target
            elif matrix[y][x - 1] == ".":
                # print "Target Found"
                matrix[y][x - 1] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True

            # else
            else:
                pass
                #print "There is a wall here"

        elif direction == "R":
            # print "######### Moving Right #########"

            # if is_space
            if matrix[y][x + 1] == " ":
                # print "OK Space Found"
                matrix[y][x + 1] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y][x + 1] == "$":
                # print "Box Found"
                if matrix[y][x + 2] == " ":
                    matrix[y][x + 2] = "$"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y][x + 2] == ".":
                    matrix[y][x + 2] = "*"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y][x + 1] == "*":
                # print "Box on target Found"
                if matrix[y][x + 2] == " ":
                    matrix[y][x + 2] = "$"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

                elif matrix[y][x + 2] == ".":
                    matrix[y][x + 2] = "*"
                    matrix[y][x + 1] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

            # if is_target
            elif matrix[y][x + 1] == ".":
                # print "Target Found"
                matrix[y][x + 1] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True

            # else
            else:
                pass
                # print "There is a wall here"

        elif direction == "D":
            # print "######### Moving Down #########"

            # if is_space
            if matrix[y + 1][x] == " ":
                # print "OK Space Found"
                matrix[y + 1][x] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y + 1][x] == "$":
                # print "Box Found"
                if matrix[y + 2][x] == " ":
                    matrix[y + 2][x] = "$"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y + 2][x] == ".":
                    matrix[y + 2][x] = "*"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y + 1][x] == "*":
                # print "Box on target Found"
                if matrix[y + 2][x] == " ":
                    matrix[y + 2][x] = "$"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

                elif matrix[y + 2][x] == ".":
                    matrix[y + 2][x] = "*"
                    matrix[y + 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

            # if is_target
            elif matrix[y + 1][x] == ".":
                # print "Target Found"
                matrix[y + 1][x] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True

            # else
            else:
                pass
                # print "There is a wall here"

        elif direction == "U":
            # print "######### Moving Up #########"

            # if is_space
            if matrix[y - 1][x] == " ":
                # print "OK Space Found"
                matrix[y - 1][x] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                    matrix.target_found = False
                else:
                    matrix[y][x] = " "

            # if is_box
            elif matrix[y - 1][x] == "$":
                # print "Box Found"
                if matrix[y - 2][x] == " ":
                    matrix[y - 2][x] = "$"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

                elif matrix[y - 2][x] == ".":
                    matrix[y - 2][x] = "*"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                        matrix.target_found = False
                    else:
                        matrix[y][x] = " "

            # if is_box_on_target
            elif matrix[y - 1][x] == "*":
                # print "Box on target Found"
                if matrix[y - 2][x] == " ":
                    matrix[y - 2][x] = "$"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

                elif matrix[y - 2][x] == ".":
                    matrix[y - 2][x] = "*"
                    matrix[y - 1][x] = "@"
                    if matrix.target_found == True:
                        matrix[y][x] = "."
                    else:
                        matrix[y][x] = " "
                    matrix.target_found = True

            # if is_target
            elif matrix[y - 1][x] == ".":
                # print "Target Found"
                matrix[y - 1][x] = "@"
                if matrix.target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                matrix.target_found = True

            # else
            else:
                pass
                # print "There is a wall here"


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

    def undo(self):
        if len(self.matrix_history) > 0:
            lastMatrix = self.matrix_history.pop()
            self.matrix = lastMatrix
            return lastMatrix
        else:
            return self.matrix


