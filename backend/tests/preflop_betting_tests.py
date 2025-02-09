import pytest
from models import *
from unittest.mock import AsyncMock
import pprint
import asyncio
import pytest_asyncio


async def get_hand_history(game_fix, monkeypatch, actions):
    test_mock = AsyncMock(side_effect=actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage="PREFLOP")
    hand_history = game_fix.get_hand_history()['PREFLOP']
    return hand_history


@pytest.mark.asyncio
async def test_player_make_bet(monkeypatch, player_list_fix, game_state_preflop_fix):
    
    actions = [
        {
            'sid' : player.sid,
            'amount_bet' : 40,
            'action' : "call"
        } for player in player_list_fix]    
    
    test_mock = AsyncMock(side_effect=actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)

    for i, player in enumerate(player_list_fix):
        old_funds = player.funds
        response = await player.make_bet(game_state_preflop_fix)
        assert response == actions[i]
        assert player.current_bet == actions[i]['amount_bet']
        assert old_funds - player.funds == actions[i]['amount_bet']

##################################################################################
##################################################################################
#### PREFLOP TESTS
##################################################################################
##################################################################################

@pytest.mark.asyncio
async def test_betting_round_1(monkeypatch, game_fix):
    '''
    Situation: All players call the big blind
    game_fix num_players=3 and sb_amount=20
    '''
    assert [player.get_id() for player in game_fix.players] == [1,2,3]

    actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]

    hand_history = await get_hand_history(game_fix, monkeypatch, actions)

    assert(len(hand_history)==3) # only three bets all call.

    assert(hand_history[0]['game_state']['pot'] == {'call_total' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 60})
    assert(hand_history[1]['game_state']['pot'] == {'call_total' : 40,'check_allowed' : False,'minimum_raise' : 80,'pot_size' : 100})
    assert(hand_history[2]['game_state']['pot'] == {'call_total' : 40,'check_allowed' : True,'minimum_raise' : 80,'pot_size' : 120})
    
    assert(hand_history[0]['response'] == {'action': 'call','amount_bet': 40,'sid': '3'})
    assert(hand_history[1]['response'] == {'action': 'call','amount_bet': 20,'sid': '1'})
    assert(hand_history[2]['response'] == {'action': 'check','amount_bet': 0,'sid': '2'})


@pytest.mark.asyncio
async def test_betting_round_2(monkeypatch, game_fix):
    '''
    Preflop stage
    history: P1 is sb pays 20, P2 is bb pays 40, P3 is other starts action
    Situation: single raise 
    '''
    # Situation:
    actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 80, 'action' : "raise"}, # P1 total 100
        {'sid' : '2', 'amount_bet' : 60, 'action' : "call"}, # P2 total 100
        {'sid' : '3', 'amount_bet' : 60, 'action' : "call"} # P3 total 100
    ]

    hand_history = await get_hand_history(game_fix, monkeypatch, actions)

    assert(len(hand_history)==4)
    # P3 saw this bellow and called 40
    assert(hand_history[0]['game_state']['pot'] == { "call_total" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 60})
    assert(hand_history[0]['player_state']['public_info']['pid'] == 3)
    assert(hand_history[0]['player_state']['public_info']['role'] == 'other')
    assert(hand_history[0]['player_state']['public_info']['funds'] == 960)
    assert(hand_history[0]['player_state']['public_info']['last_action'] == 'call')
    assert(hand_history[0]['player_state']['public_info']['current_bet'] == 40)

    # P1 saw this bellow and raised 80, total 100
    assert(hand_history[1]['game_state']['pot'] == {"call_total" : 40,"check_allowed" : False,"minimum_raise" : 80,"pot_size" : 100})
    assert(hand_history[1]['player_state']['public_info']['pid'] == 1)
    assert(hand_history[1]['player_state']['public_info']['role'] == 'sb')
    assert(hand_history[1]['player_state']['public_info']['funds'] == 900)
    assert(hand_history[1]['player_state']['public_info']['last_action'] == 'raise')
    assert(hand_history[1]['player_state']['public_info']['current_bet'] == 80)
    
    # P2 saw this bellow and called 60, total 100
    assert(hand_history[2]['game_state']['pot'] == {"call_total" : 100,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 180})
    assert(hand_history[2]['player_state']['public_info']['pid'] == 2)
    assert(hand_history[2]['player_state']['public_info']['role'] == 'bb')
    assert(hand_history[2]['player_state']['public_info']['funds'] == 900)
    assert(hand_history[2]['player_state']['public_info']['last_action'] == 'call')
    assert(hand_history[2]['player_state']['public_info']['current_bet'] == 60)

    # P3 calls his remainding 60
    assert(hand_history[3]['game_state']['pot'] == {"call_total" : 100,"check_allowed" : False,"minimum_raise" : 160,"pot_size" : 240})
    assert(hand_history[3]['player_state']['public_info']['pid'] == 3)
    assert(hand_history[3]['player_state']['public_info']['role'] == 'other')
    assert(hand_history[3]['player_state']['public_info']['funds'] == 900)
    assert(hand_history[3]['player_state']['public_info']['last_action'] == 'call')
    assert(hand_history[3]['player_state']['public_info']['current_bet'] == 60)



@pytest.mark.asyncio
async def test_betting_round3(monkeypatch, game_fix):
    '''
    Situation: pre-flop stage, player folds. 
    '''
    # PREFLOP actions: P1 sb pays 20, P2 bb pays 40, P3 other starts action
    actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"}, 
        {'sid' : '2', 'amount_bet' : 0, 'action' : "fold"},
    ]

    hand_history = await get_hand_history(game_fix, monkeypatch, actions)

    # pprint.pp(hand_history)
    assert(len(hand_history)==3)
    
    # P2 folds
    assert(hand_history[2]['player_state']['public_info']['pid'] == 2)
    assert(hand_history[2]['player_state']['public_info']['role'] == 'bb')
    assert(hand_history[2]['player_state']['public_info']['funds'] == 960)
    assert(hand_history[2]['player_state']['public_info']['last_action'] == 'fold')
    assert(hand_history[2]['player_state']['public_info']['current_bet'] == 0)

@pytest.mark.asyncio
async def test_betting_round_4(monkeypatch, game_fix):
    '''
    Situation: pre-flop stage, player goes all-in. 
    '''
    actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"}, 
        {'sid' : '2', 'amount_bet' : 960, 'action' : "all-in"},
        {'sid' : '3', 'amount_bet' : 0, 'action' : "fold"},
        {'sid' : '1', 'amount_bet' : 960, 'action' : "all-in"},  ## all-in can be both a call and a raise.

    ]
    # with fold and call you should not have to specify, maybe we can worry about that in the frontend
    hand_history = await get_hand_history(game_fix, monkeypatch, actions)
    # pprint.pprint(hand_history)
    assert(len(hand_history)==5)


     # P2 all-in
    assert(hand_history[2]['player_state']['public_info']['pid'] == 2)
    assert(hand_history[2]['player_state']['public_info']['funds'] == 0)
    assert(hand_history[2]['player_state']['public_info']['last_action'] == 'all-in')
    assert(hand_history[2]['player_state']['public_info']['current_bet'] == 960)
    assert(hand_history[2]['player_state']['public_info']['bet_total'] == 1000)

    # P3 folds
    assert(hand_history[3]['game_state']['pot'] == {"call_total" : 1000,"check_allowed" : False,"minimum_raise" : 1920,"pot_size" : 1080})
    assert(hand_history[3]['player_state']['public_info']['pid'] == 3)
    assert(hand_history[3]['player_state']['public_info']['funds'] == 960)
    assert(hand_history[3]['player_state']['public_info']['last_action'] == 'fold')
    assert(hand_history[3]['player_state']['public_info']['current_bet'] == 0)
    assert(hand_history[3]['player_state']['public_info']['bet_total'] == 40)

    # P1 all-in
    assert(hand_history[4]['game_state']['pot'] == {"call_total" : 1000,"check_allowed" : False,"minimum_raise" : 1920,"pot_size" : 1080})
    assert(hand_history[4]['player_state']['public_info']['pid'] == 1)
    assert(hand_history[4]['player_state']['public_info']['funds'] == 0)
    assert(hand_history[4]['player_state']['public_info']['last_action'] == 'all-in')
    assert(hand_history[4]['player_state']['public_info']['current_bet'] == 960)
    assert(hand_history[4]['player_state']['public_info']['bet_total'] == 1000)












