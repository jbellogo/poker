

# from models import *
# from unittest.mock import AsyncMock
# import asyncio

# _TESTING_SB_AMOUNT = 40
# _TESTING_INITIAL_PLAYER_FUNDS = 1000
# _TESTING_NUM_PLAYERS = 3


# players = [Player(name = f"player{i}",
#                     pid = i, 
#                     sid = f"sid{i}",
#                     funds=_TESTING_INITIAL_PLAYER_FUNDS) for i in range(1,_TESTING_NUM_PLAYERS+1)]
# players[0].set_role(PlayerRole.SMALL_BLIND)
# players[1].set_role(PlayerRole.BIG_BLIND)

# game = Game(sb_amount=_TESTING_SB_AMOUNT,
#             initial_player_funds=_TESTING_INITIAL_PLAYER_FUNDS)
# for player in players:
#     game.add_player(player.sid, player.name)

# actions = [
#     {
#         'sid' : '1',
#         'amount_bet' : 40,
#         'action' : "call",
#     },
#     {
#         'sid' : '2',
#         'amount_bet' : 40,
#         'action' : "call",
#     },
#     {
#         'sid' : '3',
#         'amount_bet' : 40,
#         'action' : "call",
#     }]

# test_mock = AsyncMock(side_effect=actions)
# monkeypatch.setattr(Player, "request_betting_response", test_mock)
# print("betting round 1 test")
# await game_fix.betting_round(board_stage=BoardStage.PREFLOP)   ## @TODO I'm thinking we will need asyncio.gather()
# hand_history = game_fix.get_hand_history()['PREFLOP']
   