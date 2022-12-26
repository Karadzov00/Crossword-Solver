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
        print(variables)

        self.initialize(tiles, variables, words, matrix, currentDomains)

        keys = list(variables.keys())
        variables_copy = copy.deepcopy(variables)

        backwardsFlag = False

        self.backtracking(matrix, currentDomains, keys, 0, variables_copy, backwardsFlag, words, moves_list)

        domains = {var: [word for word in words] for var in variables}
        solution = []

        for move in moves_list:
            solution.append([move[0], move[1], domains])
        return solution

    def backtracking(self, matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list):
        if level == len(keys):
            return True
        curVar = keys[level]
        print(curDomains)
        if not backwardsFlag:
            curDomains[curVar] = copy.deepcopy(words)
            self.reduceDomains(curVar, curDomains, matrix, keys, level, variables)
            if len(curDomains[curVar]) > 0:
                word = curDomains[curVar][0]
                direction = curVar[len(curVar) - 1]
                print(direction)
                position = int(curVar[:-1])
                print(position)
                numCols = len(matrix[0])
                row = int(position / len(matrix[0]))
                col = int(position % len(matrix[0]))
                print(col)
                print(row)
                wordLen = variables[curVar]
                print(wordLen)
                if direction == 'h':
                    for i in range(wordLen):
                        matrix[row][col + i] = word[i]
                elif direction == 'v':
                    for i in range(wordLen):
                        matrix[row + i][col] = word[i]
                print(matrix)
                ind = words.index(word)
                moves_list.append([curVar, ind])
                print(moves_list)
                level += 1
                backwardsFlag = False

            else:
                curDomains[curVar] = copy.deepcopy(words)
                moves_list.append([curVar, None])
                print(matrix)
                print(moves_list)

                backwardsFlag = True
                level -= 1
        else:
            if len(curDomains[curVar]) > 1:
                curDomains[curVar].pop(0)
                word = curDomains[curVar][0]
                direction = curVar[len(curVar) - 1]
                print(direction)
                position = int(curVar[:-1])
                print(position)
                col = int(position / len(matrix[0]))
                row = int(position % len(matrix[0]))
                print(col)
                print(row)
                wordLen = variables[curVar]
                print(wordLen)
                if direction == 'h':
                    for i in range(wordLen):
                        matrix[row][col + i] = word[i]
                elif direction == 'v':
                    for i in range(wordLen):
                        matrix[row + i][col] = word[i]
                print(matrix)
                ind = words.index(word)
                moves_list.append([curVar, ind])
                print(moves_list)
                level += 1
                backwardsFlag = False
            else:
                # only 1 value left so when we cross it no value will remain, os backtrack again
                curDomains[curVar] = copy.deepcopy(words)
                moves_list.append([curVar, None])
                print(matrix)
                print(moves_list)

                level -= 1
                backwardsFlag = True
        self.backtracking(matrix, curDomains, keys, level, variables, backwardsFlag, words, moves_list)

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

    def initialize(self, tiles, variables, words, matrix, currentDomains):

        print(matrix)

        for var in variables:
            currentDomains[var] = copy.deepcopy(words)

        print(currentDomains)
