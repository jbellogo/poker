import pytest
import sys
from models import *
import pprint


def test_deal_player(deck_fix, player_fix):
    '''
    test that 2 cards are removed from the deck and those two cards are added to Player.
    '''
    deck_len : int = deck_fix.length()
    player_len : int = player_fix.length()

    cards = deck_fix.deal_cards(player_fix)

    assert(deck_fix.length() == deck_len - player_fix._cards_dealt())
    assert(player_fix.length() == player_len + player_fix._cards_dealt())

    for card in cards:
      assert(player_fix.has(card) == True)
      assert(deck_fix.has(card) == False)


def test_deal_board(game_fix):
    game_fix.initialize_betting_round("PREFLOP")
    board_state = game_fix.board.get_state()
    assert(board_state['stage'] == "PREFLOP")
    assert(len(board_state['cards']) == 0)

    game_fix.initialize_betting_round("FLOP")
    board_state = game_fix.board.get_state()
    assert(board_state['stage'] == "FLOP")
    flop_cards = board_state['cards'].copy()
    assert(len(flop_cards) == 3)

    game_fix.initialize_betting_round("TURN")
    board_state = game_fix.board.get_state()
    assert(board_state['stage'] == "TURN")
    turn_cards = board_state['cards'].copy()
    assert(len(turn_cards) == 4)
    assert(turn_cards[:-1] == flop_cards)

    game_fix.initialize_betting_round("RIVER")
    board_state = game_fix.board.get_state()
    assert(board_state['stage'] == "RIVER")
    river_cards = board_state['cards'].copy()

    assert(len(river_cards) == 5)
    assert(river_cards[:-1] == turn_cards)

    