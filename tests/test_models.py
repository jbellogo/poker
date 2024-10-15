import pytest
from unittest.mock import Mock
import sys
  # append the path of the parent directory
sys.path.append("..")
from models import Deck, Entity, Player, Board, BoardStage, PlayerBetResponse, Pot
from typing import Union


# it is convenient to test on abstract base class

## you can abstract it to entity and call teh function for player and board
def test_deal_player():
    '''
    test that 2 cards are removed from the deck and those two cards are added to Player.
    '''
    deck = Deck()
    player = Player(pid=0, funds=100)
    deck_len : int = deck.length()
    player_len : int = player.length()
    cards = deck.deal_cards(player)
    assert(deck.length() == deck_len-player.cards_dealt())
    assert(player.length() == player_len+player.cards_dealt())
    for card in cards:
      assert(player.has(card) == True)
      assert(deck.has(card) == False)


def test_deal_board():
    deck = Deck()
    board = Board()
    assert(board.current_stage() == BoardStage.ZERO)
    board.next_stage()
    
    assert(board.current_stage() == BoardStage.PREFLOP)
    assert(board.length() == 0)

    assert(len(deck.deal_cards(board)) == 3)
    assert(board.next_stage() == True)
    assert(board.current_stage() == BoardStage.FLOP)
    assert(board.length() == 3)

    assert(len(deck.deal_cards(board)) == 1)
    assert(board.next_stage() == True)
    assert(board.current_stage() == BoardStage.TURN)
    assert(board.length() == 4)

    assert(len(deck.deal_cards(board)) == 1)
    assert(board.next_stage() == True)
    assert(board.current_stage() == BoardStage.RIVER)
    assert(board.length() == 5)

    # assert(len(deck.deal_cards(board)) == 0)
    assert(board.next_stage() == False)
    # assert(board.current_stage() == BoardStage) # ??
    # assert(board.length() == 5)   $ shoud we guard against it?



## @TODO make PLAYERS a fixture. 
    

def test_betting_round1(monkeypatch):
    '''
    All players call
    '''
    PLAYERS  = [Player(pid = i, funds=100, current_hand_betting_status = "active") for i in range(1,4)]
    pot = Pot(bb_amount = 20, players = PLAYERS)
    P1resp = PlayerBetResponse(pid=1, player_funds=50, action = "call", amount_bet=20)
    P2resp = PlayerBetResponse(pid=2, player_funds=50, action = "call", amount_bet=20)
    P3resp = PlayerBetResponse(pid=3, player_funds=50, action = "call", amount_bet=20)

    player_actions = [P1resp, P2resp, P3resp]
    test_mock = Mock(side_effect=player_actions)
    monkeypatch.setattr(Player, "make_bet", test_mock)

    # player.make_bet() needs to be patched with the Playerresponse!!!1
    pot.betting_round(BoardStage.PREFLOP)
    assert(pot.get_hand_history()['PREFLOP'] == [P1resp, P2resp, P3resp])




   

   





# def test_game_flow():
#     '''
#     Only tests stages: preflop, flop, turn, river.
#     doesn't test betting 
#     doesn't test winner
#     '''
#     deck = Deck()
#     board = Board(deck)
#     assert(board.__str__() == [])
#     board.next_stage(deck)

    