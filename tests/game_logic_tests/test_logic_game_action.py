"""Test game_action module."""
from . import ActionType
from . import GameAction


class TestActionType:
    """Test ActionType enum."""

    def test_action_type(self):
        """Test ActionType enum."""
        assert str(ActionType.NOTHING) == "NOTHING"
        assert str(ActionType.ASK_DEFENSE) == "ASK_DEFENSE"
        assert str(ActionType.ASK_EXCHANGE) == "ASK_EXCHANGE"
        assert str(ActionType.EXCHANGE) == "EXCHANGE"
        assert str(ActionType.INFECT) == "INFECT"
        assert str(ActionType.KILL) == "KILL"
        assert str(ActionType.SHOW) == "SHOW"
        assert str(ActionType.SHOW_ALL) == "SHOW_ALL"
        assert str(ActionType.SHOW_ALL_TO_ALL) == "SHOW_ALL_TO_ALL"
        assert str(ActionType.REVERSE_ORDER) == "REVERSE_ORDER"
        assert str(ActionType.CHANGE_POSITION) == "CHANGE_POSITION"


class TestGameAction:
    """Test GameAction class."""

    def test_get_functions_and_initialization(self):
        """Test get functions and initialization."""

        action = GameAction(action=ActionType.NOTHING)
        assert action.get_action() == ActionType.NOTHING
        assert action.get_action2() is None
        assert action.get_target() is None
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(
            action=ActionType.ASK_DEFENSE, target=[1], defense_cards=[1, 2]
        )
        assert action.get_action() == ActionType.ASK_DEFENSE
        assert action.get_action2() is None
        assert action.get_target() == [1]
        assert action.get_defense_cards() == [1, 2]
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(
            action=ActionType.ASK_EXCHANGE,
            target=[1, 2],
            card_target=[1],
            exchange_phase=False,
        )
        assert action.get_action() == ActionType.ASK_EXCHANGE
        assert action.get_action2() is None
        assert action.get_target() == [1, 2]
        assert action.get_defense_cards() is None
        assert action.get_card_target() == [1]
        assert action.get_exchange_phase() is False

        action = GameAction(
            action=ActionType.EXCHANGE,
            target=[1, 2],
            card_target=[1, 2],
            exchange_phase=False,
        )
        assert action.get_action() == ActionType.EXCHANGE
        assert action.get_action2() is None
        assert action.get_target() == [1, 2]
        assert action.get_defense_cards() is None
        assert action.get_card_target() == [1, 2]
        assert action.get_exchange_phase() is False

        action = GameAction(
            action=ActionType.EXCHANGE,
            action2=ActionType.INFECT,
            target=[1, 2, 1],
            card_target=[1, 2],
            exchange_phase=False,
        )
        assert action.get_action() == ActionType.EXCHANGE
        assert action.get_action2() == ActionType.INFECT
        assert action.get_target() == [1, 2, 1]
        assert action.get_defense_cards() is None
        assert action.get_card_target() == [1, 2]
        assert action.get_exchange_phase() is False

        action = GameAction(action=ActionType.KILL, target=[1])
        assert action.get_action() == ActionType.KILL
        assert action.get_action2() is None
        assert action.get_target() == [1]
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(
            action=ActionType.SHOW, target=[1, 2], card_target=[1]
        )
        assert action.get_action() == ActionType.SHOW
        assert action.get_action2() is None
        assert action.get_target() == [1, 2]
        assert action.get_defense_cards() is None
        assert action.get_card_target() == [1]
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(action=ActionType.SHOW_ALL, target=[1, 2])
        assert action.get_action() == ActionType.SHOW_ALL
        assert action.get_action2() is None
        assert action.get_target() == [1, 2]
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(action=ActionType.SHOW_ALL_TO_ALL, target=[1])
        assert action.get_action() == ActionType.SHOW_ALL_TO_ALL
        assert action.get_action2() is None
        assert action.get_target() == [1]
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(action=ActionType.REVERSE_ORDER)
        assert action.get_action() == ActionType.REVERSE_ORDER
        assert action.get_action2() is None
        assert action.get_target() is None
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

        action = GameAction(action=ActionType.CHANGE_POSITION, target=[1, 2])
        assert action.get_action() == ActionType.CHANGE_POSITION
        assert action.get_action2() is None
        assert action.get_target() == [1, 2]
        assert action.get_defense_cards() is None
        assert action.get_card_target() is None
        assert (
            action.get_exchange_phase() is True
            and action.exchange_phase is None
        )

    def test_set_functions(self):
        """Test set functions."""

        action = GameAction(action=ActionType.NOTHING)
        action.set_action(ActionType.ASK_DEFENSE)
        assert action.get_action() == ActionType.ASK_DEFENSE
        action.set_action2(ActionType.INFECT)
        assert action.get_action2() == ActionType.INFECT
        action.set_target([1, 2])
        assert action.get_target() == [1, 2]
        action.set_defense_cards([1, 2])
        assert action.get_defense_cards() == [1, 2]
        action.set_card_target([1, 2])
        assert action.get_card_target() == [1, 2]
        action.set_exchange_phase(False)
        assert action.get_exchange_phase() is False

    def test_str(self):
        """Test str function."""

        action = GameAction(action=ActionType.NOTHING)
        assert (
            str(action)
            == "Action: NOTHING, Action2: None, Target: None, Defense cards: None, Card target: None, Exchange phase: None"
        )

        action = GameAction(
            action=ActionType.ASK_DEFENSE, target=[1], defense_cards=[1, 2]
        )
        assert (
            str(action)
            == "Action: ASK_DEFENSE, Action2: None, Target: [1], Defense cards: [1, 2], Card target: None, Exchange phase: None"
        )

        action = GameAction(
            action=ActionType.ASK_EXCHANGE, target=[1, 2], card_target=[1]
        )
        assert (
            str(action)
            == "Action: ASK_EXCHANGE, Action2: None, Target: [1, 2], Defense cards: None, Card target: [1], Exchange phase: None"
        )

        action = GameAction(
            action=ActionType.EXCHANGE,
            target=[1, 2],
            card_target=[1, 2],
            exchange_phase=False,
        )
        assert (
            str(action)
            == "Action: EXCHANGE, Action2: None, Target: [1, 2], Defense cards: None, Card target: [1, 2], Exchange phase: False"
        )

        action = GameAction(
            action=ActionType.EXCHANGE,
            action2=ActionType.INFECT,
            target=[1, 2, 1],
            card_target=[1, 2],
            exchange_phase=False,
        )
        assert (
            str(action)
            == "Action: EXCHANGE, Action2: INFECT, Target: [1, 2, 1], Defense cards: None, Card target: [1, 2], Exchange phase: False"
        )

        action = GameAction(action=ActionType.KILL, target=[1])
        assert (
            str(action)
            == "Action: KILL, Action2: None, Target: [1], Defense cards: None, Card target: None, Exchange phase: None"
        )

        action = GameAction(
            action=ActionType.SHOW, target=[1, 2], card_target=[1]
        )
        assert (
            str(action)
            == "Action: SHOW, Action2: None, Target: [1, 2], Defense cards: None, Card target: [1], Exchange phase: None"
        )

        action = GameAction(action=ActionType.SHOW_ALL, target=[1, 2])
        assert (
            str(action)
            == "Action: SHOW_ALL, Action2: None, Target: [1, 2], Defense cards: None, Card target: None, Exchange phase: None"
        )

        action = GameAction(action=ActionType.SHOW_ALL_TO_ALL, target=[1])
        assert (
            str(action)
            == "Action: SHOW_ALL_TO_ALL, Action2: None, Target: [1], Defense cards: None, Card target: None, Exchange phase: None"
        )

        action = GameAction(action=ActionType.REVERSE_ORDER)
        assert (
            str(action)
            == "Action: REVERSE_ORDER, Action2: None, Target: None, Defense cards: None, Card target: None, Exchange phase: None"
        )

        action = GameAction(action=ActionType.CHANGE_POSITION, target=[1, 2])
        assert (
            str(action)
            == "Action: CHANGE_POSITION, Action2: None, Target: [1, 2], Defense cards: None, Card target: None, Exchange phase: None"
        )
