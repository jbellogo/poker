'''
Contains fixtures which work as global variables for tests
Fixtures are passed as arguments to test functions
'''

import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot, PotState, Game
import asyncio
from aiohttp import ClientSession
import pytest_asyncio

BIG_BLIND = 20
INITIAL_PLAYER_FUNDS = 5000

@pytest.fixture
def player_fix():
    return Player(pid=0, funds=100)

@pytest.fixture
def deck_fix():
    return Deck()
    
@pytest.fixture
def board_fix():
    return Board()

@pytest.fixture
def player_list_fix():
    return [Player(pid = i, funds=INITIAL_PLAYER_FUNDS, betting_status = "active") for i in range(1,4)]

@pytest.fixture
def pot_fix_preflop(player_list_fix):
    '''For betting tests'''
    pot = Pot(bb_amount = BIG_BLIND)
    return pot

# @pytest.fixture
# def pot_fix_flop():
#     '''For betting tests'''
#     # I just want to set potstate
#     new_pot_state = PotState({
#         'call_amount': 0,
#         'check_allowed' : True,
#         'minimum_raise' : 100,
#         'pot_size' : 1000
#     })
#     pot = Pot(bb_amount = BIG_BLIND)
#     pot.overwrite_pot_state(new_pot_state)
#     return pot

FIX_NUM_PLAYERS =3
FIX_SB_AMOUNT = 20

@pytest.fixture
def game_fix():
    return Game(num_players=FIX_NUM_PLAYERS, sb_amount=FIX_SB_AMOUNT)
