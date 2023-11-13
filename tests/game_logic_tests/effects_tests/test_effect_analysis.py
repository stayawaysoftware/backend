"""Test analysis effect."""
import pytest

from . import clean_db
from . import commit
from . import db_session
from . import Deck
from . import delete_decks
from . import discard
from . import draw_specific
from . import Game
from . import initialize_decks
from . import play
from . import Player

# ================================= ANALYSIS =================================


class TestAnalysisEffect:
    """Test Analysis effect."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

    @db_session
    def get_player_data(self, id_player: int):
        """Get player data."""
        player = Player[id_player]
        player_data = {
            "id": player.id,
            "role": player.role,
            "name": player.name,
            "round_position": player.round_position,
            "alive": player.alive,
            "game": player.game.id,
            "hand": [card.id for card in player.hand],
        }

        return player_data

    @db_session
    def get_game_data(self, id_game: int):
        """Get game data."""
        game = Game[id_game]
        game_data = {
            "id": game.id,
            "round_left_direction": game.round_left_direction,
            "status": game.status,
            "current_phase": game.current_phase,
            "current_position": game.current_position,
            "winners": game.winners,
            "players": sorted(
                (self.get_player_data(player.id) for player in game.players),
                key=lambda player: player["id"],
            ),
            "deck": game.deck.id,
        }

        return game_data

    @db_session
    def setup_method(self):
        """Setup method."""
        initialize_decks(id_game=1, quantity_players=12)
        Game(id=1, current_phase="Defense", deck=Deck[1])
        for i in range(1, 13):
            Player(
                id=i,
                name=f"Player{i}",
                round_position=i,
                game=Game[1],
                alive=True,
            )

        draw_specific(id_game=1, id_player=1, idtype_card=4)

        draw_specific(id_game=1, id_player=2, idtype_card=1)
        draw_specific(id_game=1, id_player=2, idtype_card=2)
        draw_specific(id_game=1, id_player=2, idtype_card=3)
        draw_specific(id_game=1, id_player=2, idtype_card=12)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=1, idtype_card=4)

        discard(id_game=1, id_player=2, idtype_card=1)
        discard(id_game=1, id_player=2, idtype_card=2)
        discard(id_game=1, id_player=2, idtype_card=3)
        discard(id_game=1, id_player=2, idtype_card=12)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_analysis_effect(self):
        """Test analysis effect."""
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=4,
            idtype_defense_card=0,
        )

        # With message to front
        card_list_to_show = [
            {"id": card.id, "idtype": card.idtype} for card in Player[2].hand
        ]

        assert effect == {
            "type": "show_card",
            "player_name": Player[2].name,
            "target": [1],
            "cards": card_list_to_show,
        }

        # Without modifications in the game and players
        assert game_data == self.get_game_data(id_game=1)

    @db_session
    def test_analysis_effect_with_dead_player(self):
        """Test analysis effect with dead player."""
        Player[2].alive = False
        commit()

        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=4,
                idtype_defense_card=0,
            )

    @db_session
    def test_analysis_effect_with_not_neighbor_player(self):
        """Test analysis effect with not neighbor player."""
        with pytest.raises(ValueError):
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=3,
                idtype_attack_card=4,
                idtype_defense_card=0,
            )
