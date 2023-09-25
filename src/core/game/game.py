class Game:
    """Game Class that represents a Game Match
    Attributes:
        game_id (int): The id of the Match inherited from Room Class id (Must be the same).
        name (str): The name of the Match inherited from Room Class name (Must be the same).
        user_ids (list): List of Players ids in the game inherited from Room Class.
        player_quantity(int): How much players are in the match. (This can be inherited from Room Class)
        round_direction(bool): In which direction the round goes (0 left. 1 right).
        actual_phase(str): The actual phase in the turn.
        actual_turn(int): The position that has the actual turn.
        decks(Deck): Decks of the game.
    Methods:
        for each attribute exists a get/set method with exception at the attributes "id", "gameId",
        "user_ids" because we don't want to modify that attributes in the match.

        get_attributeName(): returns the attribute "attributeName"
        set_attributeName(): sets a new value for "attributeName"
        diminish_player_quantity(self):Substracts 1 to player_quantity.
        set_round_direction(self): Sets the round direction to the opposite direction.
        next_turn(): Changes the current turn to the next one.
        end_game():  Ends the actual game.
        check_victory(): Checks who win the match.
        dealing_starting_cards(): Deals the initial cards to the players

    note: Decks will be implemented soon.

    """

    def __init__(
        self,
        game_id: int,
        name: str,
        user_ids: list[int],
        player_quantity: int,
        round_direction: bool,
        actual_phase: str,
        actual_turn: int,
    ):
        """Game Class constructor"""
        self.game_id = game_id
        self.name = name
        self.user_ids = user_ids
        self.player_quantity = player_quantity
        self.round_direction = round_direction
        self.actual_phase = actual_phase
        self.actual_turn = actual_turn

    def get_game_id(self):
        """Returns the match ID"""
        return self.game_id

    def get_name(self):
        """Returns the match name"""
        return self.name

    def get_user_ids(self):
        """Returns the list of players id"""
        return self.user_ids

    def get_player_quantity(self):
        """Returns the players quantity"""
        return self.player_quantity

    def diminish_player_quantity(self):
        """Substracts 1 to player_quantity"""
        if self.player.quantity >= 1:
            self.player_quantity -= 1

    def get_round_direction(self):
        """Returns the round direction"""
        return self.round_direction

    def set_round_direction(self):
        """Sets the round direction to the opposite direction"""
        self.round_direction = not self.round_direction

    def get_actual_phase(self):
        """Returns the actual phase"""
        return self.actual_phase

    def set_actual_phase(self, newPhase: str):
        """Sets a new phase"""
        self.actual_phase = newPhase

    def get_actual_turn(self):
        """Returns the actual player turn"""
        return self.actual_turn

    def set_actual_turn(self, newTurn: int):
        """Sets a new player turn"""
        self.actual_turn = newTurn

    def next_turn(self):
        """Changes the current turn to the next one."""

    def end_game(self):
        """Ends the actual game."""

    def check_victory(self):
        """Checks who win the match"""

    def dealStartingCards(self):
        """Deals the initial cards to the players"""
