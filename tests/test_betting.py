import pytest
from models import Deck, Player, Board, BoardStage, PlayerBetResponse, Pot
from unittest.mock import Mock
from typing import List# Tuple
import pprint




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


# Pot tests. Purely betting rounds. 
def test_betting_round1(monkeypatch, pot_fix_preflop):
    '''
    Situation: All players call
    Preflop stage, no checking allowed.
    '''
    round = BoardStage.PREFLOP
    actions = [('call', 20), ('call',20), ('call', 20)] # @TODO the calling amount should not need to be input by players
    player_actions = get_player_actions(actions)

    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)
    pot_fix_preflop.betting_round(round)
    hand_history = pot_fix_preflop.get_hand_history()['PREFLOP'] # This is the thing

    assert(hand_history[0]['player1']['response'] == {
        'action': 'call',
        'amount_bet': 20,
        'pid': 1,
        'player_funds': 50})
    assert(hand_history[1]['player2']['response'] == {
        'action': 'call',
        'amount_bet': 20,
        'pid': 2,
        'player_funds': 50})
    assert(hand_history[2]['player3']['response'] == {
        'action': 'call',
        'amount_bet': 20,
        'pid': 3,
        'player_funds': 50})

    assert(len(hand_history)==3) # only three bets all call.
    # These represent the state player i sees before performing his action !!!
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


## passing betting arguments to player_actions fixture
# betting_actions = [('call', 20), ('raise',40), ('call', 40), ('call', 20)]
# @pytest.mark.parametrize('player_actions', [betting_actions], indirect=True)
def test_betting_round2(monkeypatch, pot_fix_preflop):
    '''
    Preflop stage, no checking allowed.
    Test single raise. Call amounts should update. 
    '''
    round = BoardStage.PREFLOP
    # Situation:
    actions = [('call', 20), ('raise',40), ('call', 40), ('call', 20)]
    player_actions = get_player_actions(actions) # NEW

    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)
    pot_fix_preflop.betting_round(round)
    hand_history = pot_fix_preflop.get_hand_history()['PREFLOP'] # This is the thing

    # pprint.pp(hand_history)
    assert(len(hand_history)==4) # 4 moves total
    # These represent the state player i sees before performing his action !!!
    # P1 sees this bellow and calls 20
    assert(hand_history[0]['player1']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 0,
    })
    # P2 sees this bellow and raises 40
    assert(hand_history[1]['player2']['pot_state'] == {
      "call_amount" : 20,
      "check_allowed" : False,
      "minimum_raise" : 40,
      "pot_size" : 20,
    })
    # P3 sees this bellow and calls 40
    assert(hand_history[2]['player3']['pot_state'] == {
      "call_amount" : 40,
      "check_allowed" : False,
      "minimum_raise" : 80,
      "pot_size" : 60,
    })

    # P1 calls his remainding 20
    assert(hand_history[3]['player1']['pot_state'] == {
      "call_amount" : 40,
      "check_allowed" : False,
      "minimum_raise" : 80,
      "pot_size" : 100,
    })



def test_betting_round3(monkeypatch, pot_fix_flop):
    '''
    Tests flop stage, checking allowed.
    Test multiple raises. 
    '''
    initial_pot_state = {
        'call_amount': 0,
        'check_allowed' : True,
        'minimum_raise' : 100,
        'pot_size' : 1000
    }
    assert(pot_fix_flop.get_pot_state() == initial_pot_state)
    round = BoardStage.FLOP
    actions = [('check', 0), ('raise',100), ('raise', 200), ('call', 200), ('call', 100)]
    player_actions = get_player_actions(actions) # NEW
    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)
    pot_fix_flop.betting_round(round)
    hand_history = pot_fix_flop.get_hand_history()['FLOP']
    # pprint.pprint(hand_history)

    assert(len(hand_history)==5) # 5 moves total
    # These represent the state player i sees before performing his action !!!

    # P1 sees this bellow and checks
    assert(hand_history[0]['player1']['pot_state'] == initial_pot_state)
    # P2 sees this bellow and raises 100
    # pprint.pprint(hand_history[1]['player2']['pot_state'])
    assert(hand_history[1]['player2']['pot_state'] == initial_pot_state)
    ## P3 sees this bellow and raises 200
    assert(hand_history[2]['player3']['pot_state'] == {
        'call_amount': 100,
        'check_allowed' : False,
        'minimum_raise' : 200,
        'pot_size' : 1100
    })
    ## P1 sees this bellow and calls 200
    assert(hand_history[3]['player1']['pot_state'] == {
      "call_amount" : 200,
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 1300,
    })
    ## P2 Calls with 100
    assert(hand_history[4]['player2']['pot_state'] == {
      "call_amount" : 100,   
      ## P2 ONLY NEEDS TO 100 to call. @TODO important Call_amount changes per player!!!!
      ## This makes things tricky...
      "check_allowed" : False,
      "minimum_raise" : 400,
      "pot_size" : 1500,
    })



# @TODO test validation of call amounts and minimum raises. Test blind taxes
# Test folds