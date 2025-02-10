import pytest
from tests.conftest import get_hand_history
from models import *
import pprint

##################################################################################
##################################################################################
#### FLOP TESTS
##################################################################################
##################################################################################

## The actions don't matter, just the state of the game after the preflop round
PREFLOP_STATE = {
    'pot': {
        'call_total': 40, 
        'check_allowed': True, 
        'minimum_raise': 80, 
        'pot_size': 120}, 
    'board': {
        'stage': 'PREFLOP', 
        'cards': []}
}

# def test_override_game_state(game_fix):
#     game_fix._override_game_state(PREFLOP_STATE)
#     state = game_fix.get_state()
#     assert(state == PREFLOP_STATE)


## test the transition from preflop to flop
@pytest.mark.asyncio
async def test1(monkeypatch, game_fix):
    '''test the transition from preflop to flop'''
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    preflop_hand_history = await get_hand_history(game_fix, monkeypatch, preflop_actions, "PREFLOP")
    state = game_fix.get_state()
    assert(state == PREFLOP_STATE)

    flop_actions = [
        {'sid' : '3', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '1', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    flop_hand_history = await get_hand_history(game_fix, monkeypatch, flop_actions, "FLOP")
    state = game_fix.get_state()
    # pprint.pprint(state)
    assert(len(flop_hand_history) == 3)
    assert(state['board']['stage'] == 'FLOP')
    assert(len(state['board']['cards']) == 3)
    # call_total now builds up across betting rounds.
    assert(state['pot'] == {'call_total': 40, 'check_allowed': True, 'minimum_raise': 80, 'pot_size': 120})


@pytest.mark.asyncio
async def test2(monkeypatch, game_fix_flop):
    flop_actions = [
        {'sid' : '3', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '1', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    flop_hand_history = await get_hand_history(game_fix_flop, monkeypatch, flop_actions, "FLOP")
    state = game_fix_flop.get_state()
    assert(len(flop_hand_history) == 3)
    assert(state['board']['stage'] == 'FLOP')
    assert(len(state['board']['cards']) == 3)
    assert(state['pot'] == {'call_total': 40, 'check_allowed': True, 'minimum_raise': 80, 'pot_size': 120})



# @pytest.mark.asyncio
# async def test_betting_round3(monkeypatch, game_fix, game_state_flop_fix):
#     game_fix._override_game_state = game_state_flop_fix
#     '''
#     Situation: flop stage, check allowed, multiple raises. 
#     '''
#     actions_preflop = [('P1','call', 40), ('P2','raise',80), ('P3','call', 80), ('P1','call', 40), ('P2','check',0), ('P3','check', 0)]
#     actions_flop = [('P1','check', 0), ('P2','raise',100), ('P3','raise', 200), ('P1','call', 200), ('P2','call', 100), ('P3','check', 0)]
#     test_mock = AsyncMock(side_effect=get_player_actions(actions_preflop+actions_flop))
#     monkeypatch.setattr(Player, "request_betting_response", test_mock)

#     # Preflop
#     await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
#     # FLOP actions:
#     flop_initial_conditions = {
#       "call_total" : 0,
#       "check_allowed" : True,
#       "minimum_raise" : 80,
#       "pot_size" : 240,
#     }

#     # test_mock = AsyncMock(side_effect=get_player_actions(actions))
#     # monkeypatch.setattr(Player, "request_betting_response", test_mock) # NEW mocked method!!!!!
#     await game_fix.betting_round(BoardStage.FLOP)
#     hand_history = game_fix.get_hand_history()['FLOP']

#     assert(len(hand_history)==6) # 5 moves total... gotta wait for EVERYONE
#     # P1 sees this bellow and checks
#     assert(hand_history[0]['game_state']['pot'] == flop_initial_conditions)
#     # P2 sees this bellow and raises 100
#     assert(hand_history[1]['game_state']['pot'] == flop_initial_conditions)
#     ## P3 sees this bellow and raises 200
#     assert(hand_history[2]['game_state']['pot'] == {'call_total': 100,'check_allowed' : False,'minimum_raise' : 200,'pot_size' : 340})
#     ## P1 sees this bellow and calls 200
#     assert(hand_history[3]['game_state']['pot'] == {"call_total" : 200,"check_allowed" : False,"minimum_raise" : 400,"pot_size" : 540})
#     ## P2 Calls with 100
#     assert(hand_history[4]['game_state']['pot'] == {"call_total" : 100,   "check_allowed" : False,"minimum_raise" : 400,"pot_size" : 740})

    

