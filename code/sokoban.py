# Name: pySokoban
# Description: A sokoban implementation using python & pyGame
# Author: Kazantzakis Nikos <kazantzakisnikos@gmail.com>
# Date: 2015
# Last Modified: 31-03-2016


# import time
import pygame
import sys
from gui import SokobanGui
from Level import Level

def movePlayer(direction,myLevel):

    matrix = myLevel.getMatrix()

    myLevel.addToHistory(matrix)

    x = matrix.getPlayerPosition()[0]
    y = matrix.getPlayerPosition()[1]

    global target_found

    #print boxes
    print  matrix.getBoxes()

    if direction == "L":
        print "######### Moving Left #########"

        # if is_space
        if matrix[y][x-1] == " ":
            print "OK Space Found"
            matrix[y][x-1] = "@"
            if target_found == True:
                matrix[y][x] = "."
                target_found = False
            else:
                matrix[y][x] = " "

        # if is_box
        elif matrix[y][x-1] == "$":
            print "Box Found"
            if matrix[y][x-2] == " ":
                matrix[y][x-2] = "$"
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "
            elif matrix[y][x-2] == ".":
                matrix[y][x-2] = "*"
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "


        # if is_box_on_target
        elif matrix[y][x-1] == "*":
            print "Box on target Found"
            if matrix[y][x-2] == " ":
                matrix[y][x-2] = "$"
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

            elif matrix[y][x-2] == ".":
                matrix[y][x-2] = "*"
                matrix[y][x-1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        # if is_target
        elif matrix[y][x-1] == ".":
            print "Target Found"
            matrix[y][x-1] = "@"
            if target_found == True:
                matrix[y][x] = "."
            else:
                matrix[y][x] = " "
            target_found = True

        # else
        else:
            print "There is a wall here"

    elif direction == "R":
        print "######### Moving Right #########"

        # if is_space
        if matrix[y][x+1] == " ":
            print "OK Space Found"
            matrix[y][x+1] = "@"
            if target_found == True:
                matrix[y][x] = "."
                target_found = False
            else:
                matrix[y][x] = " "

        # if is_box
        elif matrix[y][x+1] == "$":
            print "Box Found"
            if matrix[y][x+2] == " ":
                matrix[y][x+2] = "$"
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            elif matrix[y][x+2] == ".":
                matrix[y][x+2] = "*"
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

        # if is_box_on_target
        elif matrix[y][x+1] == "*":
            print "Box on target Found"
            if matrix[y][x+2] == " ":
                matrix[y][x+2] = "$"
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

            elif matrix[y][x+2] == ".":
                matrix[y][x+2] = "*"
                matrix[y][x+1] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        # if is_target
        elif matrix[y][x+1] == ".":
            print "Target Found"
            matrix[y][x+1] = "@"
            if target_found == True:
                matrix[y][x] = "."
            else:
                matrix[y][x] = " "
            target_found = True

        # else
        else:
            print "There is a wall here"

    elif direction == "D":
        print "######### Moving Down #########"

        # if is_space
        if matrix[y+1][x] == " ":
            print "OK Space Found"
            matrix[y+1][x] = "@"
            if target_found == True:
                matrix[y][x] = "."
                target_found = False
            else:
                matrix[y][x] = " "

        # if is_box
        elif matrix[y+1][x] == "$":
            print "Box Found"
            if matrix[y+2][x] == " ":
                matrix[y+2][x] = "$"
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            elif matrix[y+2][x] == ".":
                matrix[y+2][x] = "*"
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

        # if is_box_on_target
        elif matrix[y+1][x] == "*":
            print "Box on target Found"
            if matrix[y+2][x] == " ":
                matrix[y+2][x] = "$"
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

            elif matrix[y+2][x] == ".":
                matrix[y+2][x] = "*"
                matrix[y+1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        # if is_target
        elif matrix[y+1][x] == ".":
            print "Target Found"
            matrix[y+1][x] = "@"
            if target_found == True:
                matrix[y][x] = "."
            else:
                matrix[y][x] = " "
            target_found = True

        # else
        else:
            print "There is a wall here"

    elif direction == "U":
        print "######### Moving Up #########"

        # if is_space
        if matrix[y-1][x] == " ":
            print "OK Space Found"
            matrix[y-1][x] = "@"
            if target_found == True:
                matrix[y][x] = "."
                target_found = False
            else:
                matrix[y][x] = " "

        # if is_box
        elif matrix[y-1][x] == "$":
            print "Box Found"
            if matrix[y-2][x] == " ":
                matrix[y-2][x] = "$"
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

            elif matrix[y-2][x] == ".":
                matrix[y-2][x] = "*"
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                    target_found = False
                else:
                    matrix[y][x] = " "

        # if is_box_on_target
        elif matrix[y-1][x] == "*":
            print "Box on target Found"
            if matrix[y-2][x] == " ":
                matrix[y-2][x] = "$"
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

            elif matrix[y-2][x] == ".":
                matrix[y-2][x] = "*"
                matrix[y-1][x] = "@"
                if target_found == True:
                    matrix[y][x] = "."
                else:
                    matrix[y][x] = " "
                target_found = True

        # if is_target
        elif matrix[y-1][x] == ".":
            print "Target Found"
            matrix[y-1][x] = "@"
            if target_found == True:
                matrix[y][x] = "."
            else:
                matrix[y][x] = " "
            target_found = True

        # else
        else:
            print "There is a wall here"

    gui.drawLevel(matrix)

    print "Boxes remaining: " + str(len(matrix.getBoxes()))

    if matrix.isEnd():
        gui.drawComplete()
        print "Level Completed"
        global current_level
        current_level += 1
        initLevel(level_set,current_level)

def initLevel(level_set,level):
    # Create an instance of this Level
    global myLevel
    myLevel = Level(level_set,level)

    # Draw this level
    gui.drawLevel(myLevel.getMatrix())

    global target_found
    target_found = False


target_found = False


def runGame(args):
    """
    Execute the game
    """
    global gui
    gui = SokobanGui()

    current_level = args.level
    level_set = args.set


    # Initialize Level
    initLevel(level_set,current_level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movePlayer("L",myLevel)
                elif event.key == pygame.K_RIGHT:
                    movePlayer("R",myLevel)
                elif event.key == pygame.K_DOWN:
                    movePlayer("D",myLevel)
                elif event.key == pygame.K_UP:
                    movePlayer("U",myLevel)
                elif event.key == pygame.K_u:
                    gui.drawLevel(myLevel.undo())
                elif event.key == pygame.K_r:
                    initLevel(level_set,current_level)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def default(str):
  return str + ' [Default: %default]'


def readCommand(argv):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python sokoban.py <options>
    EXAMPLES:   (1) python sokoban.py
                (2) python sokoban.py --level 2 to start level 2
    """
    parser = OptionParser(usageStr)

    parser.add_option('-l', '--level', dest='level', type='int',
                    help=default('The level to run'), metavar='level', default=1)
    parser.add_option('-s', '--set', dest='set', type='string',
                      help=default('The level set to run'), metavar='set', default="original")
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    return options


if __name__ == '__main__':
    """
    The main function called when sokoban.py is run
    from the command line:

    > python pacman.py

    See the usage string for more details.

    > python pacman.py --help
    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGame(args)
