import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot
from unittest.mock import Mock


import pprint



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
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 0,
    })
    assert(hand_history[1]['player2']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 20,
    })
    assert(hand_history[2]['player3']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 40,
    })


def test_betting_round2(monkeypatch, pot_fix):
    '''
    '''
    round = BoardStage.PREFLOP
    pot_state = pot_fix.get_pot_state()
    P1resp1 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)
    P2resp = PlayerBetResponse(pid=2, player_funds=50, action = "raise", amount_bet=40, pot_state=pot_state)
    P3resp = PlayerBetResponse(pid=3, player_funds=50, action = "call", amount_bet=40, pot_state=pot_state)
    P1resp2 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20, pot_state=pot_state)

    player_actions = [P1resp1, P2resp, P3resp, P1resp2]
    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)
    pot_fix.betting_round(round)
    hand_history = pot_fix.get_hand_history()['PREFLOP']

    pprint.pp(hand_history)
    assert(len(hand_history)==4) # 4 moves total
    assert(hand_history[0]['player1']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 0,
    })
    assert(hand_history[1]['player2']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 20,
    })
    ## P2 raises, so state of P3 changes
    assert(hand_history[2]['player3']['pot_state'] == {
      "call_amount" : 40,
      "check_allowed" : False,
      "minimum_raise" : 80,
      "pot_size" : 60,
    })
    assert(hand_history[3]['player1']['pot_state'] == {
      "call_amount" : 40,
      "check_allowed" : False,
      "minimum_raise" : 80,
      "pot_size" : 100,
    })


def test_betting_round3(monkeypatch, pot_fix):
    '''
    '''
    round = BoardStage.FLOP
    # pot_state = pot_fix.get_pot_state()
    
    P1resp1 = PlayerBetResponse(pid=1, player_funds=50, action = "check", amount_bet=0)
    P2resp1 = PlayerBetResponse(pid=2, player_funds=50, action = "raise", amount_bet=100)
    P3resp = PlayerBetResponse(pid=3, player_funds=50, action = "raise", amount_bet=200)
    P1resp2 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=200)
    P2resp2 = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=100)

    player_actions = [P1resp1, P2resp1, P3resp, P1resp2, P2resp2]
    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)

    ## Need to patch this to obtain correct calling prices for each player.
    total_bets_made_pre_action = [0, 0, 0, 0, 100]
    test_mock = Mock(side_effect=total_bets_made_pre_action)
    monkeypatch.setattr(Player, "amount_bet_this_hand", test_mock)


    pot_fix.betting_round(round)
    hand_history = pot_fix.get_hand_history()['FLOP']

    pprint.pp(hand_history)
    assert(len(hand_history)==5) # 5 moves total
    assert(hand_history[0]['player1']['pot_state'] == {
      "call_amount" : 0,
      "check_allowed" : True,
      "minimum_raise" : 1,
      "pot_size" : 0,
    })
    assert(hand_history[1]['player2']['pot_state'] == {
      "call_amount" : 0,
      "check_allowed" : True,
      "minimum_raise" : 1,
      "pot_size" : 0,
    })
    ## P2 raised 100
    assert(hand_history[2]['player3']['pot_state'] == {
      "call_amount" : 100,
      "check_allowed" : False,
      "minimum_raise" : 200,
      "pot_size" : 100,
    })
    ## P3 raised 200
    assert(hand_history[3]['player1']['pot_state'] == {
      "call_amount" : 200,
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 300,
    })
    assert(hand_history[4]['player2']['pot_state'] == {
      "call_amount" : 100,   ## P2 ONLY NEEDS TO 100 to call. @TODO important Call_amount changes per player!!!!
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 500,
    })








# @TODO test validation of call amounts and minimum raises. Test blind taxes
