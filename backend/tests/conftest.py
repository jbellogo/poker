'''
Contains fixtures which work as global variables for tests
Fixtures are passed as arguments to test functions
'''

import pytest
from models import *
import asyncio
import pytest_asyncio
import socketio
from unittest.mock import AsyncMock

from models.config import * # Global variables, better practice to use json.

## Testing global variables
_TESTING_SB_AMOUNT = 20
_TESTING_INITIAL_PLAYER_FUNDS = 1000
_TESTING_NUM_PLAYERS = 3




@pytest.fixture
def player_fix():
    return Player(name = "player1",
                  pid=0, 
                  sid = "sid1",
                  funds=_TESTING_INITIAL_PLAYER_FUNDS)

@pytest.fixture
def deck_fix():
    return Deck()
    
@pytest.fixture
def board_fix():
    return Board()

@pytest.fixture
def player_list_fix():
    players = [Player(name = f"player{i}",
                    pid = i, 
                    sid = f"sid{i}",
                    funds=_TESTING_INITIAL_PLAYER_FUNDS) for i in range(1,_TESTING_NUM_PLAYERS+1)]
    players[0].set_role(PlayerRole.SMALL_BLIND)
    players[1].set_role(PlayerRole.BIG_BLIND)
    return players


@pytest.fixture
def game_fix(player_list_fix):
    game = Game(sb_amount=_TESTING_SB_AMOUNT,
                initial_player_funds=_TESTING_INITIAL_PLAYER_FUNDS)
    for player in player_list_fix:
        game.add_player(player.sid, player.name)
    game.initialize_hand() # after adding players @TODO add some guards/lobby, game is not initialized until players > 2
    return game

@pytest.fixture
def hand_fix():
    return [Card(suit=Suit.HEARTS, rank=Rank.TWO), Card(suit=Suit.HEARTS, rank=Rank.THREE)]


@pytest_asyncio.fixture
async def game_fix_flop(monkeypatch, player_list_fix):
    game = Game(sb_amount=_TESTING_SB_AMOUNT,
                initial_player_funds=_TESTING_INITIAL_PLAYER_FUNDS)
    for player in player_list_fix:
        game.add_player(player.sid, player.name)
    game.initialize_hand() # after adding players @TODO add some guards/lobby, game is not initialized until players > 2
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    monkeypatch.setattr(Player, "request_betting_response", AsyncMock(side_effect=preflop_actions))
    await game.betting_round("PREFLOP")
    yield game


async def get_hand_history(game_fix, monkeypatch, actions, board_stage : BoardStage):
    '''
    takes in actions in form of [{'sid' : '3', 'amount_bet' : 40, 'action' : "call"},...]
    mocks the request_betting_response method for the Player class with the actions
    returns the hand history for the PREFLOP stage
    '''
    assert(board_stage in ["PREFLOP", "FLOP", "TURN", "RIVER"])
    test_mock = AsyncMock(side_effect=actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage)
    hand_history = game_fix.get_hand_history()[board_stage]
    return hand_history
