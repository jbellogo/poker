import pytest
import pprint
from models import *


def get_cards(list_strs : list[str]) -> list[Card]:
    '''
    Input: ['2H', 'AS', 'KC', '2D']
    Output: [Card(suit=Suit.HEARTS, rank=Rank.TWO), Card(suit=Suit.SPADES, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.KING), Card(suit=Suit.DIAMONDS, rank=Rank.TWO)]
    '''
    mymap = {
        '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR, '5': Rank.FIVE, 
        '6': Rank.SIX, '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE, 
        'T': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE
    }

    cards = [Card(suit=Suit(card_str[1]), rank=mymap[card_str[0]]) for card_str in list_strs]
    return sorted(cards, key=lambda x: x.rank.value, reverse=True)

def test_get_most_of_a_kind():

    # test high card
    cards = get_cards(['2H', '3H', '4H', '5H', '8S', '9S', 'TS'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.HIGH_CARD
    assert cards == set(['TEN_SPADES'])

    # test pair
    cards = get_cards(['2H', 'AD', 'KC', '2D', '3D', '4D', '5D'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.PAIR
    assert cards == set(['TWO_HEARTS', 'TWO_DIAMONDS'])

    # test two pair
    cards = get_cards(['2H', 'AD', 'KC', '2D', '3D', '3S', '5D'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.TWO_PAIR
    assert cards == set(['TWO_HEARTS', 'TWO_DIAMONDS', 'THREE_DIAMONDS', 'THREE_SPADES'])

    # test three of a kind
    cards = get_cards(['AH', 'AD', 'AC', '2D', '3D', '4S', '5C'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.THREE_OF_A_KIND
    assert cards == set(['ACE_HEARTS', 'ACE_DIAMONDS', 'ACE_CLUBS'])

    # test full house
    cards = get_cards(['AH', 'AD', 'AC', '2D', '2S', '3C', '3S'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.FULL_HOUSE
    assert cards == set(['ACE_HEARTS', 'ACE_DIAMONDS', 'ACE_CLUBS', 'THREE_SPADES', 'THREE_CLUBS'])



