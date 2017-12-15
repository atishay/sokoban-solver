import sys
import solver
from Level import Level

def movePlayer(direction,myLevel):

    matrix = myLevel.getMatrix()

    myLevel.addToHistory(matrix)

    matrix.successor(direction, True)

    if matrix.isSuccess():
        global current_level
        current_level += 1
        initLevel(level_set,current_level)

def initLevel(level_set,level):
    # Create an instance of this Level
    global myLevel
    myLevel = Level(level_set,level)


def runGame(args):
    """
    Execute the game
    """

    global current_level
    current_level = args.level
    global level_set
    level_set = "project_levels"


    # Initialize Level
    if current_level==30:
        pygame.quit()
        sys.exit()
    initLevel(level_set,current_level)
    count=0

    old_level = current_level - 1
    while old_level is current_level - 1:
        if current_level==args.last_level:
            sys.exit()
        old_level = current_level
        moves = solve(args, myLevel)
        if moves is not "":
            for move in moves:
                movePlayer(move, myLevel)
        else:
            print "Failed for level %d"%(current_level)

            current_level = current_level + 1
            if current_level==args.last_level:
                # pygame.quit()
                sys.exit()
            initLevel(level_set,current_level)



# @profile
def solveInternal(cache, method, cost, heuristic):
    solution = solver.solver()
    solution.refresh()
    moves = []
    moves_cache=[]
    if method == "dfs":
        moves_cache = solution.dfs(myLevel.getMatrix(), cache=cache)
    elif method == "bfs":
        moves_cache = solution.bfs(myLevel.getMatrix(), cache=cache)
    elif method == "ucs":
        moves_cache = solution.ucs(myLevel.getMatrix(), cache=cache)
    elif method == "back":
        moves_cache = solution.back(myLevel.getMatrix(), cache=cache)

    elif method == "astar":
        moves_cache = solution.astar(myLevel.getMatrix(), cache=cache, cost=cost, heuristic=heuristic)
    # elif method == "astarid":
    #     moves = solution.astarid(myLevel.getMatrix())
    elif method == "dfsid":
        moves_cache = solution.dfsid(myLevel.getMatrix())
    # ret.put(moves_cache)
    return moves_cache

def solve(args, myLevel):
    moves_cache = solveInternal(method=args.method, cache={}, cost=args.cost, heuristic=args.heuristic)
    print "Level: %d, Moves: %s Length: %d States Explored: %d" % (current_level, moves_cache[0], len(moves_cache[0]), moves_cache[1])
    return moves_cache[0]


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
    parser.add_option('-m', '--method', dest='method', type='string',
                    help=default('The method set to solve'), metavar='method', default="astar")
    parser.add_option('-c', '--cost', dest='cost', type='string',
                      help=default('Cost function to use'), metavar='cost', default="default")
    parser.add_option('-f', '--heuristic', dest='heuristic', type='string',
                      help=default('Heuristic function to use'), metavar='heuristic', default="hungarian")
    parser.add_option('-x', '--last_level', dest='last_level', type='int',
                      help=default('The max level to compute to'), metavar='last_level', default=30)
    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    return options


if __name__ == '__main__':
    """
    The main function called when sokoban.py is run
    from the command line:

    > python sokoban.py
    """
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGame(args)
