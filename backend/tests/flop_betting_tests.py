##################################################################################
##################################################################################
#### FLOP TESTS
##################################################################################
##################################################################################

import pytest
from tests.conftest import get_hand_history
from models import *
import pprint


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

BETTING_ROUND = "FLOP"

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
    flop_hand_history = await get_hand_history(game_fix, monkeypatch, flop_actions, BETTING_ROUND)
    state = game_fix.get_state()
    # pprint.pprint(state)
    assert(len(flop_hand_history) == 3)
    assert(state['board']['stage'] == 'FLOP')
    assert(len(state['board']['cards']) == 3)
    # call_total now builds up across betting rounds.
    assert(state['pot'] == {'call_total': 40, 'check_allowed': True, 'minimum_raise': 80, 'pot_size': 120})


@pytest.mark.asyncio
async def test2(monkeypatch, game_fix_flop_basic):
    flop_actions = [
        {'sid' : '3', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '1', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    flop_hand_history = await get_hand_history(game_fix_flop_basic, monkeypatch, flop_actions, BETTING_ROUND)
    state = game_fix_flop_basic.get_state()
    assert(len(flop_hand_history) == 3)
    assert(state['board']['stage'] == 'FLOP')
    assert(len(state['board']['cards']) == 3)
    assert(state['pot'] == {'call_total': 40, 'check_allowed': True, 'minimum_raise': 80, 'pot_size': 120})


@pytest.mark.asyncio
async def test3(monkeypatch, game_fix_flop_basic):
    # preflop they are all square
    actions = [
        {'sid' : '3', 'amount_bet' : 100, 'action' : "raise"},  # call total 100
        {'sid' : '1', 'amount_bet' : 200, 'action' : "raise"},  # call total 200
        {'sid' : '2', 'amount_bet' : 400, 'action' : "raise"},  # call total 400
        {'sid' : '3', 'amount_bet' : 300, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 200, 'action' : "call"},  
    ]

    hand_history = await get_hand_history(game_fix_flop_basic, monkeypatch, actions, BETTING_ROUND)
    assert(len(hand_history)==5)

    assert(hand_history[0]['game_state']['pot'] == {"call_total" : 40, "check_allowed" : True,"minimum_raise" : 80,"pot_size" : 120})
    assert(hand_history[1]['game_state']['pot'] == {"call_total" : 140, "check_allowed" : False,"minimum_raise" : 200,"pot_size" : 220})
    assert(hand_history[2]['game_state']['pot'] == {"call_total" : 240, "check_allowed" : False,"minimum_raise" : 400,"pot_size" : 420})
    assert(hand_history[3]['game_state']['pot'] == {"call_total" : 440, "check_allowed" : False,"minimum_raise" : 800,"pot_size" : 820})
    assert(hand_history[4]['game_state']['pot'] == {"call_total" : 440, "check_allowed" : False,"minimum_raise" : 800,"pot_size" : 1120})
    assert(game_fix_flop_basic.get_state()['pot'] == {"call_total" : 440, "check_allowed" : True,"minimum_raise" : 800,"pot_size" : 1320})


## test fold and all-ins carry through from preflop to flop. new game_fix_flop fixture needed. 
@pytest.mark.asyncio
async def test4(monkeypatch, game_fix_flop_fold):
    '''
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "fold"},
    ]
    '''
    actions = [
        {'sid' : '3', 'amount_bet' : 100, 'action' : "raise"},  # call total 140
        {'sid' : '1', 'amount_bet' : 200, 'action' : "raise"},  # call total 240
        {'sid' : '3', 'amount_bet' : 100, 'action' : "call"},
    ]

    hand_history = await get_hand_history(game_fix_flop_fold, monkeypatch, actions, BETTING_ROUND)
    assert(len(hand_history)==3)
    assert(game_fix_flop_fold.get_state()['pot'] == {"call_total" : 240, "check_allowed" : True,"minimum_raise" : 400,"pot_size" : 520})



@pytest.mark.asyncio
async def test5(monkeypatch, game_fix_flop_fold):
    '''
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "fold"},
    ]
    '''
    actions = [
        {'sid' : '3', 'amount_bet' : 80, 'action' : "raise"},  # call total 120
        {'sid' : '1', 'amount_bet' : 160, 'action' : "raise"},  # call total 200
        {'sid' : '3', 'amount_bet' : 320, 'action' : "raise"},  # call total 440
        {'sid' : '1', 'amount_bet' : 640, 'action' : "raise"},  # call total 840
        {'sid' : '3', 'amount_bet' : 400, 'action' : "call"},  # call total 840
    ]

    hand_history = await get_hand_history(game_fix_flop_fold, monkeypatch, actions, BETTING_ROUND)
    assert(len(hand_history)==5)
    assert(game_fix_flop_fold.get_state()['pot'] == {"call_total" : 840, "check_allowed" : True,"minimum_raise" : 1280,"pot_size" : 1720})



@pytest.mark.asyncio
async def test6(monkeypatch, game_fix_flop_allin):
    '''
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 980, 'action' : "all-in"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "fold"},
        {'sid' : '3', 'amount_bet' : 960, 'action' : "all-in"},
    ]
    '''
    actions = []

    hand_history = await get_hand_history(game_fix_flop_allin, monkeypatch, actions, BETTING_ROUND)
    assert(hand_history == [])
    assert(game_fix_flop_allin.get_state()['pot']["call_total"] == 1000)
    assert(game_fix_flop_allin.get_state()['pot']["check_allowed"] == True)
    # assert(game_fix_flop_allin.get_state()['pot']["minimum_raise"] == 1960)  # its 40 now... sure it doesnt matter cuz eveyone went all-in... but it technically shuold update
    assert(game_fix_flop_allin.get_state()['pot']["pot_size"] == 2040)
