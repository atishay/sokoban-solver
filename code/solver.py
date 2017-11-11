from collections import deque
import heapq


def distance(method):
    def calc(state):
        # TODO: We could cache a lot of this. In most states
        # the position of most boxes don't change.
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        total = 0
        for b in boxes:
            total += min([method(b, t) for t in targets] or [0])
        total += min([method(player, b) for b in boxes] or [0])
        return total

    return calc

class solver():
    costs = {
        "none": lambda key: 1,
        "default": lambda key: key
    }
    global distance
    heuristic = {
        "manhatten": distance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])),
        "none": lambda x: 0
    }
    def dfs(self, startState, maxDepth=50, cache={}):
        stack = deque([(startState, "")])
        while len(stack) > 0:
            state, actions = stack.pop()
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                return actions
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
        return ""

    def back(self, startState, maxDepth=130, cache={}):
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
            return ""
        return min(options, key=lambda x: len(x))

    def bfs(self, startState, maxDepth=50, cache={}):
        return self.ucs(startState, cache=cache, cost="none")

    def ucs(self, startState, cost="default", maxCost=500, cache={}):
        return self.astar(startState, cost=cost, maxCost=maxCost, cache=cache, heuristic="none")

    def astar(self, startState, maxCost=1000, cost="default", heuristic="manhatten", cache={}):
        h = self.heuristic[heuristic]
        costCalc = self.costs[cost]
        queue = PriorityQueue()
        action_map = {}
        startState.h = h(startState)
        queue.update(startState, startState.h)
        action_map[startState.toString()] = ""
        while not queue.empty():
            state, cost = queue.removeMin()
            actions = action_map[state.toString()]
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                return actions
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
                successor.h = h(successor)
                queue.update(successor, cost + costCalc(cost_delta) + successor.h - state.h)
        return ""

    def dfsid(self, startState, maxDepth=100):
        i = 1
        while True:
            val = self.dfs(startState, maxDepth=i, cache={})
            if val is not "":
                return val
            elif i < maxDepth:
                i = i + 1


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
