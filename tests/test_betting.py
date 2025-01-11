import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot
from unittest.mock import Mock, AsyncMock
from typing import List# Tuple
import pprint
import asyncio
from aiohttp import ClientSession



###### Test every function in every module!!!

def get_player_actions(actions : list[tuple[str,int]]) -> List[PlayerBetResponse]:
    player_actions = []
    '''
    Assume three players, Actions go in modular sequence ie P1, P2, P3, P1, P2, P3,...
    ex actions = [('call', 20), ('raise',40), ('call', 40), ('call', 20)]
    Returns List[PlayerBetResponses] from simplified list of tuples
    '''
    for i, a in enumerate(actions):
        pid = (i%3)+1
        action, amount = a
        player_actions.append(PlayerBetResponse(pid=pid, player_funds=50, action = action, amount_bet=amount))

    return player_actions


# @pytest.mark.asyncio
# async def test_betting_round_1(monkeypatch, game_fix):
#     '''
#     Situation: All players call
#     Preflop stage, no checking allowed.
#     game_fix num_players=3 and sb_amount=20
#     '''
#     round = BoardStage.PREFLOP
#     actions = [('call', 40), ('call',40), ('call', 40)] # @TODO the calling amount should not need to be input by players
#     player_actions = get_player_actions(actions)

#     test_mock = AsyncMock(side_effect=player_actions)
#     monkeypatch.setattr(Player, "make_bet", test_mock)
#     await game_fix.betting_round(board_stage=round)   ## @TODO I'm thinking we will need asyncio.gather()
#     hand_history = game_fix.get_hand_history()['PREFLOP'] # This is the thing


#     pprint.pprint(hand_history)
#     assert(len(hand_history)==3) # only three bets all call.


#     # These represent the state player i sees before performing his action !!!
#     assert(hand_history[0]['game_state']['pot'] == {
#         'call_amount' : 40,
#         'check_allowed' : False,
#         'minimum_raise' : 80,
#         'pot_size' : 0})
#     assert(hand_history[0]['response'] == {
#         'action': 'call',
#         'amount_bet': 40,
#         'pid': 1,
#         'player_funds': 50})


#     assert(hand_history[1]['game_state']['pot'] == {
#         "call_amount" : 40,
#         "check_allowed" : False,
#         "minimum_raise" : 80,
#         "pot_size" : 40,
#       })
#     assert(hand_history[1]['response'] == {
#         'action': 'call',
#         'amount_bet': 40,
#         'pid': 2,
#         'player_funds': 50})


#     assert(hand_history[2]['game_state']['pot'] == {
#       "call_amount" : 40,
#       "check_allowed" : False,
#       "minimum_raise" : 80,
#       "pot_size" : 80,
#     })
#     assert(hand_history[2]['response'] == {
#         'action': 'call',
#         'amount_bet': 40,
#         'pid': 3,
#         'player_funds': 50})


# @pytest.mark.asyncio
# async def test_betting_round_2(monkeypatch, game_fix):
#     '''
#     Preflop stage, no checking allowed.
#     Situation: single raise. Call amounts should update. 
#     '''
#     round = BoardStage.PREFLOP
#     # Situation:
#     actions = [('call', 40), ('raise',80), ('call', 80), ('call', 40)]
#     player_actions = get_player_actions(actions) # NEW

#     test_mock = AsyncMock(side_effect=player_actions)
#     monkeypatch.setattr(Player, "make_bet", test_mock)
#     await game_fix.betting_round(board_stage=round)
#     hand_history = game_fix.get_hand_history()['PREFLOP'] # This is the thing

#     # pprint.pp(hand_history)
#     assert(len(hand_history)==4) # 4 moves total
#     # These represent the state player i sees before performing his action !!!
#     # P1 sees this bellow and calls 40
#     assert(hand_history[0]['game_state']['pot'] == {
#       "call_amount" : 40,
#       "check_allowed" : False,
#       "minimum_raise" : 80,
#       "pot_size" : 0,
#     })
#     # P2 sees this bellow and raises 80
#     assert(hand_history[1]['game_state']['pot'] == {
#       "call_amount" : 40,
#       "check_allowed" : False,
#       "minimum_raise" : 80,
#       "pot_size" : 40,
#     })
#     # P3 sees this bellow and calls 80
#     assert(hand_history[2]['game_state']['pot'] == {
#       "call_amount" : 80,
#       "check_allowed" : False,
#       "minimum_raise" : 160,
#       "pot_size" : 120,
#     })

#     # P1 calls his remainding 40
#     assert(hand_history[3]['game_state']['pot'] == {
#       "call_amount" : 80,
#       "check_allowed" : False,
#       "minimum_raise" : 160,
#       "pot_size" : 200,
#     })


@pytest.mark.asyncio
async def test_betting_round3(monkeypatch, game_fix):
    '''
    Situation: flop stage, check allowed, multiple raises. 
    '''
    # PREFLOP actions:
    actions = [('call', 40), ('raise',80), ('call', 80), ('call', 40)]
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock)
    await game_fix.betting_round(board_stage=BoardStage.PREFLOP)


    # FLOP actions:
    flop_initial_conditions = {
      "call_amount" : 0,
      "check_allowed" : True,
      "minimum_raise" : 80,
      "pot_size" : 240,
    }

    actions = [('check', 0), ('raise',100), ('raise', 200), ('call', 200), ('call', 100)]
    test_mock = AsyncMock(side_effect=get_player_actions(actions))
    monkeypatch.setattr(Player, "request_betting_response", test_mock) # NEW mocked method!!!!!
    await game_fix.betting_round(BoardStage.FLOP)
    hand_history = game_fix.get_hand_history()['FLOP']
    # pprint.pprint(hand_history)

    assert(len(hand_history)==5) # 5 moves total
    # P1 sees this bellow and checks
    assert(hand_history[0]['game_state']['pot'] == flop_initial_conditions)
    # P2 sees this bellow and raises 100
    # pprint.pprint(hand_history[1]['player2']['pot_state'])
    assert(hand_history[1]['game_state']['pot'] == flop_initial_conditions)


    ## P3 sees this bellow and raises 200
    assert(hand_history[2]['game_state']['pot'] == {
        'call_amount': 100,
        'check_allowed' : False,
        'minimum_raise' : 200,
        'pot_size' : 340
    })

    ## P1 sees this bellow and calls 200
    assert(hand_history[3]['game_state']['pot'] == {
      "call_amount" : 200,
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 540,
    })
    ## P2 Calls with 100
    assert(hand_history[4]['game_state']['pot'] == {
      "call_amount" : 100,   
      ## P2 ONLY NEEDS TO 100 to call. @TODO important Call_amount changes per player!!!!
      ## This makes things tricky... need to personalize pot state to players somehow 
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 740,
    })



# # @TODO test validation of call amounts and minimum raises. Test blind taxes
# # Test folds