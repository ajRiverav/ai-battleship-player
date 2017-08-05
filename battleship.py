import string
import copy
import random

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
        self.startGame()
        turn = 0

        move = None
        while not self.gameOver():
            self.displayState()
            player = players[turn % len(players)]
            move = player.play(self.state, self.actions())
            self.transition(move)
            turn += 1
        self.displayGameEnd()

class HumanPlayer(object):
    def play(self, state, actions):
        while True:
            move = raw_input("Please enter a move: ")
            if move not in actions:
                print("That move is not available. Try again!")
            else:
                return move

class RandomPlayer(object):
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

class Battleship(BoardGame):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_guesses(self):
        return [self.state[0][1], self.state[1][1]]

    def get_turn(self):
        state_guesses = self.get_guesses()
        num_guesses = sum(len(guesses) for guesses in state_guesses)
        turn = num_guesses % 2
        return turn

    def startGame(self):
        board = [[0 for i in range(self.width)] for j in range(self.height)]
        board_copy = copy.deepcopy(board)
        board = self.place_ships(board)
        board_copy = self.place_ships(board_copy)
        self.state = [[board, []], [board_copy, []]]

    def actions(self):
        state_guesses = self.get_guesses()
        turn = self.get_turn()
        turn_guesses = state_guesses[turn]

        alphabet = string.ascii_uppercase
        actions = []
        for l in alphabet[:self.height]:
            for n in range(1, self.width + 1):
                str_move = l + str(n)
                if str_move not in turn_guesses:
                    actions.append(str_move)

        return actions

    def transition(self, action):
        state_guesses = self.get_guesses()
        turn = self.get_turn()

        # Update guesses
        state_guesses[turn].append(action)
        self.state[0][1] = state_guesses[0]
        self.state[1][1] = state_guesses[1]

        # Update board
        op_turn = (turn + 1) % 2
        op_board = self.state[op_turn][0]

        action_y, action_x = action[0], action[1:]
        action_x = int(action_x) - 1
        action_y = ord(action_y) - ord('A')

        cur_pos = op_board[action_y][action_x]

        if cur_pos == 0:
            op_board[action_y][action_x] = 3
        elif cur_pos == 1:
            op_board[action_y][action_x] = 2
        else:
            raise Exception("invalid action")

        self.state[op_turn][0] = op_board

    def gameOver(self):
        boards = (self.state[0][0], self.state[1][0])

        for player, board in enumerate(boards):
            total_hit = 0
            for i in range(self.height):
                for j in range(self.width):
                    if board[i][j] == 2:
                        total_hit += 1
            if total_hit == 17:
                self.winner = (player + 1) % 2
                return True
        return False

    def check_available(self, board, pos_x, pos_y):
        bounds_x = (0 <= pos_x) and (pos_x < self.width)
        bounds_y = (0 <= pos_y) and (pos_y < self.height)
        if not (bounds_x and bounds_y):
            return False

        return board[pos_y][pos_x] != 1

    def place_ship(self, board, ship_size):
        width = self.width
        height = self.height

        while True:
            orientation = random.randint(0, 3)
            pos_x = random.randint(0, width - 1)
            pos_y = random.randint(0, height - 1)
            board_copy = copy.deepcopy(board)

            can_place = True
            if orientation == 0:
                for i in range(ship_size):
                    can_place = self.check_available(board_copy, pos_x + i, pos_y)
                    if can_place:
                        board_copy[pos_y][pos_x + i] = 1
                    else:
                        break
            elif orientation == 1:
                for i in range(ship_size):
                    can_place = self.check_available(board_copy, pos_x, pos_y + i)
                    if can_place:
                        board_copy[pos_y + i][pos_x] = 1
                    else:
                        break
            elif orientation == 2:
                for i in range(ship_size):
                    can_place = self.check_available(board_copy, pos_x, pos_y - i)
                    if can_place:
                        board_copy[pos_y - i][pos_x] = 1
                    else:
                        break
            if orientation == 3:
                for i in range(ship_size):
                    can_place = self.check_available(board_copy, pos_x - i, pos_y)
                    if can_place:
                        board_copy[pos_y][pos_x - i] = 1
                    else:
                        break
            if can_place:
                return board_copy
    def place_ships(self, board):
        ship_sizes = [5, 4, 3, 3, 2]
        for ship_size in ship_sizes:
            board = self.place_ship(board, ship_size)
        return board


    def displayGameEnd(self):
        winner = self.winner + 1
        print("The winner is {}".format(winner))

    def displayState(self):
        op_display_map = {
            0: " ",
            1: " ",
            2: "X",
            3: "O"
        }

        display_map = {
            0: " ",
            1: "*",
            2: "X",
            3: "O"
        }

        turn = self.get_turn()
        board = self.state[turn][0]

        op_turn = (turn + 1) % 2
        op_board = self.state[op_turn][0]

        board_disp = "Target board\n"
        head = " |"
        for i in range(1, self.width + 1):
            head += str(i) + "|"
        head += "\n"
        row_sep = "-" * 2 * (self.width + 1) + "\n"

        board_disp += head + row_sep

        alphabet = string.ascii_uppercase
        for i in range(self.height):
            row = alphabet[i] + "|"
            for j in range(self.width):
                row += op_display_map[op_board[i][j]] + "|"
            row += "\n"
            board_disp += row + row_sep

        board_disp += "\n"
        board_disp += "Your board\n"
        board_disp += head + row_sep
        for i in range(self.height):
            row = alphabet[i] + "|"
            for j in range(self.width):
                row += display_map[board[i][j]] + "|"
            row += "\n"
            board_disp += row + row_sep
        print(board_disp)

if __name__ == "__main__":
    battleship = Battleship(10, 10)
    players = [HumanPlayer(), HumanPlayer()]
    battleship.playGame(players)
