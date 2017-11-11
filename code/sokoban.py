# Name: pySokoban
# Description: A sokoban implementation using python & pyGame
# Author: Kazantzakis Nikos <kazantzakisnikos@gmail.com>
# Date: 2015
# Last Modified: 31-03-2016


import pygame
import sys
import solver
import time
from multiprocessing import Process, Queue
from memory_profiler import profile

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
    if args.method == "human":
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
            moves = solve(args, myLevel)
            if moves is not "":
                for move in moves:
                    movePlayer(move, myLevel)
                    if args.gui == "True":
                        pygame.time.wait(100)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                                pygame.quit()
                                sys.exit()
            else:
                print "Failed for level %d"%(current_level)
                current_level = current_level + 1


# @profile
def solveInternal(cache, method, ret):
    solution = solver.solver()
    moves = []
    if method == "dfs":
        moves = solution.dfs(myLevel.getMatrix(), cache=cache)
    elif method == "bfs":
        moves = solution.bfs(myLevel.getMatrix(), cache=cache)
    elif method == "ucs":
        moves = solution.ucs(myLevel.getMatrix(), cache=cache)
    elif method == "back":
        moves = solution.back(myLevel.getMatrix(), cache=cache)
    elif method == "astar":
        moves = solution.astar(myLevel.getMatrix(), cache=cache)
    # elif method == "astarid":
    #     moves = solution.astarid(myLevel.getMatrix())
    elif method == "dfsid":
        moves = solution.dfsid(myLevel.getMatrix())
    ret.put(moves)
    # return moves

def solve(args, myLevel):
    log_file = open(args.method + '.txt', 'a')
    start_time = time.time() * 1000
    cache = {}
    ret = Queue()
    p = Process(target=solveInternal, args=(cache, args.method, ret))
    p.start()
    p.join(args.timeout)
    moves = ""
    global current_level

    if not ret.empty():
        moves = ret.get()
        log_file.write(args.set + ',' + str(current_level) + ',' + args.method + ',' + str(time.time() * 1000 - start_time) +
                       ',' + str(len(moves)) + ',' + str(len(cache)) + '\n')
    else:
        print "Timeout"
        log_file.write(args.set + ',' + str(current_level) + ',' + args.method + ',' + "999999" +
                       ',' + str(len(moves)) + ',' + str(len(cache)) + '\n')

    # solveInternal(method=args.method, cache=cache)
    print "Level: %d, Moves: %s Length: %d" % (current_level, moves, len(moves))
    return moves


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
    parser.add_option('-g', '--gui', dest='gui',
                      help=default('Run in CLI mode'), metavar='gui', default="True")
    parser.add_option('-t', '--timeout', dest='timeout', type='int',
                      help=default('Timeout for the method'), metavar='gui', default=60)
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
