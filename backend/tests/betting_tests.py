import pytest
from models import *
from unittest.mock import AsyncMock
import pprint
import asyncio
import pytest_asyncio

from tests.conftest import _TESTING_INITIAL_PLAYER_FUNDS

###### @TODO Test every function in every module!!!



# @pytest.mark.asyncio
# async def test_player_make_bet(monkeypatch, player_list_fix, game_state_preflop_fix):
#     actions = [
#         {
#             'sid' : player.sid,
#             'amount_bet' : 40,
#             'action' : "call"
#         } for player in player_list_fix]
#     # pprint.pprint(actions)
    
#     test_mock = AsyncMock(side_effect=actions)
#     monkeypatch.setattr(Player, "request_betting_response", test_mock)
#     for i, player in enumerate(player_list_fix):
#         old_funds = player.funds
#         response = await player.make_bet(game_state_preflop_fix)
#         assert response == actions[i]
#         assert player.current_bet == actions[i]['amount_bet']
#         assert old_funds - player.funds == actions[i]['amount_bet']
#         assert player.betting_status == PlayerAction(actions[i]['action']).to_status()
#     # print("test_player_make_bet passed")

# PREFLOP TESTS

@pytest.mark.asyncio
async def test_betting_round_1(monkeypatch, game_fix):
    '''
    Situation: All players call
    Preflop stage, no checking allowed.
    game_fix num_players=3 and sb_amount=20
    '''
    assert game_fix.get_players() == [1,2,3]
    assert game_fix.get_sb_index() == 0
    actions = [{
        'sid' : '1',
        'amount_bet' : 40,
        'action' : "call",
    },
    {
        'sid' : '2',
        'amount_bet' : 40,
        'action' : "call",
    },
    {
        'sid' : '3',
        'amount_bet' : 40,
        'action' : "call",
    }]

    test_mock = AsyncMock(side_effect=actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)   ## @TODO I'm thinking we will need asyncio.gather()
    hand_history = game_fix.get_hand_history()['PREFLOP']
    assert(len(hand_history)==3) # only three bets all call.

    # These represent the state player i sees before performing his action !!!
    assert(hand_history[0]['game_state']['pot'] == {'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 0})
    assert(hand_history[1]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 40})
    assert(hand_history[2]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 80})
    
    assert(hand_history[0]['response'] == {'action': 'call','amount_bet': 40,'sid': '1'})
    assert(hand_history[1]['response'] == {'action': 'call','amount_bet': 40,'sid': '2'})
    assert(hand_history[2]['response'] == {'action': 'call','amount_bet': 40,'sid': '3'})


@pytest.mark.asyncio
async def test_betting_round_2(monkeypatch, game_fix):
    '''
    Preflop stage, no checking allowed.
    Situation: single raise. Call amounts should update. 
    '''
    # Situation:
    actions = [{
        'sid' : '1',
        'amount_bet' : 40,
        'action' : "call",
    },
    {
        'sid' : '2',
        'amount_bet' : 80,
        'action' : "raise",
    },
    {
        'sid' : '3',
        'amount_bet' : 80,
        'action' : "call",
    },
    {
        'sid' : '1',
        'amount_bet' : 40,
        'action' : "call",
    },
    {
        'sid' : '2',
        'amount_bet' : 0,
        'action' : "check",
    },
    {
        'sid' : '3',
        'amount_bet' : 0,
        'action' : "check",
    }]

    test_mock = AsyncMock(side_effect=actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    hand_history = game_fix.get_hand_history()['PREFLOP']

    pprint.pp(hand_history)
    assert(len(hand_history)==6)
    # P1 sees this bellow and calls 40
    assert(hand_history[0]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 0})
    # P2 sees this bellow and raises 80
    assert(hand_history[1]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 40})
    # P3 sees this bellow and calls 80
    assert(hand_history[2]['game_state']['pot'] == {"call_amount" : 80,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 120})
    # P1 calls his remainding 40
    assert(hand_history[3]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 200})
    # P2 sees this bellow and checks    
    assert(hand_history[4]['game_state']['pot'] == {"call_amount" : 0,"check_allowed" : True,"minimum_raise" : 160,"pot_size" : 240})
    # P3 sees this bellow and checks
    assert(hand_history[5]['game_state']['pot'] == {"call_amount" : 0,"check_allowed" : True,"minimum_raise" : 160,"pot_size" : 240})


# @pytest.mark.asyncio
# async def test_betting_round3(monkeypatch, game_fix):
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
#       "call_amount" : 0,
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
#     assert(hand_history[2]['game_state']['pot'] == {'call_amount': 100,'check_allowed' : False,'minimum_raise' : 200,'pot_size' : 340})
#     ## P1 sees this bellow and calls 200
#     assert(hand_history[3]['game_state']['pot'] == {"call_amount" : 200,"check_allowed" : False,"minimum_raise" : 400,"pot_size" : 540})
#     ## P2 Calls with 100
#     assert(hand_history[4]['game_state']['pot'] == {"call_amount" : 100,   "check_allowed" : False,"minimum_raise" : 400,"pot_size" : 740})

    
# @pytest.mark.asyncio
# async def test_betting_round4(monkeypatch, game_fix):
#     '''
#     Situation: pre-flop stage, player folds. 
#     '''
#     # PREFLOP actions:
#     actions = [('P1','call',40), ('P2','raise',80), ('P3','fold',0), ('P1','raise',160), ('P2','call',120)] # P3 actually not allowed to check   
#     # with fold and call you should not have to specify, maybe we can worry about that in the frontend
#     test_mock = AsyncMock(side_effect=get_player_actions(actions))
#     monkeypatch.setattr(Player, "request_betting_response", test_mock)
#     await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    
#     hand_history = game_fix.get_hand_history()['PREFLOP']

#     assert(len(hand_history)==5)

#     assert(hand_history[0]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 0}) # P1 sees
#     assert(hand_history[1]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 40}) # P2 sees
#     assert(hand_history[2]['game_state']['pot']=={'call_amount' : 80,'check_allowed' : False,'minimum_raise' : 160,'pot_size' : 120}) # P3 sees
#     assert(hand_history[3]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 160,'pot_size' : 120}) # P1 sees
#     assert(hand_history[4]['game_state']['pot']=={'call_amount' : 120,'check_allowed' : False,'minimum_raise' : 320,'pot_size' : 280}) # P2 sees


# # # @TODO test validation of call amounts and minimum raises. 
# # # Test blind taxes in preflop round, they should not be able to fold
# # # Test all-in 

# @pytest.mark.asyncio
# async def test_betting_round_5(monkeypatch, game_fix):
#     '''
#     Situation: pre-flop stage, player goes all-in. 
#     '''
#     actions = [('P1','call',40), ('P2','call',40), ('P3','all-in',5000), ('P1','fold',0), ('P2','all-in',4960)] # P3 actually not allowed to check   
#     # with fold and call you should not have to specify, maybe we can worry about that in the frontend
#     test_mock = AsyncMock(side_effect=get_player_actions(actions))
#     monkeypatch.setattr(Player, "request_betting_response", test_mock)
#     await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
#     hand_history = game_fix.get_hand_history()['PREFLOP']
#     pprint.pprint(hand_history)
#     assert(len(hand_history)==5)









