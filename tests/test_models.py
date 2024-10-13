import pytest
import sys
  # append the path of the parent directory
sys.path.append("..")
from models import Deck, Entity, Player, Board, BoardStage
from typing import Union


# it is convenient to test on abstract base class

## you can abstract it to entity and call teh function for player and board
def test_deal_player():
    '''
    test that 2 cards are removed from the deck and those two cards are added to Player.
    '''
    deck = Deck()
    player = Player(player_id=0)
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

    