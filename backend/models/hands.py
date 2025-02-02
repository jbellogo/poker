# '''
# Hand validation.
# take full board and cards from an active player -> compute highest ranking 5 card hand.
# Do that for all active players to determine winner.
# How to organize this validation? 
# '''



# # class Hand(str, Enum):
# #     '''
# #     it should also have tie-breaking information
# #     Each hand has a number associated with it. We use this number for breaking ties.
# #     --Ex) Straight has the biggest number. In the event of two players having straights, 
# #           the player whose straight hand has the maximum number wins.
# #           Royal_flush has none. 
# #           Straight Flush has largest number. 
# #           Four_of_a_kind has the number. 
# #           full_house has the triple number THEN the secondary number. 
# #           flush has the suit ranks  
# #           three of a kind the number 

# #     '''
# from enum import Enum
# from typing import TypedDict

# class PlayerRole(str, Enum):
#     SMALL_BLIND = 'sb'
#     BIG_BLIND = 'bb'
#     OTHER = 'other'

# class PlayerAction(str, Enum):
#     CALL = 'call'
#     RAISE = 'raise'
#     FOLD = 'fold'
#     CHECK = 'check'
#     ALLIN = 'all-in'
#     NO_ACTION = 'no-action'


# class PlayerBetResponse(TypedDict):
#     role : PlayerRole
#     action : PlayerAction

# role = PlayerRole('sb')
# action = PlayerAction('call')

# resp = PlayerBetResponse(role=role, action=action)

# print(resp)