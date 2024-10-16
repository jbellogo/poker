import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot
from unittest.mock import Mock



def test_betting_round1(monkeypatch, pot_fix):
    '''
    All players call
    '''
    pot_state = pot_fix.get_pot_state()
    P1resp = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)
    P2resp = PlayerBetResponse(pid=2, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)
    P3resp = PlayerBetResponse(pid=3, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)
    player_actions = [P1resp, P2resp, P3resp]
    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)

    pot_fix.betting_round(BoardStage.PREFLOP)
    hand_history = pot_fix.get_hand_history()['PREFLOP']

    assert(hand_history[0]['player1']['response'] == P1resp)
    assert(hand_history[1]['player2']['response'] == P2resp)
    assert(hand_history[2]['player3']['response'] == P3resp)

    # pprint.pp(hand_history)
    assert(len(hand_history)==3) # only three bets all call.
    assert(hand_history[0]['player1']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : True,  ## uhm 
      "minimum_raise" : 40,
      "pot_size" : 20,
    })
    assert(hand_history[1]['player2']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : True,
      "minimum_raise" : 40,
      "pot_size" : 40,
    })
    assert(hand_history[2]['player3']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : True,
      "minimum_raise" : 40,
      "pot_size" : 60,
    })


# def test_betting_round2(monkeypatch, pot_fix):
#     '''
#     '''
#     pot_state = pot_fix.get_pot_state()
#     P1resp1 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)
#     P2resp = PlayerBetResponse(pid=2, player_funds=50, action = "raise", amount_bet=40, pot_state=pot_state)
#     P3resp = PlayerBetResponse(pid=3, player_funds=50, action = "call", amount_bet=40, pot_state=pot_state)
#     P1resp2 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)

#     player_actions = [P1resp1, P2resp, P3resp, P1resp2]
#     test_mock = Mock(side_effect=player_actions)
#     monkeypatch.setattr(Player, "make_bet", test_mock)
#     pot_fix.betting_round(BoardStage.PREFLOP)
#     hand_history = pot_fix.get_hand_history()['PREFLOP']

#     pprint.pp(hand_history)
#     assert(len(hand_history)==4) # only three bets all call.
#     assert(hand_history[0]['player1']['pot_state'] == {
#       "call_amount" : 20,
#       "check_allowed" : True,
#       "minimum_raise" : 40,
#       "pot_size" : 20,
#     })
#     assert(hand_history[1]['player2']['pot_state'] == {
#       "call_amount" : 20,
#       "check_allowed" : True,
#       "minimum_raise" : 40,
#       "pot_size" : 40,
#     })
#     assert(hand_history[2]['player3']['pot_state'] == {
#       "call_amount" : 20,
#       "check_allowed" : True,
#       "minimum_raise" : 40,
#       "pot_size" : 60,
#     })
#     assert(hand_history[3]['player1']['pot_state'] == {
#       "call_amount" : 20,
#       "check_allowed" : True,
#       "minimum_raise" : 40,
#       "pot_size" : 20,
#     })



# @TODO test validation. 
