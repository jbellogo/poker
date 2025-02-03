'''
Contains fixtures which work as global variables for tests
Fixtures are passed as arguments to test functions
'''

import pytest
from models import *
import asyncio
import pytest_asyncio
import socketio

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


# @pytest.fixture
# def server_fix():
#     return sio

@pytest.fixture
def game_fix(player_list_fix):
    # sio = socketio.Server(cors_allowed_origins='*')
    # app = socketio.WSGIApp(sio)

    game = Game(sb_amount=_TESTING_SB_AMOUNT,
                initial_player_funds=_TESTING_INITIAL_PLAYER_FUNDS)
    for player in player_list_fix:
        game.add_player(player.sid, player.name)
    
    return game  # Use yield instead of return
    # Cleanup after the test
    # sio.disconnect()  # Disconnect all clients
    # sio.stop()

@pytest.fixture
def hand_fix():
    return [Card(suit=Suit.HEARTS, rank=Rank.TWO), Card(suit=Suit.HEARTS, rank=Rank.THREE)]


@pytest.fixture
def game_state_preflop_fix():
    pot = PotState(call_amount=40, check_allowed=False, minimum_raise=80, pot_size=0)
    board = BoardState(cards=[], stage=BoardStage.PREFLOP)
    return GameState(pot=pot, board=board)