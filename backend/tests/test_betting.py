import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot
from unittest.mock import Mock, AsyncMock
from typing import List# Tuple
import pprint
import asyncio

###### @TODO Test every function in every module!!!

def get_player_actions(actions : list[tuple[str,int]]) -> List[PlayerBetResponse]:
    player_actions = []
    '''
    Assume three players, Actions go in modular sequence ie P1, P2, P3, P1, P2, P3,...
    ex actions = [('call', 20), ('raise',40), ('call', 40), ('call', 20)]
    Returns List[PlayerBetResponses] from simplified list of tuples
    '''
    for i, a in enumerate(actions):
        pid = (i%3)+1
        _, action, amount = a
        player_actions.append(PlayerBetResponse(pid=pid, player_funds=50, action = action, amount_bet=amount))

    return player_actions


@pytest.mark.asyncio
async def test_betting_round_1(monkeypatch, game_fix):
    '''
    Situation: All players call
    Preflop stage, no checking allowed.
    game_fix num_players=3 and sb_amount=20
    '''
    actions = [('P1','call', 40), ('P2','call',40), ('P3','call', 40)] # @TODO the calling amount should not need to be input by players
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)   ## @TODO I'm thinking we will need asyncio.gather()
    hand_history = game_fix.get_hand_history()['PREFLOP'] # This is the thing

    assert(len(hand_history)==3) # only three bets all call.

    # These represent the state player i sees before performing his action !!!
    assert(hand_history[0]['game_state']['pot'] == {'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 0})
    assert(hand_history[1]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 40})
    assert(hand_history[2]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 80})
    
    assert(hand_history[0]['response'] == {'action': 'call','amount_bet': 40,'pid': 1,'player_funds': 50})
    assert(hand_history[1]['response'] == {'action': 'call','amount_bet': 40,'pid': 2,'player_funds': 50})
    assert(hand_history[2]['response'] == {'action': 'call','amount_bet': 40,'pid': 3,'player_funds': 50})


@pytest.mark.asyncio
async def test_betting_round_2(monkeypatch, game_fix):
    '''
    Preflop stage, no checking allowed.
    Situation: single raise. Call amounts should update. 
    '''
    # Situation:
    actions = [('P1','call', 40), ('P2','raise',80), ('P3','call', 80), ('P1','call', 40), ('P2','check',0), ('P3','check', 0)]
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)

    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    hand_history = game_fix.get_hand_history()['PREFLOP']

    # pprint.pp(hand_history)
    assert(len(hand_history)==6)
    # These represent the state player i sees before performing his action !!!
    # P1 sees this bellow and calls 40
    assert(hand_history[0]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 0})
    # P2 sees this bellow and raises 80
    assert(hand_history[1]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 40})
    # P3 sees this bellow and calls 80
    assert(hand_history[2]['game_state']['pot'] == {"call_amount" : 80,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 120})
    # P1 calls his remainding 40
    assert(hand_history[3]['game_state']['pot'] == {"call_amount" : 40,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 200})


@pytest.mark.asyncio
async def test_betting_round3(monkeypatch, game_fix):
    '''
    Situation: flop stage, check allowed, multiple raises. 
    '''
    actions_preflop = [('P1','call', 40), ('P2','raise',80), ('P3','call', 80), ('P1','call', 40), ('P2','check',0), ('P3','check', 0)]
    actions_flop = [('P1','check', 0), ('P2','raise',100), ('P3','raise', 200), ('P1','call', 200), ('P2','call', 100), ('P3','check', 0)]
    test_mock = AsyncMock(side_effect=get_player_actions(actions_preflop+actions_flop))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)

    # Preflop
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    # FLOP actions:
    flop_initial_conditions = {
      "call_amount" : 0,
      "check_allowed" : True,
      "minimum_raise" : 80,
      "pot_size" : 240,
    }

    # test_mock = AsyncMock(side_effect=get_player_actions(actions))
    # monkeypatch.setattr(Player, "request_betting_response", test_mock) # NEW mocked method!!!!!
    await game_fix.betting_round(BoardStage.FLOP)
    hand_history = game_fix.get_hand_history()['FLOP']

    assert(len(hand_history)==6) # 5 moves total... gotta wait for EVERYONE
    # P1 sees this bellow and checks
    assert(hand_history[0]['game_state']['pot'] == flop_initial_conditions)
    # P2 sees this bellow and raises 100
    assert(hand_history[1]['game_state']['pot'] == flop_initial_conditions)
    ## P3 sees this bellow and raises 200
    assert(hand_history[2]['game_state']['pot'] == {'call_amount': 100,'check_allowed' : False,'minimum_raise' : 200,'pot_size' : 340})
    ## P1 sees this bellow and calls 200
    assert(hand_history[3]['game_state']['pot'] == {"call_amount" : 200,"check_allowed" : False,"minimum_raise" : 400,"pot_size" : 540})
    ## P2 Calls with 100
    assert(hand_history[4]['game_state']['pot'] == {"call_amount" : 100,   "check_allowed" : False,"minimum_raise" : 400,"pot_size" : 740})

    
@pytest.mark.asyncio
async def test_betting_round4(monkeypatch, game_fix):
    '''
    Situation: pre-flop stage, player folds. 
    '''
    # PREFLOP actions:
    actions = [('P1','call',40), ('P2','raise',80), ('P3','fold',0), ('P1','raise',160), ('P2','call',120)] # P3 actually not allowed to check   
    # with fold and call you should not have to specify, maybe we can worry about that in the frontend
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    
    hand_history = game_fix.get_hand_history()['PREFLOP']

    assert(len(hand_history)==5)

    assert(hand_history[0]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 0}) # P1 sees
    assert(hand_history[1]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 40}) # P2 sees
    assert(hand_history[2]['game_state']['pot']=={'call_amount' : 80,'check_allowed' : False,'minimum_raise' : 160,'pot_size' : 120}) # P3 sees
    assert(hand_history[3]['game_state']['pot']=={'call_amount' : 40,'check_allowed' : False,'minimum_raise' : 160,'pot_size' : 120}) # P1 sees
    assert(hand_history[4]['game_state']['pot']=={'call_amount' : 120,'check_allowed' : False,'minimum_raise' : 320,'pot_size' : 280}) # P2 sees


# # @TODO test validation of call amounts and minimum raises. 
# # Test blind taxes in preflop round, they should not be able to fold
# # Test all-in 

@pytest.mark.asyncio
async def test_betting_round_5(monkeypatch, game_fix):
    '''
    Situation: pre-flop stage, player goes all-in. 
    '''
    actions = [('P1','call',40), ('P2','call',40), ('P3','all-in',5000), ('P1','fold',0), ('P2','all-in',4960)] # P3 actually not allowed to check   
    # with fold and call you should not have to specify, maybe we can worry about that in the frontend
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)
    hand_history = game_fix.get_hand_history()['PREFLOP']
    pprint.pprint(hand_history)
    assert(len(hand_history)==5)









