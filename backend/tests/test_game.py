import pytest
import pprint

from typing import List

from models import *
from tests.conftest import get_hand_history
from unittest.mock import AsyncMock


# def test_update_player_turns_basic(game_fix):
#     players = list(range(1, NUM_PLAYERS+1))

#     assert(game_fix.get_sb_index()==0)
#     assert(game_fix.get_players() == players)

#     game_fix.update_player_turns()

#     assert(game_fix.get_sb_index()==1)
#     updated_players = players[1:] + players[:1]

#     assert(game_fix.get_players() == updated_players)

#     game_fix.update_player_turns()

#     assert(game_fix.get_sb_index()==2)
#     updated_players = players[2:] + players[:2]

#     assert(game_fix.get_players() == updated_players)


# def test_update_player_turns_modular(game_fix):
#     '''Tests that after all players have been sb, it is the turn of the first sb again.'''
#     players = list(range(1, NUM_PLAYERS+1))
#     assert(game_fix.get_sb_index()==0)
#     assert(game_fix.get_players() == players)

#     for _ in range(NUM_PLAYERS):
#         game_fix.update_player_turns()
    
#     assert(game_fix.get_sb_index()==0)
#     assert(game_fix.get_players() == players)



@pytest.mark.asyncio
async def test_hand(game_fix, monkeypatch):
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    flop_actions = [
        {'sid' : '3', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '1', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    turn_actions = flop_actions
    river_actions = flop_actions

    preflop_history = await get_hand_history(game_fix, monkeypatch, preflop_actions, "PREFLOP")
    assert(game_fix.get_state()['board']['stage'] == "PREFLOP")
    assert(len(game_fix.get_state()['board']['cards']) == 0)
    assert(game_fix.get_state()['pot']['pot_size'] == 120)
    flop_history = await get_hand_history(game_fix, monkeypatch, flop_actions, "FLOP")
    assert(game_fix.get_state()['board']['stage'] == "FLOP")
    assert(len(game_fix.get_state()['board']['cards']) == 3)
    assert(game_fix.get_state()['pot']['pot_size'] == 120)
    turn_history = await get_hand_history(game_fix, monkeypatch, turn_actions, "TURN")
    assert(game_fix.get_state()['board']['stage'] == "TURN")
    assert(len(game_fix.get_state()['board']['cards']) == 4)
    assert(game_fix.get_state()['pot']['pot_size'] == 120)
    river_history = await get_hand_history(game_fix, monkeypatch, river_actions, "RIVER")
    assert(game_fix.get_state()['board']['stage'] == "RIVER")
    assert(len(game_fix.get_state()['board']['cards']) == 5)
    assert(game_fix.get_state()['pot']['pot_size'] == 120)





@pytest.mark.asyncio
async def test_play_hand(game_fix_not_initialized, monkeypatch):
    preflop_actions = [
        {'sid' : '3', 'amount_bet' : 40, 'action' : "call"},
        {'sid' : '1', 'amount_bet' : 20, 'action' : "call"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    flop_actions = [
        {'sid' : '3', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '1', 'amount_bet' : 0, 'action' : "check"},
        {'sid' : '2', 'amount_bet' : 0, 'action' : "check"},
    ]
    turn_actions = flop_actions
    river_actions = flop_actions
    test_mock = AsyncMock(side_effect=preflop_actions + flop_actions + turn_actions + river_actions)
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix_not_initialized.play_hand()



