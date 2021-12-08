import string
import copy
import random

def randomNameGen():
    return (random.choice(string.ascii_uppercase) + \
            random.choice(['a', 'e', 'i', 'o', 'u']) + \
            random.choice(['a', 'e', 'i', 'o', 'u']))

class Game(object):
    def __init__(self):
        self.state = None

    def startGame(self):
        raise NotImplementedError

    def actions(self):
        raise NotImplementedError

    def transition(self, action):
        raise NotImplementedError

    def gameOver(self):
        raise NotImplementedError

class BoardGame(Game):
    def displayState(self):
        raise NotImplementedError

    def displayGameEnd(self):
        raise NotImplementedError

    def playGame(self, players):
        """
        Overrides Game.playGame()

        """
        self.startGame()
        turn = 0

        move = None
        while not self.gameOver():
            self.displayState(players)
            player = players[turn % len(players)]
            move = player.play(self.state, self.actions())
            if self.transition(move):
                turn += 1
        self.displayGameEnd(players)


class Player(object):
    def __init__(self, name=None):
        if name is None:
            self.name = randomNameGen()
        else:
            self.name = name

class HumanPlayer(Player):
    def __init__(self, name=None):
        super(HumanPlayer, self).__init__(name)

    def play(self, state, actions):
        while True:
            move = raw_input(self.name + ", please enter a move: ")
            if move not in actions:
                print("That move is not available. Try again!")
            else:
                return move

class RandomShotsPlayer(Player):
    def __init__(self, name=None):
        super(RandomShotsPlayer, self).__init__(name)

    def play(self, state, actions):
        return random.choice(actions)


#
# BattleShip
#
# State:
# 2 10x10 boards
#   Per Square:
#    0 - for no ship
#    1 - for ship portion
#    2 - for ship portion that has been hit
#    3 - for shot that did not hit a ship
#
# 2 lists recording each player's moves
#
# 2 aim positions
#

class Battleship(BoardGame):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.moves = ['up', 'down', 'left', 'right', 'fire']

    def getGuesses(self):
        return [self.state[0][1], self.state[1][1]]

    def getTurn(self):
        stateGuesses = self.getGuesses()
        numGuesses = sum(len(guesses) for guesses in stateGuesses)
        turn = numGuesses % 2
        return turn

    def getAim(self):
        turn = self.getTurn()
        return self.state[turn][2]

    def startGame(self):
        """
        Overrides Game.startGame()

        """
        board = [[0 for i in range(self.width)] for j in range(self.height)]
        boardCopy = copy.deepcopy(board)
        board = self.placeShips(board)
        boardCopy = self.placeShips(boardCopy)
        self.state = [[board, [], [0, 0]], [boardCopy, [], [0, 0]]]

    def actions(self):
        """
        Overrides Game.actions()

        """
        return self.moves

    def transition(self, action):
        """
        Overrides Game.transition()

        """
        stateGuesses = self.getGuesses()
        turn = self.getTurn()
        aimX, aimY = self.getAim()

        makeTransition = False

        if action == 'up':
            aimY = max(0, aimY - 1)
        elif action == 'down':
            aimY = min(self.height - 1, aimY + 1)
        elif action == 'left':
            aimX = max(0, aimX - 1)
        elif action == 'right':
            aimX = min(self.width - 1, aimX + 1)
        elif action == 'fire':
            makeTransition = True
        else:
            raise Exception('Invalid move: {}'.format(action))

        if makeTransition:
            # Update guesses
            stateGuesses[turn].append(action)

            # Update board
            opTurn = (turn + 1) % 2
            opBoard = self.state[opTurn][0]

            print(aimY, aimX)
            curPos = opBoard[aimY][aimX]

            if curPos == 0:
                opBoard[aimY][aimX] = 3
            elif curPos == 1:
                opBoard[aimY][aimX] = 2
            else:
                return False

            self.state[0][1] = stateGuesses[0]
            self.state[1][1] = stateGuesses[1]

            self.state[opTurn][0] = opBoard
        else:
            self.state[turn][2] = [aimX, aimY]

        return makeTransition

    def gameOver(self):
        """
        Overrides Game.gameOver()

        """
        boards = (self.state[0][0], self.state[1][0])

        for player, board in enumerate(boards):
            totalHit = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == 2:
                        totalHit += 1
            if totalHit == 17:
                self.winner = (player + 1) % 2
                return True
        return False

    def checkAvailable(self, board, posX, posY):
        boundsX = (0 <= posX) and (posX < self.width)
        boundsY = (0 <= posY) and (posY < self.height)
        if not (boundsX and boundsY):
            return False

        return board[posY][posX] != 1

    def placeShip(self, board, shipSize):
        width = self.width
        height = self.height

        while True:
            orientation = random.randint(0, 3)
            posX = random.randint(0, width - 1)
            posY = random.randint(0, height - 1)
            boardCopy = copy.deepcopy(board)

            canPlace = True
            if orientation == 0:
                for i in range(shipSize):
                    canPlace = self.checkAvailable(boardCopy, posX + i, posY)
                    if canPlace:
                        boardCopy[posY][posX + i] = 1
                    else:
                        break
            elif orientation == 1:
                for i in range(shipSize):
                    canPlace = self.checkAvailable(boardCopy, posX, posY + i)
                    if canPlace:
                        boardCopy[posY + i][posX] = 1
                    else:
                        break
            elif orientation == 2:
                for i in range(shipSize):
                    canPlace = self.checkAvailable(boardCopy, posX, posY - i)
                    if canPlace:
                        boardCopy[posY - i][posX] = 1
                    else:
                        break
            if orientation == 3:
                for i in range(shipSize):
                    canPlace = self.checkAvailable(boardCopy, posX - i, posY)
                    if canPlace:
                        boardCopy[posY][posX - i] = 1
                    else:
                        break
            if canPlace:
                return boardCopy
    def placeShips(self, board):
        shipSizes = [5, 4, 3, 3, 2]
        for shipSize in shipSizes:
            board = self.placeShip(board, shipSize)
        return board

    def displayGameEnd(self, players):
        """
        Overrides BoardGame.displayGameEnd()

        """
        print("The winner is " + players[self.winner].name)

    def displayState(self, players):
        """
        Overrides BoardGame.displayState()

        """
        opDisplayMap = {
            0: " ",
            1: " ",
            2: "X",
            3: "O"
        }

        displayMap = {
            0: " ",
            1: "*",
            2: "X",
            3: "O"
        }

        turn = self.getTurn()
        board = self.state[turn][0]

        opTurn = (turn + 1) % 2
        opBoard = self.state[opTurn][0]

        boardDisp = players[opTurn].name + str("\n")
        head = " |"
        for i in range(1, self.width + 1):
            head += str(i) + "|"
        head += "\n"
        rowSep = "-" * 2 * (self.width + 1) + "\n"

        boardDisp += head + rowSep

        alphabet = string.ascii_uppercase
        for i in range(self.height):
            row = alphabet[i] + "|"
            for j in range(self.width):
                row += opDisplayMap[opBoard[i][j]] + "|"
            row += "\n"
            boardDisp += row + rowSep

        opTurn = (opTurn + 1) % 2
        boardDisp += "\n"
        boardDisp += players[opTurn].name + str("\n")
        boardDisp += head + rowSep
        for i in range(self.height):
            row = alphabet[i] + "|"
            for j in range(self.width):
                row += displayMap[board[i][j]] + "|"
            row += "\n"
            boardDisp += row + rowSep
        print(boardDisp)

if __name__ == "__main__":
    battleship = Battleship(10, 10)
    players = [RandomShotsPlayer(), RandomShotsPlayer()]
    battleship.playGame(players)
