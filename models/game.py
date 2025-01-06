from models.entities import Deck, Board, BoardStage, Player, PlayerBetResponse
from typing import List, Dict
from uuid import UUID
from models.definitions import PotState, PlayerBetResponse, BettingRoundRecord
import pprint
from pydantic import BaseModel


# both hand and pot state, and game logic can be separated into three classes?
# state class should have both hand and pot. 

NUM_PLAYERS = 5

# class State(BaseModel):
#     '''
#     Game logic. Keeps state. Keeps turns. 
#     State plays one Hand class at a time, sets turns, updates list of players, and player wealth. 

#     '''
#     players : List[Player] = [Player(i) for i in range(0, NUM_PLAYERS)]

#     def __init__(self, num_players : int, small_blind : int, big_blind : int) -> None:
#         # if someone who has less than others goes all in, then there are multiple pots.
#         # if there is a tie, the pot is divided. 
#         # now you need to think of a way in which you'd like to persist hand histories.
#         self.players : List[Player] = [Player(i) for i in range(0, num_players)]
        
#     # start the small blind at index 0
#     def start(): 
#         while(True):
#             # update players
#             # play hand
#             hand.play()
    



    
    #     '''{
    #     "pre-flop" : [
    #     {
    #         "<player_uui>" : {
    #         "role" : "sb",
    #         "price_to_call" : 20
    #         "action" : "call",
    #         "amount" : 20,
    #     }, 
    #     {
    #         "<player_uui>" : {
    #         "role" : "bb",
    #         "price_to_call" : 20
    #         "action" : "raise",
    #         "amount" : 20,
    #     }, 
    #     ]
    # }'''

# Game 
NUM_PLAYERS : int = 5
INITIAL_PLAYER_FUNDS : int  = 100
SB_AMOUNT : int = 20
BB_AMOUNT : int = 40



class Game(BaseModel):
    # variables
    rounds  : List[BoardStage] = [BoardStage.PREFLOP, BoardStage.FLOP, BoardStage.TURN, BoardStage.RIVER]
    players : List[Player] = [Player(pid = i, funds = INITIAL_PLAYER_FUNDS, betting_status = "active") for i in range(1, NUM_PLAYERS+1)]
    pot : Pot = Pot() # @TODO pending arguments
    sb_index : int = 0


    def play_hand(self):
        # Initialize clean Deck and Board
        deck = Deck()
        board = Board()

        for round in self.rounds:
            # 1) Show Board
            # 2) Betting Round 
            self.update_player_turns()
            self.pot.betting_round(self.players)


    def update_player_turns(self) -> List[Player]:
        '''copies the list starting at sb_index and wrapping around'''
        pass

            






            
# class Hand(BaseModel):

#     '''     
#     Acts as dealer: Creates a deck, deals cards to board and players
#     will need to take list[pleyrs] as a reference to update their cards. 
#     Also takes "TURN" for the index of the small blind starting 

#     '''
#     def __init__(self, sb_amount:int, players: List[Player], sb_player_id: UUID):
#         self.sb_amount = sb_amount   # Passed and updated every hand. 
#         self.players = players
#         self.sb_player_id = sb_player_id
#         # Initialized per Hand.
#         self.board : Board = Board()
#         self.deck : Deck = Deck()    
#         self.pot : Pot = Pot(sb_amount=sb_amount, players=players, sb_player_id =sb_player_id)


#     def start(self):
#         for player in self.players:
#             self.deck.deal_cards(player)

        
#         ## RUNS FOR STAGES PREFLOP, FLOP, TURN, RIVER.
#         while(self.board.next_stage()):
#             ## 1) render the board
#             print(self.board)
#             ## 2) await betting round. 
#             self.pot.betting_round() 
#             ## 3) update the board. 
#             self.deck.deal_cards(self.board)
        
#         ## 4) Determine winner. 
            
#     def persist_hand():
#         ''' saves hand data/state to database'''
#         pass




# class Hand(str, Enum):
#     '''
#     it should also have tie-breaking information
#     Each hand has a number associated with it. We use this number for breaking ties.
#     --Ex) Straight has the biggest number. In the event of two players having straights, 
#           the player whose straight hand has the maximum number wins.
#           Royal_flush has none. 
#           Straight Flush has largest number. 
#           Four_of_a_kind has the number. 
#           full_house has the triple number THEN the secondary number. 
#           flush has the suit ranks  
#           three of a kind the number 

#     '''


