import re
import sys
import codecs
import time


class Node:
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.isWordFinished = False

    def findChildByChar(self, char):
        for child in self.children:
            if child.char == char:
                return child

        return None


def addNode(rootNode, word: str):
    word = word.lower()
    currentNode = rootNode
    for char in word:
        foundChild = currentNode.findChildByChar(char)

        if foundChild:
            currentNode = foundChild
        else:
            newNode = Node(char)
            currentNode.children.append(newNode)
            currentNode = newNode

    # Once added word is finished, we mark current node as such
    currentNode.isWordFinished = True


def makeLettersMatrix(letters: str):
    letters = letters[:]
    if len(letters) != 16:
        print("Letters must be 16 characters long. Input was " +
              str(len(letters)) + " long")
        raise TypeError

    matrix = [[0 for x in range(4)] for y in range(4)]
    for y in range(0, 4):
        row = []
        for x in range(0, 4):
            matrix[x][y] = letters[0]
            letters = letters[1:]
        matrix.append(row)

    print("Initialized letters matrix")
    print("------------------------")
    for y in range(0, 4):
        for x in range(0, 4):
            print(matrix[x][y].upper(), end="")
        print("")

    return matrix


def createPrefixTree():
    root = Node("*")
    with codecs.open("sanalista.txt", encoding='utf-8') as wordFile:
        row = wordFile.readline()
        while row:
            word = re.search(r"<s>(.*?)<\/s>", row)[1]
            row = wordFile.readline()
            addNode(root, word.lower())

    return root


def getAllWords(lettersMatrix, rootNode):
    resultList = []
    for x in range(0, 4):
        for y in range(0, 4):
            recursiveWordSearch(
                (x, y), rootNode, lettersMatrix, "", [], resultList)
    return resultList


def recursiveWordSearch(coord, previousNode, lettersMatrix, wordSoFar, usedCoords, wordsFound):
    #print("Going to " + str(coord))
    currentLetter = lettersMatrix[coord[0]][coord[1]]
    foundChild = previousNode.findChildByChar(currentLetter)
    if not foundChild:
        return

    wordSoFarCopy = wordSoFar[:]
    wordSoFarCopy += currentLetter
    if foundChild.isWordFinished and wordSoFarCopy not in wordsFound:
        wordsFound.append(wordSoFarCopy)

    usedCoordsCopy = usedCoords.copy()
    usedCoordsCopy.append(coord)

    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            nextX = coord[0] + dx
            nextY = coord[1] + dy
            if nextX >= 0 and nextX <= 3 and nextY >= 0 and nextY <= 3:
                tupleCoords = (nextX, nextY)
                if tupleCoords not in usedCoordsCopy:
                    #print(str(tupleCoords) + " not in " + str(usedCoordsCopy))
                    recursiveWordSearch(
                        tupleCoords, foundChild, lettersMatrix, wordSoFarCopy, usedCoordsCopy, wordsFound)


def main():
    print("Creating tree")
    root = createPrefixTree()
    print("Prefix tree created")

    lettersMatrix = [[], [], [], []]
    command = input("Input letters: ").lower()
    while len(command) == 16:
        start = time.time()
        lettersMatrix = makeLettersMatrix(command)
        allWords = getAllWords(lettersMatrix, root)
        mid = time.time()
        allWords.sort(key=len)
        print("------------------------")
        for w in allWords:
            print(w)
        end = time.time()
        print("Algorithm took " + str(mid-start) +
              " and with sort + print whole process took " + str(end-start))
        command = input("Input letters: ")


main()
