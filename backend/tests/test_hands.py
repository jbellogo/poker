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

    # test four of a kind
    cards = get_cards(['AH', 'AD', 'AC', 'AS', '2D', '2H', '4D'])
    best_hand, cards = get_most_of_a_kind(cards)
    assert best_hand == HandRankings.FOUR_OF_A_KIND
    assert cards == set(['ACE_HEARTS', 'ACE_DIAMONDS', 'ACE_CLUBS', 'ACE_SPADES'])



def test_get_straight():
    cards = get_cards(['2D', '3H', '4S', '5H', '6H', 'AH', '8H'])
    best_hand, cards = get_straight(cards)
    assert best_hand == HandRankings.STRAIGHT
    assert cards == set(['TWO_DIAMONDS', 'THREE_HEARTS', 'FOUR_SPADES', 'FIVE_HEARTS', 'SIX_HEARTS'])

def test_get_flush():
    cards = get_cards(['2D', '3H', '4S', '5H', '6H', 'AH', '8H'])
    best_hand, cards = get_flush(cards)
    assert best_hand == HandRankings.FLUSH
    assert cards == set(['THREE_HEARTS', 'FIVE_HEARTS', 'SIX_HEARTS', 'ACE_HEARTS', 'EIGHT_HEARTS'])

def test_get_straight_flush():
    cards = get_cards(['2D', '3H', '4S', '4H', '5H', '6H', '7H'])
    # test straight
    hand, hand_cards = get_straight(cards)
    assert hand == HandRankings.STRAIGHT
    # assert cards == set(['THREE_HEARTS', 'FOUR_HEARTS', 'FIVE_HEARTS', 'SIX_HEARTS', 'SEVEN_HEARTS']) # this fails
    assert hand_cards == set(['THREE_HEARTS', 'FOUR_SPADES', 'FIVE_HEARTS', 'SIX_HEARTS', 'SEVEN_HEARTS'])

    # test flush
    hand, hand_cards = get_flush(cards)
    assert hand == HandRankings.FLUSH
    assert hand_cards == set(['THREE_HEARTS', 'FOUR_HEARTS', 'FIVE_HEARTS', 'SIX_HEARTS', 'SEVEN_HEARTS'])

    # test straight flush
    best_hand, hand_cards = get_straight_flush(cards)
    assert best_hand == HandRankings.STRAIGHT_FLUSH
    assert hand_cards == set(['THREE_HEARTS', 'FOUR_HEARTS', 'FIVE_HEARTS', 'SIX_HEARTS', 'SEVEN_HEARTS'])

    # test royal flush
    cards = get_cards(['AD', 'KD', 'QD', 'JD', 'TD', 'AH', 'KH'])
    best_hand, hand_cards = get_straight_flush(cards)
    assert best_hand == HandRankings.ROYAL_FLUSH
    assert hand_cards == set(['ACE_DIAMONDS', 'KING_DIAMONDS', 'QUEEN_DIAMONDS', 'JACK_DIAMONDS', 'TEN_DIAMONDS'])


def test_get_best_hand():
    # test royal flush
    cards = get_cards(['AD', 'KD', 'QD', 'JD', 'TD', 'AH', 'KH'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.ROYAL_FLUSH
    assert hand_cards == set(['ACE_DIAMONDS', 'KING_DIAMONDS', 'QUEEN_DIAMONDS', 'JACK_DIAMONDS', 'TEN_DIAMONDS'])

    # test straight flush
    cards = get_cards(['2D', '3H', '4S', '4H', '5H', '6H', '7H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.STRAIGHT_FLUSH
    assert hand_cards == set(['THREE_HEARTS', 'FOUR_HEARTS', 'FIVE_HEARTS', 'SIX_HEARTS', 'SEVEN_HEARTS'])

    # test four of a kind
    cards = get_cards(['4D', '3H', '4S', '4H', '4C', '6H', '7H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.FOUR_OF_A_KIND
    assert hand_cards == set(['FOUR_DIAMONDS', 'FOUR_HEARTS', 'FOUR_SPADES', 'FOUR_CLUBS'])

    # test full house
    cards = get_cards(['4D', '4H', '4S', '3H', '3S', 'AH', 'AD'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.FULL_HOUSE
    assert hand_cards == set(['FOUR_DIAMONDS', 'FOUR_HEARTS', 'FOUR_SPADES', 'ACE_HEARTS', 'ACE_DIAMONDS'])

    # test flush
    cards = get_cards(['AD', 'AH', 'AS', '4H', '3H', '2H', '7H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.FLUSH
    assert hand_cards == set(['ACE_HEARTS', 'FOUR_HEARTS', 'THREE_HEARTS', 'TWO_HEARTS', 'SEVEN_HEARTS'])

    # test straight
    cards = get_cards(['2D', '3D', '4S', '5H', '6H', '7H', '8H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.STRAIGHT
    assert hand_cards == set(['EIGHT_HEARTS', 'SEVEN_HEARTS', 'SIX_HEARTS', 'FIVE_HEARTS', 'FOUR_SPADES'])

    # test three of a kind
    cards = get_cards(['2D', '3H', '4S', '4H', '4C', '6H', '7H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.THREE_OF_A_KIND
    assert hand_cards == set(['FOUR_CLUBS', 'FOUR_HEARTS', 'FOUR_SPADES'])

    # test two pair
    cards = get_cards(['2D', '2H', '5S', '4H', '4C', '6H', '7H'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.TWO_PAIR
    assert hand_cards == set(['FOUR_HEARTS', 'FOUR_CLUBS', 'TWO_HEARTS', 'TWO_DIAMONDS'])

    # test pair
    cards = get_cards(['2D', '2H', '5S', '4H', 'TC', 'KH', 'QH'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.PAIR
    assert hand_cards == set(['TWO_HEARTS', 'TWO_DIAMONDS'])

    # test high card
    cards = get_cards(['2D', '3C', '4S', '5H', 'TH', 'KH', 'JC'])
    best_hand, hand_cards = get_best_hand(cards)
    assert best_hand == HandRankings.HIGH_CARD
    assert hand_cards == set(['KING_HEARTS'])


    
