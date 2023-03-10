import copy


class Algorithm:
    def get_algorithm_steps(self, tiles, variables, words):
        pass


class ExampleAlgorithm(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = [['0h', 0], ['0v', 2], ['1v', 1], ['2h', 1], ['4h', None],
                      ['2h', None], ['1v', None], ['0v', 3], ['1v', 1], ['2h', 1],
                      ['4h', 4], ['5v', 5]]

        domains = {var: [word for word in words] for var in variables}
        solution = []
        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution


class Backtracking(Algorithm):

    def get_algorithm_steps(self, tiles, variables, words):
        moves_list = []

        rows = len(tiles)
        cols = len(tiles[0])

        matrix = [[0] * len(tiles[0]) for i in range(len(tiles))]
        # matrix[0][0] = 'a'
        # matrix[1][0] = 'b'
        # matrix[0][1] = 'c'
        # print(matrix)
        currentDomains = {}
        varsNow = {}
        print(variables)

        self.initialize(tiles, variables, words, matrix, currentDomains, varsNow)

        keys = list(variables.keys())
        variables_copy = copy.deepcopy(variables)

        backwardsFlag = False

        # self.backtracking(matrix, currentDomains, keys, 0, variables_copy, backwardsFlag, words, moves_list, varsNow)
        graph = {}
        self.formGraph(tiles, variables, words, graph)
        self.forwardChecking(matrix, currentDomains, keys, 0, variables_copy, backwardsFlag, words, moves_list, varsNow,
                             graph)

        domains = {var: [word for word in words] for var in variables}
        solution = []

        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution



    def backtracking(self, matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list, varsNow):
        if level == len(keys):
            return True
        curVar = keys[level]
        print(curDomains)
        if not backwardsFlag:
            curDomains[curVar] = copy.deepcopy(words)
            self.removeFromMatrix(matrix, variables, varsNow)
            self.reduceDomains(curVar, curDomains, matrix, keys, level, variables)
            if len(curDomains[curVar]) > 0:
                word = curDomains[curVar][0]
                self.writeWordInMatrix(curVar, matrix, variables, word)

                print(matrix)
                varsNow[curVar] = word
                ind = words.index(word)
                moves_list.append([curVar, ind])
                print(moves_list)
                level += 1
                backwardsFlag = False

            else:
                self.goBackwards(curDomains, curVar, varsNow, matrix, moves_list, words)
                backwardsFlag = True
                level -= 1
        else:
            if len(curDomains[curVar]) > 1:
                curDomains[curVar].pop(0)
                word = curDomains[curVar][0]
                self.writeWordInMatrix(curVar, matrix, variables, word)

                print(matrix)
                varsNow[curVar] = word
                ind = words.index(word)
                moves_list.append([curVar, ind])
                print(moves_list)
                level += 1
                backwardsFlag = False
            else:
                # only 1 value left so when we cross it no value will remain, so backtrack again
                self.goBackwards(curDomains, curVar, varsNow, matrix, moves_list, words)
                level -= 1
                backwardsFlag = True
        self.backtracking(matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list, varsNow)


    def goBackwards(self, curDomains, curVar, varsNow, matrix, moves_list, words):
        curDomains[curVar] = copy.deepcopy(words)
        moves_list.append([curVar, None])
        print(matrix)
        print(moves_list)
        varsNow[curVar] = None

    def reduceDomains(self, curVar, currentDomains, matrix, keys, level, variables):
        n = len(currentDomains[curVar])
        i = 0

        # cut domains for words with different length
        while i < n:
            if len(currentDomains[curVar][i]) != variables[curVar]:
                currentDomains[curVar].pop(i)
                n = n - 1
            else:
                i = i + 1

        direction = curVar[len(curVar) - 1]
        startPosition = int(curVar[:-1])
        curRow = int(startPosition / len(matrix[0]))
        curCol = int(startPosition % len(matrix[0]))

        # cut domains for words that doesn't match letters in matrix
        # variables[curVar] is the length of the current variable
        for j in range(variables[curVar]):
            length = len(currentDomains[curVar])  # length of current var domain array
            k = 0

            if direction == 'v':
                # iterate through all words in hashmap for that var
                while k < length:
                    # here are only words of equal length
                    if matrix[curRow][curCol] != 0 and matrix[curRow][curCol] != currentDomains[curVar][k][j]:
                        currentDomains[curVar].pop(k)
                        length -= 1
                        # go to next field
                    else:
                        k += 1

                curRow += 1
                # curCol stays the same

            elif direction == 'h':
                while k < length:
                    # here are only words of equal length
                    if matrix[curRow][curCol] != 0 and matrix[curRow][curCol] != currentDomains[curVar][k][j]:
                        currentDomains[curVar].pop(k)
                        length -= 1
                        # go to next field
                    else:
                        k += 1

                curCol += 1
                # curRow stays the same

    def initialize(self, tiles, variables, words, matrix, currentDomains, varsNow):

        print(matrix)

        for var in variables:
            currentDomains[var] = copy.deepcopy(words)
            varsNow[var] = None

        print(currentDomains)

    def removeFromMatrix(self, matrix, variables, varsNow):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                matrix[i][j] = 0

        for var in variables:
            if varsNow[var] is not None:
                word = varsNow[var]
                direction = var[len(var) - 1]
                position = int(var[:-1])
                numCols = len(matrix[0])
                row = int(position / numCols)
                col = int(position % numCols)

                wordLen = variables[var]
                print(wordLen)
                if direction == 'h':
                    for i in range(wordLen):
                        matrix[row][col] = word[i]
                        col += 1
                elif direction == 'v':
                    for i in range(wordLen):
                        matrix[row][col] = word[i]
                        row += 1
                print(matrix)

    def forwardChecking(self, matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list, varsNow,
                        graph):
        if level == len(keys):
            return True
        curVar = keys[level]
        changedList = set()
        print(curDomains)
        if not backwardsFlag:
            curDomains[curVar] = copy.deepcopy(words)
            self.removeFromMatrix(matrix, variables, varsNow)
            self.reduceDomains(curVar, curDomains, matrix, keys, level, variables)
            if len(curDomains[curVar]) > 0:
                word = curDomains[curVar][0]
                self.writeWordInMatrix(curVar, matrix, variables, word)

                print(matrix)
                varsNow[curVar] = word
                ind = words.index(word)
                moves_list.append([curVar, ind])
                print(moves_list)

                fc_backtrack = False
                # forward check
                for neighbor in graph[curVar]:
                    self.removeFromMatrix(matrix, variables, varsNow)
                    self.reduceDomainsFC(neighbor, curDomains, matrix, keys, level, variables, changedList)
                    if len(curDomains[neighbor]) == 0:
                        print("Cur Domains after forward check")
                        print(curDomains)
                        backwardsFlag = True
                        fc_backtrack = True
                        # refresh the domain of neighbor
                        curDomains[neighbor] = copy.deepcopy(words)
                        varsNow[neighbor] = None
                        # level stays the same
                        break
                print("Cur Domains after forward check")
                print(curDomains)
                print("Changed List after fc:")
                print(changedList)

                self.arcConsistency(matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list,
                                    varsNow, graph, changedList, fc_backtrack)

                if not fc_backtrack:
                    level += 1
                    backwardsFlag = False

            else:
                self.goBackwards(curDomains, curVar, varsNow, matrix, moves_list, words)

                backwardsFlag = True
                level -= 1
        else:
            if len(curDomains[curVar]) > 1:
                curDomains[curVar].pop(0)
                word = curDomains[curVar][0]
                self.writeWordInMatrix(curVar, matrix, variables, word)

                print(matrix)
                varsNow[curVar] = word
                ind = words.index(word)
                moves_list.append([curVar, ind])
                fc_backtrack = False
                # forward check
                for neighbor in graph[curVar]:
                    self.removeFromMatrix(matrix, variables, varsNow)
                    self.reduceDomainsFC(neighbor, curDomains, matrix, keys, level, variables, changedList)
                    if len(curDomains[neighbor]) == 0:
                        print("Cur Domains after forward check")
                        print(curDomains)
                        backwardsFlag = True
                        fc_backtrack = True
                        curDomains[neighbor] = copy.deepcopy(words)
                        varsNow[neighbor] = None
                        # level stays the same
                        break
                print("Cur Domains after forward check")
                print(curDomains)
                print("Changed List after fc:")
                print(changedList)

                self.arcConsistency(matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list,
                                    varsNow, graph, changedList, fc_backtrack)

                if not fc_backtrack:
                    level += 1
                    backwardsFlag = False
            else:
                # only 1 value left so when we cross it no value will remain, so backtrack again
                self.goBackwards(curDomains, curVar, varsNow, matrix, moves_list, words)

                level -= 1
                backwardsFlag = True
        self.forwardChecking(matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list, varsNow,
                             graph)

    def formGraph(self, tiles, variables, words, graph):
        variableList = list(variables.keys())
        verticalList = []
        horizontalList = []

        for var in variableList:
            graph[var] = []
            direction = var[len(var) - 1]
            position = int(var[:-1])
            if direction == 'h':
                horizontalList.append(position)
            elif direction == 'v':
                verticalList.append(position)

        print(horizontalList)
        print(verticalList)
        print(tiles)
        print(graph)

        for var in variableList:
            direction = var[len(var) - 1]
            position = int(var[:-1])
            numCols = len(tiles[0])
            row = int(position / numCols)
            col = int(position % numCols)
            if direction == 'h':
                for i in range(variables[var]):
                    # reset rows
                    row = int(position / numCols)
                    while True:
                        if row == 0 or tiles[row - 1][col] is True:
                            break
                        else:
                            row -= 1

                    # calculate number from col and row
                    number = len(tiles[0]) * row + col
                    cnt = verticalList.count(number)
                    # add variable to graph as a neighbor of current variable
                    if cnt > 0:
                        fullVar = str(number) + 'v'
                        graph[var].append(fullVar)
                    col += 1
            elif direction == 'v':
                for i in range(variables[var]):
                    # reset cols
                    col = int(position % numCols)
                    while True:
                        if col == 0 or tiles[row][col - 1] is True:
                            break
                        else:
                            col -= 1

                    # calculate number from col and row
                    number = len(tiles[0]) * row + col
                    cnt = horizontalList.count(number)
                    # add variable to graph as a neighbor of current variable
                    if cnt > 0:
                        fullVar = str(number) + 'h'
                        graph[var].append(fullVar)
                    row += 1
        print(graph)

    def reduceDomainsFC(self, curVar, currentDomains, matrix, keys, level, variables, changedList):
        n = len(currentDomains[curVar])
        i = 0

        # cut domains for words with different length
        while i < n:
            if len(currentDomains[curVar][i]) != variables[curVar]:
                currentDomains[curVar].pop(i)
                n = n - 1
                changedList.add(curVar)
            else:
                i = i + 1

        direction = curVar[len(curVar) - 1]
        startPosition = int(curVar[:-1])
        curRow = int(startPosition / len(matrix[0]))
        curCol = int(startPosition % len(matrix[0]))

        # cut domains for words that doesn't match letters in matrix
        # variables[curVar] is the length of the current variable
        for j in range(variables[curVar]):
            length = len(currentDomains[curVar])  # length of current var domain array
            k = 0

            if direction == 'v':
                # iterate through all words in hashmap for that var
                while k < length:
                    # here are only words of equal length
                    if matrix[curRow][curCol] != 0 and matrix[curRow][curCol] != currentDomains[curVar][k][j]:
                        currentDomains[curVar].pop(k)
                        length -= 1
                        # go to next field
                    else:
                        k += 1

                curRow += 1
                # curCol stays the same

            elif direction == 'h':
                while k < length:
                    # here are only words of equal length
                    if matrix[curRow][curCol] != 0 and matrix[curRow][curCol] != currentDomains[curVar][k][j]:
                        currentDomains[curVar].pop(k)
                        length -= 1
                        # go to next field
                        changedList.add(curVar)
                    else:
                        k += 1

                curCol += 1
                # curRow stays the same

    def arcConsistency(self, matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list, varsNow,
                       graph, changedList, fc_backtrack):
        while len(changedList) > 0:
            if backwardsFlag:
                break
            print("\n arcConsistency \n \n")
            node = changedList.pop()

            print(node)
            neighbors = graph[node]
            print("neighbors")
            print(neighbors)
            print("branches")
            for firstVar in graph[node]:
                if varsNow[firstVar] is None:
                    print(firstVar + "-" + node)
                    self.reduceDomains(firstVar, curDomains, matrix, keys, level, variables)

                    length = len(curDomains[firstVar])
                    k = 0
                    while k < length:
                        word = curDomains[firstVar][k]
                        self.writeWordInMatrix(firstVar, matrix, variables, word)
                        print("word is " + word)
                        print("\n Matrix after writing word from firstVar domain \n")
                        print(matrix)
                        print("\n")
                        tempDomains = copy.deepcopy(curDomains)
                        self.reduceDomains(node, tempDomains, matrix, keys, level, variables)
                        print("domains of node")
                        print(tempDomains[node])
                        if len(tempDomains[node]) == 0:
                            print("domains of firstVar before deletion")
                            print(curDomains[firstVar])
                            curDomains[firstVar].pop(k)
                            changedList.add(firstVar)
                            length -= 1
                            print("domains of firstVar after deletion")
                            print(curDomains[firstVar])
                            if len(curDomains[firstVar])==0:
                                print("Cur Domains after forward check")
                                print(curDomains)
                                backwardsFlag = True
                                fc_backtrack = True
                                curDomains[firstVar] = copy.deepcopy(words)
                                varsNow[firstVar] = None
                                break

                        else:
                            k += 1

                        self.removeFromMatrix(matrix, variables, varsNow)
                        print(" matrix after removing ")
                        print(matrix)


    def writeWordInMatrix(self, curVar, matrix, variables, word):
        direction = curVar[len(curVar) - 1]
        position = int(curVar[:-1])
        print(position)
        numCols = len(matrix[0])
        row = int(position / numCols)
        col = int(position % numCols)
        print(col)
        print(row)
        wordLen = variables[curVar]
        print(wordLen)
        if direction == 'h':
            for i in range(wordLen):
                matrix[row][col] = word[i]
                col += 1
        elif direction == 'v':
            for i in range(wordLen):
                matrix[row][col] = word[i]
                row += 1
