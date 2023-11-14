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
from . import GameMessage
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
            "hand": sorted(card.id for card in player.hand),
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

        Player[1].role = "The Thing"

        draw_specific(id_game=1, id_player=1, idtype_card=1)
        draw_specific(id_game=1, id_player=1, idtype_card=2)
        draw_specific(id_game=1, id_player=1, idtype_card=3)
        draw_specific(id_game=1, id_player=1, idtype_card=4)

        Player[2].role = "Human"

        draw_specific(id_game=1, id_player=2, idtype_card=5)
        draw_specific(id_game=1, id_player=2, idtype_card=6)
        draw_specific(id_game=1, id_player=2, idtype_card=7)
        draw_specific(id_game=1, id_player=2, idtype_card=8)

        commit()

    @db_session
    def teardown_method(self):
        """Teardown method."""
        Game[1].current_phase = "Discard"
        for card in Player[1].hand:
            discard(id_game=1, id_player=1, idtype_card=card.idtype)
        for card in Player[2].hand:
            discard(id_game=1, id_player=2, idtype_card=card.idtype)

        delete_decks(id_game=1)
        Game[1].delete()
        for i in range(1, 13):
            Player[i].delete()
        commit()

    @db_session
    def test_exchange_effect_without_infection(self):
        """Test exchange effect without infection."""

        # Important data to testing
        card_chosen = [
            Player[1].hand.select(idtype=3).first().id,
            Player[2].hand.select(idtype=5).first().id,
        ]

        # Do the testing
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=32,
            idtype_defense_card=0,
            card_chosen_by_attacker=3,
            card_chosen_by_defender=5,
        )

        # Without message to front
        assert effect is None

        # With modifications in the game and players
        modified_game_data = self.get_game_data(id_game=1)

        assert modified_game_data != game_data

        # Check the cards in the hands
        assert (
            card_chosen[0] not in modified_game_data["players"][0]["hand"]
            and card_chosen[1] in modified_game_data["players"][0]["hand"]
        )
        assert (
            card_chosen[1] not in modified_game_data["players"][1]["hand"]
            and card_chosen[0] in modified_game_data["players"][1]["hand"]
        )

        # Check that this is the only modification

        for i in range(2):
            for j in range(0, len(modified_game_data["players"][i]["hand"])):
                if (
                    modified_game_data["players"][i]["hand"][j]
                    == card_chosen[1 - i]
                ):
                    modified_game_data["players"][i]["hand"][j] = card_chosen[
                        i
                    ]
                    break

        # Order the game_data cards to compare easily

        for i in range(12):
            list_for_game_data = list(modified_game_data["players"][i]["hand"])
            list_for_game_data.sort()

            modified_game_data["players"][i]["hand"] = list_for_game_data

        assert game_data == modified_game_data

    @db_session
    def test_exchange_effect_with_infection(self):
        """Test exchange effect with infection."""

        # Important data to testing
        card_chosen = [
            Player[1].hand.select(idtype=2).first().id,
            Player[2].hand.select(idtype=5).first().id,
        ]

        # Do the testing
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=32,
            idtype_defense_card=0,
            card_chosen_by_attacker=2,
            card_chosen_by_defender=5,
        )

        # Without message to front
        assert effect is None

        # With modifications in the game and players
        modified_game_data = self.get_game_data(id_game=1)

        assert modified_game_data != game_data

        # Check the cards in the hands
        assert (
            card_chosen[0] not in modified_game_data["players"][0]["hand"]
            and card_chosen[1] in modified_game_data["players"][0]["hand"]
        )
        assert (
            card_chosen[1] not in modified_game_data["players"][1]["hand"]
            and card_chosen[0] in modified_game_data["players"][1]["hand"]
        )

        # Check the infection
        assert (
            game_data["players"][1]["role"] == "Human"
            and modified_game_data["players"][1]["role"] == "Infected"
        )

        # Check that this is the only modification

        modified_game_data["players"][1]["role"] = "Human"

        for i in range(2):
            for j in range(0, len(modified_game_data["players"][i]["hand"])):
                if (
                    modified_game_data["players"][i]["hand"][j]
                    == card_chosen[1 - i]
                ):
                    modified_game_data["players"][i]["hand"][j] = card_chosen[
                        i
                    ]
                    break

        # Order the game_data cards to compare easily

        for i in range(12):
            list_for_game_data = list(modified_game_data["players"][i]["hand"])
            list_for_game_data.sort()

            modified_game_data["players"][i]["hand"] = list_for_game_data

        assert game_data == modified_game_data

    @db_session
    def test_exchange_effect_from_infected_to_the_thing(self):
        """Test exchange effect from infected to the thing."""

        # Important data to testing
        Player[2].role = "Infected"
        draw_specific(id_game=1, id_player=2, idtype_card=2)
        draw_specific(id_game=1, id_player=2, idtype_card=2)

        card_chosen = [
            min(card.id for card in Player[1].hand.select(idtype=3)),
            min(card.id for card in Player[2].hand.select(idtype=2)),
        ]

        # Do the testing
        game_data = self.get_game_data(id_game=1)

        effect = play(
            id_game=1,
            attack_player_id=1,
            defense_player_id=2,
            idtype_attack_card=32,
            idtype_defense_card=0,
            card_chosen_by_attacker=3,
            card_chosen_by_defender=2,
        )

        # Without message to front
        assert effect is None

        # With modifications in the game and players
        modified_game_data = self.get_game_data(id_game=1)

        assert modified_game_data != game_data

        # Check the cards in the hands
        assert (
            card_chosen[0] not in modified_game_data["players"][0]["hand"]
            and card_chosen[1] in modified_game_data["players"][0]["hand"]
        )
        assert (
            card_chosen[1] not in modified_game_data["players"][1]["hand"]
            and card_chosen[0] in modified_game_data["players"][1]["hand"]
        )

        # Check that this is the only modification

        for i in range(2):
            for j in range(0, len(modified_game_data["players"][i]["hand"])):
                if (
                    modified_game_data["players"][i]["hand"][j]
                    == card_chosen[1 - i]
                ):
                    modified_game_data["players"][i]["hand"][j] = card_chosen[
                        i
                    ]
                    break

        # Order the game_data cards to compare easily

        for i in range(12):
            list_for_game_data = list(modified_game_data["players"][i]["hand"])
            list_for_game_data.sort()

            modified_game_data["players"][i]["hand"] = list_for_game_data

        assert game_data == modified_game_data

    @db_session
    def test_exchange_effect_infected_between_both_sides(self):
        Player[2].role = "Infected"
        draw_specific(id_game=1, id_player=2, idtype_card=2)

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=2,
                card_chosen_by_defender=2,
            )

    @db_session
    def test_exchange_effect_infected_from_the_thing_to_infected(self):
        Player[2].role = "Infected"

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=2,
                card_chosen_by_defender=5,
            )

    @db_session
    def test_exchange_effect_infected_with_only_one_card(self):
        Player[2].role = "Infected"
        draw_specific(id_game=1, id_player=2, idtype_card=2)

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=3,
                card_chosen_by_defender=2,
            )

    @db_session
    def test_exchange_effect_with_dead_player(self):
        """Test exchange effect with dead player."""
        Player[2].alive = False
        commit()

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=3,
                card_chosen_by_defender=5,
            )

    @db_session
    def test_exchange_effect_with_not_neighbor_player(self):
        """Test exchange effect with not neighbor player."""
        Player[2].round_position = 3
        Player[3].round_position = 2
        commit()

        with pytest.raises(ValueError) as excinfo:
            play(
                id_game=1,
                attack_player_id=1,
                defense_player_id=2,
                idtype_attack_card=32,
                idtype_defense_card=0,
                card_chosen_by_attacker=3,
                card_chosen_by_defender=5,
            )


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

        message = GameMessage.create(
            type="show_card",
            room_id=1,
            quarantined=None,
            card_id=card_id,
            player_id=1,
            target_id=2,
        )

        assert effect == message

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
