"""Containing my version of the tic tac toe game, 
which can be executed using the run() method of the class TicTacToeGame.

This contains the following classes:
- TicTacToeGame
- GameField
- Player
- Scoreboard

And the following global methods:
- clear_screen
- ask_yes_no
- ask_for_options
- ask_for_text
- ask_for_turn

"""

import os

# HELPER METHODS
def clear_screen():
    """Empties the console output
    """
    os.system("cls||clear")

def ask_yes_no(question: str) -> bool:
    """Asks the user for input and handles unexpected input.

    Args:
        question (str): Question for the user.

    Returns:
        bool: returns true if the user accepted, otherwise false.
    """
    response = input(f"{question}\ny for yes\nn for no\n")

    if response.lower() == "n":
        return False
    if response.lower() == "y":
        return True

    print(f"'{response}' is not a valid input. Try again.\n")
    return ask_yes_no(question)


def ask_for_options(question: str, options: dict) -> str:
    """Asks the user to choose between different options

    Args:
        question (str): Question for the user
        options (dict): Allowed input values

    Returns:
        str: Returns the supplied input
    """
    print(question)
    for key, value in options.items():
        print(f"\t{key} for {value}")

    choice = input("Your choice? ")

    if choice in options:
        return choice

    print(f"'{choice}' is not a valid input. Try again.\n")
    return ask_for_options(question, options)


def ask_for_text(question: str, min_length: int, forbidden_inputs: list = None) -> str:
    """Asks the user to input a string and validates the input against the specified minimum length

    Args:
        question (str): Question for the user
        min_length (int): Minimum length of expected inputs
        forbidden_inputs (list, optional): Disallowed inputs. Defaults to None.

    Returns:
        str: Returns the supplied input
    """
    if forbidden_inputs is None:
        forbidden_inputs = []

    response = input(f"{question} (At least {min_length} characters)\n")

    if len(response) < min_length:
        print(f"'{response}' is too short. Try again.\n")
        return ask_for_text(question, min_length)

    if response in forbidden_inputs:
        print(f"'{response}' is not allowed. Try again.\n")
        return ask_for_text(question, min_length)

    return response


def ask_for_turn(question: str, allowed_turns: list = None) -> int:
    """Asks the user to make a turn and returns the value if the turn is allowed

    Args:
        question (str): Question for the user
        allowed_turns (list, optional): A list of the allowed fields for the next turn. 
        Defaults to None.

    Returns:
        int: Returns the chosen
    """
    if allowed_turns is None:
        allowed_turns = []

    allowed = ", ".join(str(x) for x in allowed_turns)

    turn = input(f"{question} (Allowed fields: {allowed})\n").strip()

    if turn.isdigit() and int(turn) in allowed_turns:
        return int(turn)

    print(f"'{turn}' is not allowed. Try again.\n")
    return ask_for_turn(question, allowed_turns)


class TicTacToeGame:
    """Handles the tic tac toe game flow.
    """

    def __init__(self):
        self.__player_min_length = 2
        self.__scoreboard = None
        self.__game_field = None
        self.player_a = None
        self.player_b = None

    def run(self):
        """Runs the tic tac toe game
        """
        self.startup_and_configure()

        continue_game = True
        while continue_game:
            self.play_next_round()
            self.__scoreboard.print_state()

            if not ask_yes_no("\nDo you want to play another round?"):
                continue_game = False

    def startup_and_configure(self):
        """Startup logic of this game
        1. Greeting
        2. Choose mode (PvP or PvC)
        4. Set player name(s)
        5. Initialize components
        """

        game_modes = {
            "0" : "PvP (Player vs Player)",
            "1" : "PvC (Player vs Computer)"
        }

        clear_screen()
        print("Welcome to the tic tac toe game\n")
        game_mode_key = ask_for_options("Available game modes:", game_modes)

        player_1_name = ask_for_text(
            "\nWhat is the name of player 1?",
            min_length=self.__player_min_length
        )

        player_2_name = "Computer"

        if game_mode_key == "0":
            player_2_name = ask_for_text(
            "\nWhat is the name of player 1?",
            min_length=self.__player_min_length,
            forbidden_inputs=[player_1_name]
        )

        summary = f"\nSummary:\nGame mode: {game_modes[game_mode_key]}\n"
        summary += f"Player 1: {player_1_name}\n"
        if game_mode_key == "0":
            summary += f"Player 2: {player_2_name}\n"
        summary += "Are those values correct?"

        should_continue = ask_yes_no(summary)

        if not should_continue:
            if ask_yes_no("Do you want to quit?"):
                print("Exiting the game")
            else:
                print("Restarting the game\n\n")
                self.startup_and_configure()
            return

        print("\n\nConfiguring game...")
        print("Creating players...")
        self.player_a = Player(player_1_name, "X", False)
        self.player_b = Player(player_2_name, "O", game_mode_key == "1")

        print("Creating scoreboard...")
        self.__scoreboard = Scoreboard(self.player_a, self.player_b)

        print("Creating game field...")
        self.__game_field = GameField()
        print("Finished configuration\n")


    def play_next_round(self):
        """Handles the current round of the tic tac toe game.
        """
        self.__game_field.reset()
        players = [self.player_a, self.player_b]
        current_player_index = self.__scoreboard.who_starts()
        starting_player_key = players[current_player_index].key
        clear_screen()
        self.__game_field.print()

        while not self.__game_field.is_game_finished(self.player_a.key, self.player_b.key):
            current_player = players[current_player_index]
            if current_player.is_computer:
                print(f"It's the turn of {current_player.name}")
                turn_result = self.make_next_computer_turn("O", "X", starting_player_key)
            else:
                turn = ask_for_turn(
                    f"What is your next move {current_player.name}?",
                    self.__game_field.get_available_fields()
                )
                turn_result =  self.__game_field.try_make_turn(turn, current_player.key)

            if not turn_result:
                print("There was an error this turn.")
                print("Ending this round with a tie and starting again.")
                self.__scoreboard.increment_ties()
                return

            clear_screen()
            self.__game_field.print()

            current_player_index = (current_player_index + 1) % 2

        if self.__game_field.check_for_win(self.player_a.key):
            print(f"{self.player_a.name} won this round!")
            self.player_a.increment_score()
        elif self.__game_field.check_for_win(self.player_b.key):
            print(f"{self.player_b.name} won this round!")
            self.player_b.increment_score()
        else:
            print("It's a tie. Nobody wins")
            self.__scoreboard.increment_ties()


    def make_next_computer_turn(self, c_key: str, p_key: str, s_key: str) -> bool:
        """Checks the game field and decides how the next turn of the computer should be.

        Args:
            c_key (str): Mark of the computer; usually O
            p_key (str): Mark of the Player; usually X
            s_key (str): Mark of the starting player of the current round

        Returns:
            bool: returns if the turn was successful or not
        """
        middle = 5

        available_fields = self.__game_field.get_available_fields()
        taken_fields = self.__game_field.get_taken_fields()
        taken_by_opponent = taken_fields[p_key]
        own_fields = taken_fields[c_key]

        amount_of_taken_fields = len(taken_by_opponent) + len(own_fields)
        current_round = int(amount_of_taken_fields/2)

        if current_round == 0:
            if middle in available_fields:
                return self.__game_field.try_make_turn(middle, c_key)
            else:
                return self.__game_field.try_make_turn(1, c_key)

        if current_round == 1 and s_key == c_key:
            rows_to_scan = [[1, 2, 3], [7, 8, 9], [1, 4], [3, 6]]
            edges = [1, 3, 7, 9]

            for current_row in rows_to_scan:
                if taken_by_opponent[0] in current_row:
                    next_turn = [x for x in current_row if x in edges and x in available_fields][0]
                    return self.__game_field.try_make_turn(next_turn, c_key)

        rows_to_scan = [
            [1, 2, 3], [4, 5, 6], [7, 8, 9],
            [1, 4, 7], [2, 5 ,8], [3, 6, 9],
            [1, 5, 9], [3, 5, 7]
        ]

        # take win
        for row in rows_to_scan:
            ticked_in_row = [x for x in own_fields if x in row]
            free_in_row = [x for x in row if x in available_fields]
            if len(ticked_in_row) == 2 and len(free_in_row) == 1:
                return self.__game_field.try_make_turn(free_in_row[0], c_key)

        # defend
        for row in rows_to_scan:
            opponent_in_row = [x for x in taken_by_opponent if x in row]
            free_in_row = [x for x in row if x in available_fields]
            if len(opponent_in_row) == 2 and len(free_in_row) == 1:
                return self.__game_field.try_make_turn(free_in_row[0], c_key)

        # default get random
        return self.__game_field.try_make_turn(available_fields[0], c_key)


class GameField():
    """Represents the tic tac toe game field and its state
    """

    def __init__(self):
        self.__fields = {}

    def reset(self):
        """Resets the game field
        """
        self.__fields = {i: i+1 for i in range(9)}

    def get_available_fields(self):
        """Returns all fields which can be checked
        """
        return [value for (key, value) in self.__fields.items() if (key + 1) == value]

    def try_make_turn(self, field_name: int, field_value: str) -> bool:
        """Tries to make a turn.
        

        Args:
            field_name (int): The name of the current field
            field_value (str): The value which should be inserted to the field; usually X or O

        Returns:
            bool: If the field is already marked, the method returns false otherwise true.
        """
        field_id = field_name - 1
        if self.__fields[field_id] == field_name:
            self.__fields[field_id] = field_value
            return True
        return False

    def get_taken_fields(self):
        """Returns all taken fields

        Returns:
            dict: A dictionary containing a list with the ticked fields per player
        """
        return {
            "X":[x + 1 for x in self.__fields if self.__fields[x] == "X"],
            "O":[o + 1 for o in self.__fields if self.__fields[o] == "O"]
        }


    def print(self):
        """prints the current values to the console
        """
        for row in range(3):
            i = row * 3
            print(f" {self.__fields[i]} | {self.__fields[i + 1]} | {self.__fields[i + 2]}")
            if row < 2:
                print('-' * (4*3))
            else:
                print("\n")

    def is_game_finished(self, player_a: str, player_b: str) -> bool:
        """Checks if the game is finished.
        Which is the case when there are no remaining turns or if one of the players has won

        Args:
            player_a (str): Mark of player a
            player_b (str): Mark of player b

        Returns:
            bool: Returns true if the game is finished otherwise false
        """
        fields_without_values = self.get_available_fields()

        # are there remaining turns
        if len(fields_without_values) == 0:
            return True

        return self.check_for_win(player_a) or self.check_for_win(player_b)

    def check_for_win(self, player: str) -> bool:
        """Checks if the submitted player has won the game.

        Args:
            player (str): Mark of the player to check

        Returns:
            bool: Returns true if the player has won
        """
        # check horizontal win
        for row in range(3):
            row_start = row * 3
            if (
                self.__fields[row_start] == player and
                self.__fields[row_start + 1] == player and
                self.__fields[row_start + 2] == player
                ):
                return True

        # check vertical win
        for column in range(3):
            if (
                self.__fields[column] == player and
                self.__fields[column + 3] == player and
                self.__fields[column + 6] == player
                ):
                return True

        # check diagonal wins
        if (
            self.__fields[0] == player and
            self.__fields[4] == player and
            self.__fields[8] == player
            ):
            return True

        if (
            self.__fields[6] == player and
            self.__fields[4] == player and
            self.__fields[2] == player
            ):
            return True

        return False

class Player():
    """Represents a player of the tic tac toe game
    """
    def __init__(self, name: str, key: str, is_computer: bool):
        self.name = name
        self.key = key
        self.is_computer = is_computer
        self.__score = 0

    def increment_score(self):
        """Increments the score by 1
        """
        self.__score += 1

    def get_score(self) -> int:
        """Gets the amount of wins for the player object

        Returns:
            int: Returns amount of wins
        """
        return self.__score

class Scoreboard():
    """Represents the scoreboard of the tic tac toe game
    """

    def __init__(self, player_a: Player, player_b: Player):
        self.player_a = player_a
        self.player_b = player_b
        self.__amount_of_ties = 0

    def increment_ties(self):
        """Increments the ties by 1
        """
        self.__amount_of_ties += 1

    def who_starts(self) -> int:
        """Determines which player should start the next game

        Returns:
            int: Returns the index of the player which starts the next round
        """
        return (self.player_a.get_score() + self.player_b.get_score() + self.__amount_of_ties) % 2

    def print_state(self):
        """Prints the current score to the console
        """
        message = "\nCurrent score:\n"
        message += f"{self.player_a.name}: {self.player_a.get_score()}\n"
        message += f"{self.player_b.name}: {self.player_b.get_score()}\n"
        message += f"Ties: {self.__amount_of_ties}\n"

        print(message)
