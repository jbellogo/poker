import pytest
import sys
  # append the path of the parent directory
sys.path.append("..")
from models import Deck, Entity, Player, Board
from typing import Union


# it is convenient to test on abstract base class

def test_deal_card():
    deck = Deck()
    player = Player()
    deck_len : int = deck.length()
    player_len : int = player.length()
    card = deck.deal_card(player)
    assert(deck.length() == deck_len-1)
    assert(player.length() == player_len+1)
    assert(player.has(card) == True)
    assert(deck.has(card) == False)

    