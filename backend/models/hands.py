# '''
# Hand validation.
# take full board and cards from an active player -> compute highest ranking 5 card hand.
# Do that for all active players to determine winner.
# '''

from models.definitions import Card, HandRankings, Rank
from typing import Union
import pprint


def get_most_of_a_kind(sorted_cards : list[Card]) -> tuple[HandRankings, set[Card]]:
    '''
    Returns the highest ranking hand made up of repeating cards:
    - High Card <  Pair < Two Pair <  Three of a Kind < Full House < Four of a Kind
    '''    
    # print(f"SORTED CARDS:")
    # pprint.pprint(sorted_cards)
    rank_counts = { card.rank.name : set() for card in sorted_cards }
    maximally_occurring_rank = sorted_cards[0].rank.name

    # group cards by repeating ranks
    for card in sorted_cards:
        rank_counts[card.rank.name].add(card.__str__())
        if len(rank_counts[card.rank.name]) > len(rank_counts[maximally_occurring_rank]):
            maximally_occurring_rank = card.rank.name

    # print(f"MAXIMALLY OCCURRING RANK: {maximally_occurring_rank}")
    # pprint.pprint(rank_counts)

    # the order of the following checks is important to return the highest ranking hand
    hand_rank = HandRankings.HIGH_CARD
    if len(rank_counts[maximally_occurring_rank]) == 4:
        hand_rank = HandRankings.FOUR_OF_A_KIND

    elif len(rank_counts[maximally_occurring_rank]) == 3:
        hand_rank = HandRankings.THREE_OF_A_KIND
        # check for full house
        for rank, cards in rank_counts.items():
            if len(cards) == 2 and rank != maximally_occurring_rank:
                return (HandRankings.FULL_HOUSE, rank_counts[maximally_occurring_rank] | rank_counts[rank]) # set union
    elif len(rank_counts[maximally_occurring_rank]) == 2:
        hand_rank = HandRankings.PAIR
        # check for two pairs
        for rank, cards in rank_counts.items():
            if len(cards) == 2 and rank != maximally_occurring_rank:
                return (HandRankings.TWO_PAIR, rank_counts[maximally_occurring_rank] | rank_counts[rank])
    return (hand_rank, rank_counts[maximally_occurring_rank])  # @TODO return the cards that make up the hand


def add_ace_low(sorted_cards : list[Card]):
    i = 0
    new_lst = [Card(suit=card.suit, rank=card.rank) for card in sorted_cards]  # deep copy
    while sorted_cards[i].rank == Rank.ACE:
        ace_copy = Card(suit=sorted_cards[0].suit, rank=Rank.ACE_LOW)  # Create new Card object
        new_lst.append(ace_copy)  # at the end position, to facilitate straight detection
        i += 1
    return new_lst


def get_straight(sorted_cards : list[Card]) -> Union[bool, tuple[HandRankings, list[Card]]]:
    ## test: 1,2,3,4,5,6,7... we get 3,4,5,6,7
    sorted_cards_acelow = add_ace_low(sorted_cards)
    max_consecutive = []
    for card in sorted_cards_acelow:
        if len(max_consecutive) == 5:
            return (HandRankings.STRAIGHT, set([ card.__str__() for card in max_consecutive ]))
        elif max_consecutive != []:
            if card.rank == max_consecutive[-1].rank - 1:
                max_consecutive.append(card)
            elif card.rank == max_consecutive[-1].rank:
                continue ## skip duplicates... this might conflict with straight flush if we skip the card that makes the flush
            else:
                max_consecutive = [card]
        else:
            max_consecutive = [card]
    return False

def get_flush(sorted_cards : list[Card]) -> Union[bool, tuple[HandRankings, list[Card]]]:
    suit_counts = {"S": set(), "H": set(), "C": set(), "D": set()}
    for card in sorted_cards:
        suit_counts[card.suit].add(card.__str__())
        if len(suit_counts[card.suit]) == 5:
            return (HandRankings.FLUSH, suit_counts[card.suit])
    return False

def get_straight_flush(sorted_cards : list[Card]) -> Union[bool, tuple[HandRankings, list[Card]]]:
    '''
    straight < flush < straight flush < royal flush
    '''
    # print(f"SORTED CARDS:")
    # pprint.pprint(sorted_cards)
    isFlush = get_flush(sorted_cards)
    isStraight = get_straight(sorted_cards)
    # print(f"IS FLUSH: {isFlush}")
    # print(f"IS STRAIGHT: {isStraight}")
    if (isFlush!=False and isStraight!=False):
        # check for straight flush, matching ranks only
        set_flush_ranks = set([card.split('_')[0] for card in isFlush[1]])
        set_straight_ranks = set([card.split('_')[0] for card in isStraight[1]])
        # print(f"SET FLUSH RANKS: {set_flush_ranks}")
        # print(f"SET STRAIGHT RANKS: {set_straight_ranks}")
        if set_flush_ranks == set_straight_ranks:
            # check for royal flush
            if set_straight_ranks == set(['TEN', 'JACK', 'QUEEN', 'KING', 'ACE']):
                return (HandRankings.ROYAL_FLUSH, isFlush[1])
            else:
                return (HandRankings.STRAIGHT_FLUSH, isFlush[1])
    elif isFlush!=False:
        return (HandRankings.FLUSH, isFlush[1])
    elif isStraight!=False:
        return (HandRankings.STRAIGHT, isStraight[1])
    return False
    


def get_best_hand(cards : list[Card]) -> tuple[HandRankings, list[Card]]:
    '''
    Returns the best hand from a list of cards, 
    both the HandRanking name and the actual cards to settle ties
    '''
    sorted_cards = sorted(cards, key=lambda x: x.rank.value, reverse=True)
    assert(len(sorted_cards) == 7)


    # Optimize by checking for max likelihood/lowest ranking hands first

    # high card vs pair vs three of a kind vs four of a kind
    best_hand_kinds, cards_in_hand_kinds = get_most_of_a_kind(sorted_cards)
    straight_flush = get_straight_flush(sorted_cards)

    print(f"BEST KINDS HANDS: {best_hand_kinds}")
    print(f" -- cards: {cards_in_hand_kinds}")

    if straight_flush==False:
        return best_hand_kinds, cards_in_hand_kinds

    else:
        print(f"STRAIGHT FLUSH: {straight_flush[0]}")
        print(f" -- cards: {straight_flush[1]}")
        if straight_flush[0] < best_hand_kinds:
            return straight_flush
        else:
            return best_hand_kinds, cards_in_hand_kinds
        

def get_winner(hands : dict[str, tuple[HandRankings, set[Card]]]) -> list[str]:
    '''
    Returns a list of sids of players with the best hand.
    hands = { sid : (hand_ranking, set[cards]) }
    cards contains copies of 5 board cards plus 2 player cards
    Handles ties by returning all players with the highest ranking hand
    '''
    # First find the maximum ranking
    min_ranking : HandRankings = min(hands.values(), key=lambda x: x[0])[0]
    
    print(f"MIN RANKING: {min_ranking}")
    # Return all players that have this ranking
    winners : list[str] = [sid for sid, (hand_ranking, cards) in hands.items() if hand_ranking == min_ranking]
    
    # break ties, if possible, by comparing cards and suits

    return winners

