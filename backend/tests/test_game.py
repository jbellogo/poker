import pytest
import pprint

from typing import List

from models import *



def test_update_player_turns_basic(game_fix):
    players = list(range(1, NUM_PLAYERS+1))

    assert(game_fix.get_sb_index()==0)
    assert(game_fix.get_players() == players)

    game_fix.update_player_turns()

    assert(game_fix.get_sb_index()==1)
    updated_players = players[1:] + players[:1]

    assert(game_fix.get_players() == updated_players)

    game_fix.update_player_turns()

    assert(game_fix.get_sb_index()==2)
    updated_players = players[2:] + players[:2]

    assert(game_fix.get_players() == updated_players)


def test_update_player_turns_modular(game_fix):
    '''Tests that after all players have been sb, it is the turn of the first sb again.'''
    players = list(range(1, NUM_PLAYERS+1))
    assert(game_fix.get_sb_index()==0)
    assert(game_fix.get_players() == players)

    for _ in range(NUM_PLAYERS):
        game_fix.update_player_turns()
    
    assert(game_fix.get_sb_index()==0)
    assert(game_fix.get_players() == players)






