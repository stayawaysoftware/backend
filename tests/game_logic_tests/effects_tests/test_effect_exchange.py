"""Test exchange effect."""
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

# ============================ EXCHANGE EFFECT ============================


class TestExchange:
    """Tests for exchange effect."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

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

        # draw_specific(id_game=1, id_player=1, idtype_card=1)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=1, idtype_card=1)
        discard(id_game=1, id_player=1, idtype_card=2)
        discard(id_game=1, id_player=1, idtype_card=3)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()


# ================================= EXCHANGE / SEDUCTION (WITH DEFENSE) =================================

# TERRIFYING


class TestTerrifying:
    """Test Terrifying effect."""

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
            "players": [
                self.get_player_data(player.id) for player in game.players
            ],
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

        draw_specific(id_game=1, id_player=1, idtype_card=3)
        draw_specific(id_game=1, id_player=2, idtype_card=4)

        draw_specific(id_game=1, id_player=2, idtype_card=14)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=1, idtype_card=3)
        discard(id_game=1, id_player=2, idtype_card=4)
        discard(id_game=1, id_player=2, idtype_card=14)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_terrifying_effect(self):
        """Test Terrifying effect."""
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=32,
            idtype_defense_card=14,
            card_chosen_by_attacker=3,
        )

        # Without modifications in the game and players
        assert game_data == self.get_game_data(id_game=1)

        # With message to front
        card_id = Player[1].hand.select(idtype=3).first().id

        assert effect == {
            "type": "show_card",
            "player_name": Player[1].name,
            "target": [2],
            "cards": [{"id": card_id, "idtype": 3}],
        }

    @db_session
    def test_terrifying_effect_with_dead_attaker(self):
        """Test Terrifying effect with dead attacker."""
        Player[1].alive = False
        commit()

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=14,
                card_chosen_by_attacker=3,
            )

    @db_session
    def test_terrifying_effect_with_dead_defender(self):
        """Test Terrifying effect with dead defender."""
        Player[2].alive = False
        commit()

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=14,
                card_chosen_by_attacker=3,
            )


# NO, THANKS


class TestNoThanks:
    """Test No Thanks effect."""

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
            "players": [
                self.get_player_data(player.id) for player in game.players
            ],
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

        draw_specific(id_game=1, id_player=2, idtype_card=15)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=2, idtype_card=15)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_no_thanks_effect(self):
        """Test No Thanks effect."""
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=32,
            idtype_defense_card=15,
        )

        # Without message to front
        assert effect is None

        # Without modifications in the game and players
        assert game_data == self.get_game_data(id_game=1)

    @db_session
    def test_no_thanks_effect_with_dead_player(self):
        """Test No Thanks effect with dead player."""
        Player[2].alive = False
        commit()

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=15,
            )


# YOU FAILED


class TestYouFailed:
    """Test You Failed effect."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        clean_db()

    @classmethod
    def teardown_class(cls):
        """Teardown class."""
        clean_db()

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

        # draw_specific(id_game=1, id_player=1, idtype_card=1)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        discard(id_game=1, id_player=1, idtype_card=1)
        discard(id_game=1, id_player=1, idtype_card=2)
        discard(id_game=1, id_player=1, idtype_card=3)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()
