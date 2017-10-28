
class solver():
    def dfs(self, startState, cost=[1,2], maxDepth=10):
        def recurse(state, depth, actions):
            if state.isSuccess():
                return actions
            if state.isFailure():
                return []
            if depth is maxDepth:
                return ""
            for action in "LRUD":
                successor = state.successor(action)
                op = recurse(successor, depth + 1, actions + action)
                if len(op) > 0:
                    return op
            return ""
        return recurse(startState, 0, "")

    def bfs(self, startState, cost=[1, 2], maxDepth=500):
        pass

    def back(self, startState, cost=[1, 2], maxDepth=500):
        pass

    def ucs(self, startState, cost=[1, 2], maxDepth=500):
        pass

    def astar(self, startState, cost=[1, 2], maxDepth=500):
        pass
