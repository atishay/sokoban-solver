from collections import deque
import heapq
import numpy as np
from hungarian import Hungarian
import math

def hungarianDistance(method):
    def calc(state, cache):
        if 'hungarian' not in cache:
            cache['hungarian'] = {}
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        key = (",".join([str(x[0]) + "-" + str(x[1]) for x in boxes]),
               ",".join([str(x[0]) + "-" + str(x[1]) for x in targets]))
        total = 0
        if key in cache['hungarian']:
            total = cache['hungarian'][key]
        else :
            distance_list = []
            for b in boxes:
                distance_list.append([method(b, t) for t in targets])
            if len(distance_list) is 0:
                return 1
            array = np.array(distance_list, dtype='float64')
            hungarian = Hungarian(array)
            hungarian.calculate()
            total = hungarian.get_total_potential()
            cache['hungarian'][key] = total
        total += sum([method(player, b) for b in boxes] or [0])
        return total
    return calc

def distance(method):
    def calc(state, cache):
        # TODO: We could cache a lot of this. In most states
        # the position of most boxes don't change.
        if 'min_distance' not in cache:
            cache['min_distance'] = {}
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        total = 0
        key = (",".join([str(x[0]) + "-" + str(x[1]) for x in boxes]),
               ",".join([str(x[0]) + "-" + str(x[1]) for x in targets]))
        if key in cache['min_distance']:
            total = cache['min_distance'][key]
        else:
            for b in boxes:
                total += min([method(b, t) for t in targets] or [0])
            cache['min_distance'][key] = total
        total += sum([method(player, b) for b in boxes] or [0])
        return total

    return calc

def default(key, cache):
    if key is 'Move':
        return 1
    elif key is 'Push':
        return 2
    elif key is 'PushOut':
        return 10


def cost2(key, cache):
    if key is 'Move':
        return 2
    elif key is 'Push':
        return 1
    elif key is 'PushOut':
        return 2


class solver():
    cache = {}
    costs = {
        "none": lambda key, cache: 1,
        "default": default,
        "cost2": cost2
    }
    global distance
    heuristic = {
        "manhatten": distance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
        "none": lambda x, y: 0,
        "hungarian": hungarianDistance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
        "euclidean": distance(lambda x, y: math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)),
        "hungarian_euclidean": hungarianDistance(lambda x, y: math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2))
    }
    def refresh(self):
        self.cache = {}

    def dfs(self, startState, maxDepth=150, cache={}):
        stack = deque([(startState, "")])
        while len(stack) > 0:
            state, actions = stack.pop()
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                return (actions,len(cache))
            if state.isFailure():
                continue
            if len(actions) is maxDepth:
                continue
            for (action, _) in state.getPossibleActions():
                successor = state.successor(action)
                # Don't go to an explored state
                if successor.toString() in cache and cache[successor.toString()] <= len(actions) + 1:
                    continue
                # # Don't go to a state already marked for visit
                # if next((x for (x, _) in stack if x.toString() is successor.toString()), None) is not None:
                #     continue
                stack.append((successor, actions + action))
        return ("",0)

    def back(self, startState, maxDepth=float('inf'), cache={}):
        options = []
        stack = deque([(startState, "")])
        while len(stack) > 0:
            state, actions = stack.pop()
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                options.append(actions);
                continue
            if state.isFailure():
                continue
            if len(actions) is maxDepth:
                continue
            for (action, _) in state.getPossibleActions():
                successor = state.successor(action)
                # Don't go to an explored state
                if successor.toString() in cache and cache[successor.toString()] <= len(actions) + 1:
                    continue
                # # Don't go to a state already marked for visit
                # if next((x for (x, _) in stack if x.toString() is successor.toString()), None) is not None:
                #     continue
                stack.append((successor, actions + action))
        if len(options) is 0:
            return ("",0)
        return (min(options, key=lambda x: len(x)), len(cache))

    def bfs(self, startState, maxDepth=float('inf'), cache={}):
        return self.ucs(startState, cache=cache, cost="none")

    def ucs(self, startState, cost="default", maxCost=500, cache={}):
        return self.astar(startState, cost=cost, maxCost=maxCost, cache=cache, heuristic="none")

    def astar(self, startState, maxCost=1000, cost="default", heuristic="hungarian", cache={}):
        h = self.heuristic[heuristic]
        costCalc = self.costs[cost]
        queue = PriorityQueue()
        action_map = {}
        startState.h = h(startState, self.cache)
        queue.update(startState, startState.h)
        action_map[startState.toString()] = ""
        while not queue.empty():
            state, cost = queue.removeMin()
            actions = action_map[state.toString()]
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                return (actions,len(cache))
            if state.isFailure():
                continue
            if cost >= maxCost:
                continue
            for (action, cost_delta) in state.getPossibleActions():
                successor = state.successor(action)
                # Don't go to an explored state again
                if successor.toString() in cache:
                    continue
                old = action_map[successor.toString()] if successor.toString(
                ) in action_map else None
                if not old or len(old) > len(actions) + 1:
                    action_map[successor.toString()] = actions + action
                successor.h = h(successor, self.cache)
                queue.update(successor, cost + costCalc(cost_delta, self.cache) + successor.h - state.h)
        return ("",0)

    def dfsid(self, startState, maxDepth=500):
        i = 1
        # while True:
        while i<=maxDepth:
            val = self.dfs(startState, maxDepth=i, cache={})
            if val[0] is not "":
                return val
            # elif i < maxDepth:

            i = i + 1
        #Modified for metrics creation
        return ("",0)

    # def astarid(self):
    #     pass


def manhattenDistance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Data structure for supporting uniform cost search.
class PriorityQueue:
    def __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE:
                continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None)  # Nothing left...

    def empty(self):
        return len(self.heap) is 0
