import pytest
import pprint

from typing import List

# f

# from models.game import Game
# from models.entities import Player
from models import *




def test_update_player_turns(game_fix):
    ## 
    players = list(range(1, NUM_PLAYERS+1))
    print(players)

    # for sb in range(1, NUM_PLAYERS):
    #     assert(sb_index == sb)
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




