'''
Contains fixtures which work as global variables for tests
Fixtures are passed as arguments to test functions
'''

import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot

BIG_BLIND = 20

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
    return [Player(pid = i, funds=50, current_hand_betting_status = "active") for i in range(1,4)]

@pytest.fixture
def pot_fix(player_list_fix):
    '''
    this is a ficture because a list of players is used in a lot of tests
    '''
    pot = Pot(bb_amount = BIG_BLIND, players = player_list_fix)
    return pot

