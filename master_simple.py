import random
import turtle as tt
import Eat.print
import math
import Eat.square as square
import Eat.neural_simple as neural_simple
import time

x_width = 25
y_width = 25
speed = 10  # lower the speed the faster the gameplay
METABOLISM = .25  # how much mass the player loses each tick

max_moss = 5


class Game:
    """
    the state of the game
    board (list of list of Squares) = the board
    character_x (int) = the x of the player in the board
    character_y = the y of the player in the board
    character_mass = the mass of the player

    """

    def __init__(self, board=False):
        """
        creates a Game
        :param board: if default, generates a Game
            if supplied, creates a copy of the board that is passed
        @TODO test if supplied
        """
        if not board:
            self.board = []
            self.create_board()
            self.biomize_board()
            self.character_x = 3
            self.character_y = 3
            self.character_mass = 5

            self.smooth_board()
            self.finish_board()
        else:
            self.board = []
            for x in range(len(board.board)):
                self.board.append([])
                for y in range(len(board.board[x])):
                    self.board.append(square.SquareDone(board.board[x][y].moss, board.board[x][y].moss))

            self.character_x = 3
            self.character_y = 3
            self.character_mass = 5

    def character_up(self):
        """
        tries to move the stored location of the player up
        """
        if self.character_y < y_width - 2:
            self.character_y += 1

    def character_down(self):
        """
        tries to move the stored location of the player down
        """

        if self.character_y > 0:
            self.character_y -= 1

    def character_right(self):
        """
        tries to move the stored location of the player right
        """
        if self.character_x < x_width - 2:
            self.character_x += 1

    def character_left(self):
        """
        tries to move the stored location of the player left
        """
        if self.character_x > 0:
            self.character_x -= 1

    def character_eat(self, food):
        """
        adds food to the player's mass
        :param food: the amount of food being added to the player
        """
        self.character_mass += food

    def character_tick(self):
        """
        does whatever needs to be done to the player's information at the end of each turn
        makes the player's mass go down by METABOLISM
        """
        self.character_mass -= METABOLISM

    def finish_board(self):
        """
        converts everything to a finalized object
        :return:
        """
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if isinstance(self.board[x][y], square.SquareBiome):
                    moss = self.smooth_biome_square(x, y)
                    self.board[x][y] = square.SquareDone(moss, moss)

                else:
                    self.board[x][y] = square.SquareDone(self.board[x][y].moss, self.board[x][y].moss)

    def smooth_biome_square(self, x, y):
        """
        averages the squares around x and y
        :param x: the x being averaged around
        :param y: the y being averaged around
        :return:
        """
        ans = 0
        divide_by = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and x + i >= 0 and y + j >= 0:
                    try:
                        ans += self.board[x + i][y + j].moss
                        divide_by += 1
                    except IndexError:
                        pass
        return ans / divide_by

    def smooth_board(self):
        """
        creates a moss level for each square
        :return: None
        """
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                self.smooth_square(x, y)

    def smooth_square(self, x, y):
        """
        figures out how much moss a square should have
        :param x: the x being smoothed
        :param y: the y being smoothed
        :return: how much moss a square should have
        """
        moss = []
        weight = []
        care_distance = 9
        # null_weight = 1
        if not isinstance(self.board[x][y], square.SquareBiome):

            for i in range(-care_distance, care_distance):

                for j in range(-care_distance, care_distance):
                    # compute the distance from x,y to x+i,y+j
                    try:
                        if isinstance(self.board[x + i][y + j], square.SquareBiome):
                            moss.append(self.board[x + i][y + j].biome)
                            distance = int(math.sqrt(i * i + j * j) + 1)
                            weight.append((1 / math.log10(distance)))

                    except (IndexError):
                        pass

            expected_moss = .0002
            weight_reciprical = 0.001
            for i in range(len(moss)):
                expected_moss += moss[i] * weight[i]
                weight_reciprical += weight[i]
            expected_moss /= weight_reciprical
            self.board[x][y] = square.SquareMoss(expected_moss)

    def biomize_board(self):
        """
        puts biomes in the board
        :return: None
        """
        biome_tries = 200
        for biome in range(biome_tries):
            x = random.randrange(len(self.board))
            y = random.randrange(len(self.board[x]))

            if not self.is_next_to_biome(x, y):
                self.board[x][y] = square.SquareBiome()

    def is_next_to_biome(self, x, y):
        """
        checks if a given square is next to a biome
        :param x: the proposed x to be a new biome
        :param y: the proposed y to be a new biome
        :return: True if square is next to a biome
        """
        distance_to_check = 3

        for i in range(-distance_to_check, distance_to_check + 1):
            for j in range(-distance_to_check, distance_to_check + 1):
                x_at = x + i
                y_at = y + j
                if 0 <= x_at < len(self.board) and 0 <= y_at < len(self.board[x_at]) and \
                        isinstance(self.board[x_at][y_at], square.SquareBiome):
                    return True
        return False

    def create_board(self):
        """
        creates a board of unfinshed squares
        :return: None
        """
        square.SquareDone.max_moss = max_moss
        for x in range(x_width):
            self.board.append([])
            for y in range(y_width):
                self.board[x].append(square.SquareUnfinished())

    def visible(self, sight=8):
        """
        finds the board around the player
        :return: the board around the player
        """
        visible = []
        for x in range(-sight, sight + 1):
            visible.append([])
            for y in range(-sight, sight + 1):
                if self.character_x + x < 0 or self.character_y + y < 0:
                    visible[x + sight].append(None)
                else:
                    try:
                        visible[x + sight].append(self.board[self.character_x + x][self.character_y + y])
                    except IndexError:
                        visible[x + sight].append(None)

        return visible

    def eat(self):
        """
        subtracts moss from under the player
        :return: the moss subtracted from under the player
        """
        moss = self.board[self.character_x][self.character_y].moss / speed
        self.board[self.character_x][self.character_y].moss -= moss
        return moss

    def turn(self, choice):
        """
        execute the command decided by the player
        :param choice: the choice the user made (wasd)
        :return:
        """
        if choice == 'w':
            self.character_up()
        elif choice == 'a':
            self.character_left()
        elif choice == 's':
            self.character_down()
        elif choice == 'd':
            self.character_right()
        else:
            self.character_eat(self.eat())
        self.tick()

    def tick(self):
        """
        calls tick on each square in the board
            makes each square's mass go up a bit
        calls tick on the character
            makes the player lose mass
        :return:
        """
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                self.board[x][y].tick(speed)
        self.character_tick()


class Human():
    """
    is a human decision getter
    """

    def __init__(self):
        """
        does nothing
        """
        pass

    def choice(self, visible):
        """
        gets a turn from a human
        :param visible: the map the human is allowed to see
        :return: the choice 'string'
        """
        Eat.print.print(visible)

        choice = input('move?')
        improper_answer = True
        while improper_answer:
            if choice == 'w' or choice == 'a' or choice == 's' or choice == 'd' or choice == 'x':
                improper_answer = False
                continue
            else:
                choice = input('move? (w/a/s/d/x')
        return choice


def see_play_game(player, game):
    """
    play a game with player and game
    displays the actions the player does
    :param player: the player playing the game
    :param game: the state of the game at the start
    :return: how long the player survived
    """
    tt.reset()
    Eat.print.initialize(game.board, max_moss * 1.1)
    turns = 0
    while game.character_mass > 0:
        turns += 1
        tt.reset()
        Eat.print.print(game.visible(), 30, game.character_mass)
        tt.update()
        game.turn(player.choice(game.visible(Eat.neural_simple.visible)))

    tt.update()

    return turns


def see_AI_play_game(player, game):
    """
    not compatible with a human player
    play a game with player and game
    displays the brain of the player and the decision making
    :param player: the player playing the game
    :param game: the state of the game at the start
    :return: how long the player survived
    """

    tt.reset()
    Eat.print.print_player(player)
    tt.update()
    turns = 0
    while game.character_mass > 0:
        turns += 1

        choice = Eat.print.print_choice(player, game.visible(Eat.neural_simple.visible))
        tt.update()
        print(choice, end='  ')
        game.turn(choice)
    print('')
    return turns


def play_game(player, game):
    """
    play a game with player and game
    does not create a visual
    :param player: the player playing the game
    :param game: the state of the game at the start
    :return: how long the player survived
    """
    turns = 0
    while game.character_mass > 0:
        turns += 1
        game.turn(player.choice(game.visible(Eat.neural_simple.visible)))

    tt.update()

    return turns


def main(show_AI = False):
    """

    :param show_AI:
    :return:
    """
    tt.bgcolor(0, 0, .25)
    # see_play_game(Human(), Game())

    players = []
    survival = []
    best_player = None
    if show_AI:
        for i in range(20):
            players.append(neural_simple.AI())
            tt.title(i)
            survival.append(see_AI_play_game(players[i], Game()))

        for round in range(300):
            best = 0
            highest = survival[0]
            for j in range(len(survival)):
                if survival[j] > highest:
                    best = j
                    highest = survival[j]
            best_player = players[best]
            players = []
            survival = []
            for j in range(20):
                tt.title(i)
                players.append(neural_simple.AI(best_player))
                survival.append(see_AI_play_game(players[j], Game()))
            best_player = players[best]
            tt.reset()
            Eat.print.print_player(best_player)
            time.sleep(1)

    if not show_AI:
        for i in range(20):
            players.append(neural_simple.AI())
            tt.title(i)
            survival.append(see_play_game(players[i], Game()))

        for round in range(300):
            best = 0
            highest = survival[0]
            for j in range(len(survival)):
                if survival[j] > highest:
                    best = j
                    highest = survival[j]
            best_player = players[best]
            players = []
            survival = []
            for j in range(20):
                tt.title(i)
                players.append(Eat.neural_simple.AI(best_player))
                survival.append(see_play_game(players[j], Game()))
            best_player = players[best]
            tt.reset()
            Eat.print.print_player(best_player)
            time.sleep(1)
    input()
    see_play_game(best_player, Game())
    Eat.print.print_player(best_player)


if __name__ == "__main__":
    tt.tracer(0, 0)
    # see_play_game(Human(),Game())
    main(False)
    tt.done()
