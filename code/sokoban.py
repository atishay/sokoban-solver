# Name: pySokoban
# Description: A sokoban implementation using python & pyGame
# Author: Kazantzakis Nikos <kazantzakisnikos@gmail.com>
# Date: 2015
# Last Modified: 31-03-2016


# import time
import pygame
import sys
import solver

from gui import SokobanGui
from Level import Level

def movePlayer(direction,myLevel):

    matrix = myLevel.getMatrix()

    myLevel.addToHistory(matrix)

    matrix.successor(direction, True)

    gui.drawLevel(matrix)

    # print "Boxes remaining: " + str(len(matrix.getBoxes()))

    if matrix.isSuccess():
        gui.drawComplete()
        # print "Level Completed"
        global current_level
        current_level += 1
        initLevel(level_set,current_level)

def initLevel(level_set,level):
    # Create an instance of this Level
    global myLevel
    myLevel = Level(level_set,level)

    # Draw this level
    gui.drawLevel(myLevel.getMatrix())


def runGame(args):
    """
    Execute the game
    """
    global gui
    gui = SokobanGui()
    global current_level
    current_level = args.level
    global level_set
    level_set = args.set


    # Initialize Level
    initLevel(level_set,current_level)
    if args.method is "human":
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
    else:
        old_level = current_level - 1
        while old_level is current_level - 1:
            old_level = current_level
            solution = solver.solver()
            moves = []
            if args.method == "dfs":
                moves = solution.dfs(myLevel.getMatrix())
            elif args.method == "bfs":
                moves = solution.bfs(myLevel.getMatrix())
            elif args.method == "ucs":
                moves = solution.ucs(myLevel.getMatrix())
            elif args.method == "astar":
                moves = solution.astar(myLevel.getMatrix())

            print "Level: %d, Moves: %s"%(current_level, moves)
            if moves is not "":
                for move in moves:
                    movePlayer(move, myLevel)

            else:
                print "Failed for level"





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
    parser.add_option('-m', '--method', dest='method', type='string',
                    help=default('The method set to solve'), metavar='method', default="human")
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
