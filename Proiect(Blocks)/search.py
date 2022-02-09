import random
import util
import copy
import searchAgent

import time
start_time = time.time()

nb_expanded = 0
nb_generated = 0

class BlockPuzzleState:

    def __init__(self, stacks):
        self.stacks = stacks

    def random_generation(no_stacks, no_blocks):
        l_stacks = []
        for i in range(no_stacks):
            l_stacks.append(util.Stack())

        for i in range(no_blocks):
            x = int(random.random() * no_stacks)
            l_stacks[x].push(i)
        return l_stacks

    def getStacks(self):
        return self.stacks

    def isGoal(self, puzzle):
        if puzzle == 1:
            if self.stacks[0] == [] and self.stacks[1] == [2, 1, 0] and self.stacks[2] == []:
                return True
            else:
                return False
        if puzzle == 2:

            if self.stacks[0] == [2, 0] and self.stacks[1] == [3, 1] and self.stacks[2] == [4]:
                return True
            else:
                return False
        if puzzle == 3:
            if self.stacks[0] == [2, 0] and self.stacks[1] == [3, 4] and self.stacks[2] == [5, 1]:
                return True
            else:
                return False

    def __eq__(self, other):
        for i in range(len(self.stacks)):
            if self.getStacks()[i] != other.getStacks()[i]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.stacks))


class Node_search:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.cost = cost  # retinem si actiunea? (blocul mutat, starea init a blocului, starea fin a blocului)

    def getState(self):
        return self.state

    def getCost(self):
        return self.cost

    def getParent(self):
        return self.parent

    def getPath(self):
        path = [self]
        node = self
        while node.getParent() is not None:
            path.insert(0, node.getParent())
            node = node.getParent()
        return path

    # def afisDrum(self, afisezCost=False):  # functie ce afiseaza drumul parcurs
    #     parents = self.getPath()
    #     for nodCurent in parents:
    #         print(str(nodCurent))
    #     if afisezCost:
    #         print("Cost: ", self.cost)

    def __str__(self):
        to_print = ""
        for stack in self.state.getStacks():
            to_print += (str(stack)) + "\n"
        to_print += "######################\n"
        return to_print


class BlockPuzzleSearchProblem:

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state, no_puzzle):
        return state.isGoal(no_puzzle)

    def generateSuccsesors(self, currentNode):
        succsesors = []
        c_stacks = currentNode.getState()
        no_stacks = len(c_stacks.getStacks())
        i = 0
        for idx in range(no_stacks):
            copy_intern = copy.deepcopy(c_stacks.getStacks())
            # print("Sunt la stiva " + str(idx))
            if copy_intern[idx].isEmpty():
                continue
            block = copy_intern[idx].pop()

            for j in range(no_stacks):
                if idx == j:
                    continue
                stacks_n = copy.deepcopy(copy_intern)
                stacks_n[j].push(block)

                nod_nou = Node_search(BlockPuzzleState(stacks_n), currentNode, 1)
                if nod_nou not in succsesors:
                    succsesors.append(nod_nou)

            copy_intern[idx].push(block)

            # for stiva in copie_interm:
            #     print("Stiva ramasa contine:")
            #     print(str(stiva))

        return succsesors

    def newPosition(node, otherNode):
        no_stacks = len(node.getState().getStacks())
        s1 = node.getState().getStacks()
        s2 = otherNode.getState().getStacks()
        for idx in range(no_stacks):
            if s1[idx] == s2[idx]:
                continue
            else:
                if len(s1[idx]) < len(s2[idx]):
                    x = idx
                    y = len(s2[idx])
                    position = (x, y)
                    return position

    def movedBlok(node, otherNode):
        no_stacks = len(node.getState().getStacks())
        s1 = node.getState().getStacks()
        s2 = otherNode.getState().getStacks()
        for idx in range(no_stacks):
            if s1[idx] == s2[idx]:
                continue
            else:
                if len(s1[idx]) < len(s2[idx]):
                    x = s2[idx].top()
                    return x

def depthFirstSearch(problem, no_puzzle):
    global nb_expanded
    nb_expanded = 0

    global nb_generated
    nb_generated = 0

    if problem.isGoalState(problem.getStartState(), no_puzzle):
        # print("Number of expandaded nodes: " + str(nb_expanded))
        return []

    currNode = None
    stack = util.Stack()
    vis = []

    startNode = Node_search(problem.getStartState(), None, 0)
    stack.push(startNode)

    while not stack.isEmpty():

        nb_generated += 1

        currNode = stack.pop()
        if problem.isGoalState(currNode.getState(), no_puzzle):
            break

        if currNode.getState() not in vis:

            vis.append(currNode.getState())
            succ = problem.generateSuccsesors(currNode)

            nb_expanded += 1

            for n in succ:
                if n.getState() not in vis:
                    stack.push(n)
    sol = []
    while currNode.getParent() != None:
        sol.append(currNode.getState())
        currNode = currNode.getParent()

    sol.reverse()
    # print("Number of expandaded nodes: " + str(nb_expanded))
    return sol


def breadthFirstSearch(problem, no_puzzle):
    global nb_expanded
    nb_expanded = 0

    global nb_generated
    nb_generated = 0

    if problem.isGoalState(problem.getStartState(), no_puzzle):
        # print("Number of expandaded nodes: " + str(nr_expand))
        return []

    currNode = None
    queue = util.Queue()
    vis = []

    startNode = Node_search(problem.getStartState(), None, 0)
    # print(startNode)
    queue.push(startNode)

    while not queue.isEmpty():

        nb_generated += 1

        currNode = queue.pop()
        # print(currNode)

        if problem.isGoalState(currNode.getState(), no_puzzle):
            break

        if currNode.getState() not in vis:

            succ = problem.generateSuccsesors(currNode)
            vis.append(currNode.getState())

            nb_expanded += 1

            for n in succ:
                queue.push(n)
                if problem.isGoalState(n.getState(), no_puzzle):
                    # print(n)
                    break
    sol = []
    while currNode.getParent():
        sol.append(currNode.getState())
        currNode = currNode.getParent()

    sol.reverse()

    # print("Number of expandaded nodes: " + str(nb_expanded))
    return sol


def uniformCostSearch(problem, no_puzzle):
    global nb_expanded
    nb_expanded = 0

    global nb_generated
    nb_generated = 0

    queue = util.PriorityQueue()
    vis = []
    sol = []

    if problem.isGoalState(problem.getStartState(), no_puzzle):
        # print("Number of expandaded nodes: " + str(nb_expanded))
        return []

    startNode = Node_search(problem.getStartState(), None, 0)
    queue.push((startNode, sol), startNode.getCost())

    while not queue.isEmpty():

        nb_generated += 1

        t, sol = queue.pop()
        if problem.isGoalState(t.getState(), no_puzzle):
            sol = sol + [t.getState()]
            # print("Number of expandaded nodes: " + str(nb_expanded))
            return sol

        succ = problem.generateSuccsesors(t)

        nb_expanded += 1

        for n in succ:
            if n.getState() not in vis:
                nPath = sol + [n.getParent().getState()]
                vis.append(n.getState())
                queue.update((n, nPath), len(nPath))  # problem.getCostOfActionSequence(nPath)

    # print("Number of expandaded nodes: " + str(nb_expanded))
    return sol


def aStarSearch(problem, no_puzzle, heuristic=searchAgent.manhattanHeuristic):
    global nb_expanded
    nb_expanded = 0

    global nb_generated
    nb_generated = 0

    queue = util.PriorityQueue()  # frontiera
    vis = []  # teritoriu
    sol = []

    if problem.isGoalState(problem.getStartState(), no_puzzle):
        # print("Number of expandaded nodes: " + str(nb_expanded))
        return []

    startNode = Node_search(problem.getStartState(), None, 0)
    queue.push((startNode, sol), startNode.getCost())

    while not queue.isEmpty():

        nb_generated += 1

        t, sol = queue.pop()
        if problem.isGoalState(t.getState(), no_puzzle):
            sol = sol + [t.getState()]
            # print("Number of expandaded nodes: " + str(nb_expanded))
            return sol

        succ = problem.generateSuccsesors(t)

        nb_expanded += 1

        for n in succ:
            if n.getState() not in vis:
                nPath = sol + [n.getParent().getState()]
                vis.append(n.getState())

                pos = BlockPuzzleSearchProblem.newPosition(t, n)
                block = BlockPuzzleSearchProblem.movedBlok(t, n)
                x = 0
                if heuristic == searchAgent.manhattanHeuristic:
                    x = searchAgent.manhattanHeuristic(pos, block, no_puzzle)
                elif heuristic == searchAgent.chebisevDistance:
                    x = searchAgent.chebisevDistance(pos, block, no_puzzle)
                elif heuristic == searchAgent.chiSquaredDistance:
                    x = searchAgent.chiSquaredDistance(pos, block, no_puzzle)
                else:
                    x = searchAgent.euclideanHeuristic(pos, block, no_puzzle)
                queue.update((n, nPath),
                             len(nPath) + x)  # update daca nu exist nodul de updatat ii face push asa ca este nevoide doar de update si nu de 2 if - uri
    # print("Number of expandaded nodes: " + str(nb_expanded))
    return sol


b = BlockPuzzleState(BlockPuzzleState.random_generation(3, 6))
incercare = BlockPuzzleSearchProblem(b)

# sol = breadthFirstSearch(incercare, 3)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
#
# sol = depthFirstSearch(incercare, 3)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
#
# sol = uniformCostSearch(incercare, 3)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
#
# sol = aStarSearch(incercare, 3, searchAgent.manhattanHeuristic)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
# #
# sol = aStarSearch(incercare, 3, searchAgent.euclideanHeuristic)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
#
# sol = aStarSearch(incercare, 3, searchAgent.chebisevDistance)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
#
# sol = aStarSearch(incercare, 3, searchAgent.chiSquaredDistance)
# print("--- %s seconds ---" % (time.time() - start_time))
# print("Number of generated nodes: " + str(nb_generated))
# print("Number of expandaded nodes: " + str(nb_expanded))
# print(str(len(sol)))
