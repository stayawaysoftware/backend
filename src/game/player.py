
class Player:
    """ Player Class that represents a player in a Match 
        Attributes:
            id (int): The id of the player inherited from User Class id (Must be the same).
            name (str): The name of the player inherited from User Class name (Must be the same).
            id_game (int): The id of the player inherited from Room Class id (Must be the same).
            role (str): Player's role in the game.
            round_position (int): Player's position during the round.
            alive (bool): Player's status during the game.
            quarentined (bool): Player's status about quarentine effect.
    """

    def __init__(self, id: int, name: str, id_game: int, role: str, round_position: int, alive: bool=True,
                    quarantined: bool=False):
        """Constructor for Player class"""
        self.id = id
        self.name = name
        self.id_lobby = id_lobby
        self.role = role
        self.round_position = round_position
        self.alive = alive #Weird, why would I want this condition to be false?
        self.quarantined = quarantined

    
    def __str__(self):
        """String representation for Player Class"""
        return f"""User: {self.id},{self.name},{self.id_lobby},{self.role},{self.round_position},
                    {self.alive},{self.quarantined}"""

    def get_id(self):
        """Returns the player's id"""
        return self.id    

    def get_name(self):
        """Returns the player's name"""
        return self.name

    def set_name(self,newName: str):
        """Sets the player's name"""
        self.name = newName

    def get_id_lobby(self):
        """Returns the player's lobby id"""
        return self.id_lobby

    def get_role(self):
        """Returns the player's role"""
        return self.role

    def set_role(self, newRole: str):
        """Sets the player's role"""
        self.role = newRole

    def get_round_position(self):
        """Returns the player's round position"""
        return self.round_position

    def set_round_position(self, newPosition: int):
        """Sets the player's round position"""
        self.round_position = newPosition

    def get_alive(self):
        """Returns the player's alive status"""
        return self.alive
    
    def set_alive(self, newStatus: bool):
        """Sets the player's alive status"""
        self.alive = newStatus

    def get_quarentined(self):
        """Returns the player's quarentine status"""
        return self.quarantined
    
    def set_quarentined(self,newStatus: bool):
        """Sets the player's quarentine status"""
        self.quarantined = newStatus


    def DrawCard(self):
        """Draws a card from the deck."""
        pass

    def SwapCard(self):
        """Swap cards with another player."""
        pass

    def PlayCard(self):
        """Allows the player to play a card in the game."""
        pass

    def DiscardCard(self):
        """Allows the player to discard a card in the game."""
        pass
