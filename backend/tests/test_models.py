import pytest
import sys
from models import Deck, Entity, Player, Board, BoardStage, PlayerBetResponse, Pot
from typing import Union
import pprint


def test_deal_player(deck_fix, player_fix):
    '''
    test that 2 cards are removed from the deck and those two cards are added to Player.
    '''
    deck_len : int = deck_fix.length()
    player_len : int = player_fix.length()
    cards = deck_fix.deal_cards(player_fix)
    assert(deck_fix.length() == deck_len-player_fix.cards_dealt())
    assert(player_fix.length() == player_len+player_fix.cards_dealt())
    for card in cards:
      assert(player_fix.has(card) == True)
      assert(deck_fix.has(card) == False)


def test_deal_board(deck_fix, board_fix):
    assert(board_fix.current_stage() == BoardStage.ZERO)
    board_fix.next_stage()
    
    assert(board_fix.current_stage() == BoardStage.PREFLOP)
    assert(board_fix.length() == 0)

    assert(len(deck_fix.deal_cards(board_fix)) == 3)
    assert(board_fix.next_stage() == True)
    assert(board_fix.current_stage() == BoardStage.FLOP)
    assert(board_fix.length() == 3)

    assert(len(deck_fix.deal_cards(board_fix)) == 1)
    assert(board_fix.next_stage() == True)
    assert(board_fix.current_stage() == BoardStage.TURN)
    assert(board_fix.length() == 4)

    assert(len(deck_fix.deal_cards(board_fix)) == 1)
    assert(board_fix.next_stage() == True)
    assert(board_fix.current_stage() == BoardStage.RIVER)
    assert(board_fix.length() == 5)

    assert(board_fix.next_stage() == False)



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

    