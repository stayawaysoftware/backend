class Game:
    """ Game Class that represents a Game Match 
        Attributes:
            gameId (int): The id of the Match inherited from Room Class id (Must be the same).
            name (str): The name of the Match inherited from Room Class name (Must be the same).
            userIds (list): List of Players ids in the game inherited from Room Class.
            playerQuantity(int): How much players are in the match. (This can be inherited from Room Class)
            roundDirection(bool): In which direction the round goes (0 left. 1 right).
            actualPhase(str): The actual phase in the turn.
            actualTurn(int): The position that has the actual turn.
            decks(Deck): Decks of the game.
        Methods:
            for each attribute exists a get/set method with exception at the attributes "id", "gameId",
            "userIds" and "playerQuantity" because we don't want to modify that attributes in the match.

            get_attributeName(): returns the attribute "attributeName"
            set_attributeName(): sets a new value for "attributeName"
            nextTurn(): Changes the current turn to the next one.
            endGame():  Ends the actual game.
            checkVictory(): Checks who win the match.
            dealingStartingCards(): Deals the initial cards to the players

        note: Decks will be implemented soon.

    """ 

    def __init__(self, gameId: int, name: str, userIds: list[int], playerQuantity: int, roundDirection: bool, actualPhase: str,
                    actualTurn: int):
        """ Game Class constructor """
        self.gameId = game_id
        self.name = name
        self.userIds = user_ids
        self.playerQuantity = player_quantity
        self.roundDirection = round_direction
        self.actualPhase = actual_phase
        self.actualTurn = actual_turn

    
    def get_gameId(self):
        """ Returns the match ID """
        return self.gameId

    def get_name(self):
        """ Returns the match name """
        return self.name

    def get_userIds(self):
        """Returns the list of players id"""
        return self.userIds
    
    def get_playerQuantity(self):
        """Returns the players quantity"""
        return self.playerQuantity

    def set_playerQuantity(self, newQuant: int):
        """Sets the players quantity"""
        self.playerQuantity = newQuant
    
    def get_roundDirection(self):
        """Returns the round direction"""
        return self.roundDirection
    
    def set_roundDirection(self, newDirection: bool):
        """Sets the round direction"""
        self.roundDirection = newDirection

    def get_actualPhase(self):
        """Returns the actual phase"""
        return actualPhase

    def set_actualPhase(self, newPhase: str):
        """Sets a new phase"""
        self.actualPhase = newPhase

    def get_actualTurn(self):
        """Returns the actual player turn"""
        return self.actualTurn 

    def set_actualTurn(self, newTurn: int):
        """Sets a new player turn"""
        self.actualTurn = newTurn

    
    def nextTurn(self):
        """Changes the current turn to the next one."""
        pass

    def endGame(self):
        """Ends the actual game."""
        pass

    def checkVictory(self):
        """Checks who win the match"""
        pass

    def dealStartingCards(self):
        """Deals the initial cards to the players"""
        pass