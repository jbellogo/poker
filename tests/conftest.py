'''
Contains fixtures which work as global variables for tests
Fixtures are passed as arguments to test functions
'''

import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot, PotState

BIG_BLIND = 20
INITIAL_PLAYER_FUNDS = 50

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
    pot = Pot(bb_amount = BIG_BLIND, players = player_list_fix)
    return pot

@pytest.fixture
def pot_fix_flop(player_list_fix):
    '''For betting tests'''
    # I just want to set potstate
    new_pot_state = PotState({
        'call_amount': 0,
        'check_allowed' : True,
        'minimum_raise' : 100,
        'pot_size' : 1000
    })
    pot = Pot(bb_amount = BIG_BLIND, players = player_list_fix)
    pot.overwrite_pot_state(new_pot_state)
    return pot



# @pytest.fixture
# def player_actions(actions : list[tuple[str,int]]):
#     player_actions_lst = []
#     '''
#     Assume three players, Actions go in modular order ie P1, P2, P3, P1, P2, P3,...
#     ex actions = [('call', 20), ('raise',40), ('call', 40), ('call', 20)]
#     '''
#     for i in range(0,4):
#         pid = (i%3)+1
#         action, amount = actions[i]
#         player_actions_lst.append(PlayerBetResponse(pid=pid, player_funds=50, action = action, amount_bet=amount))

#     return player_actions_lst

