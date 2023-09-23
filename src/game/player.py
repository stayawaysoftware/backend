
class Player:
    """ Player Class that represents a player in a Match """

    def __init__(self, id: int, name: str, id_lobby: int, role: str, round_position: int, alive: bool=True,
                    quarantined: bool=False, leftDoorBlocked: bool=False, rightDoorBlocked: bool=False):
        self.id = id
        self.name = name
        self.id_lobby = id_lobby
        self.role = role
        self.round_position = round_position
        self.alive = alive #Weird, why would I want this condition to be false?
        self.quarantined = quarantined
        self.leftDoorBlocked = leftDoorBlocked
        self.rightDoorBlocked = rightDoorBlocked

    def get_id(self):
        return self.id
    
    def set_id(self, newId: int):
        self.id = newId

    def get_name(self):
        return self.name

    def set_name(self,newName: str):
        self.name = newName

    def get_id_lobby(self):
        return self.id_lobby

    def set_id_lobby(self, newLobbyId: int):
        self.id_lobby = newLobbyId

    def get_role(self):
        return self.role

    def set_role(self, newRole: str):
        self.role = newRole

    def get_round_position(self):
        return self.round_position

    def set_round_position(self, newPosition: int):
        self.round_position = newPosition

    def get_alive(self):
        return self.alive
    
    def set_alive(self, newStatus: bool):
        self.alive = newStatus

    def get_quarentined(self):
        return self.quarantined
    
    def set_quarentined(self,newStatus: bool):
        self.quarantined = newStatus

    def get_leftDoorBlocked(self):
        return self.leftDoorBlocked
    
    def set_leftDoorBlocked(self, newStatus: bool):
        self.leftDoorBlocked = newStatus

    def get_rightDoorBlocked(self):
        return self.rightDoorBlocked
    
    def set_rigntDoorBlocked(self, newStatus: bool):
        self.rightDoorBlocked = newStatus


    