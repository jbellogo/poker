from models.card_entities import Deck, Board, BoardStage
from models.player_entitites import Player, PlayerBetResponse, PotState
from typing import List, Dict
from uuid import UUID


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






class BettingState:
    def __init__(self, call_amount : int):
        self.call_amount : int = call_amount
        self.check_allowed : bool = False
        self.minimum_raise : int = call_amount*2

    def get_json(self):
        return {
            "call_amount" : self.call_amount,
            "check_allowed": self.check_allowed,
            "minimum_raise": self.minimum_raise,
             # "small_blind_uuid" : self.sb_amount

        }
    def update(self, action : PlayerBetResponse):
        self.call_amount = action.amount_bet  ##
        self.check_allowed = False if action.action == "raise" else True, ## @TODO what about the first time around?
        self.minimum_raise = 2*action.amount_bet  ##

    



class Pot():
    '''
    Saves betting history in a single hand.
    awaits responses in methods betting_round()

    {
        "pre-flop" : [
        {
            "<player_uui>" : {
            "role" : "sb",
            "price_to_call" : 20
            "action" : "call",
            "amount" : 20,
        }, 
        {
            "<player_uui>" : {
            "role" : "bb",
            "price_to_call" : 20
            "action" : "raise",
            "amount" : 20,
        }, 
        ]
    }
    '''   
    
    def __init__(self, bb_amount:int, players: List[Player]): #, sb_player_indx: int) -> None:
        self.players : List[Player] = players
        self.betting_state = BettingState(call_amount = bb_amount)
        self.pot_size : int = 0
        self.hand_history = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]}

        # @TODO implement blinds 
        # self.sb_amount : int = sb_amount # player index? id # they ust be taken from them. 
        # self.bb_amount : int = sb_amount*2
        # self.sb_player_id: UUID = sb_player_id


    def get_pot_state(self) -> PotState:
        '''
        returns the necessary information about the pot state for any player to make a decision. 
        '''
        state = self.betting_state.get_json()
        state['pot_size'] = self.pot_size
        return PotState(state)
    
    def update_pot_state(self, last_action : PlayerBetResponse):
        self.pot_size += last_action.amount_bet
        self.betting_state.update(last_action)


    # async def betting_round(self):
    #     # go around once or as many times as there are raises!!!. 
    #     for player in self.players:
    #         response = await player.make_bet(self.pot) ## all changes are reflected on the pot. 
    #         self.pot_size += response.amount
    #         self.update_pre_bet_state(response)
            # if response_action == "raise":
            #     # everyone needs to call or raise.


    def betting_round(self, board_stage : BoardStage):
        '''pass the small blind index and amount here'''
        ## Assume players has only active players ... how do we keep track if they fold, or go al in? a special, iterable data struture
        active_players = len(self.players)
        players_to_call = active_players

        while players_to_call != 0:
            for player in self.players:
                if players_to_call == 0:
                    break
                if player.hand_status() == "active":
                    # print(f"\nplayers_to_call = {players_to_call}")
                    # print(f"active_players = {active_players}")

                    response : PlayerBetResponse = player.make_bet(self.betting_state) # needs to be awaited
                    ## response has a pot_state.. it should not have one asigned until we are ready to save it. 
                    self.update_pot_state(response)
                    response.pot_state = self.betting_state ## HERE 

                    player_action =  response.action
                    if  player_action == "raise":
                        players_to_call = active_players-1 # all active players
                    if player_action == "fold":
                        players_to_call-=1
                        active_players-=1
                        player.set_status("fold")
                    if player_action == "call":
                        players_to_call -=1
                    
                    player_id = "player" + str(response.pid)
                    self.hand_history[board_stage.name].append({player_id : response})

            
        print("betting round over!")
        self.persist_betting_round()

    def persist_betting_round(self):
        pass

    def get_hand_history(self):
        return self.hand_history
    
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

#     ROYAL_FLUSH = "royal_flush"
#     STRAIGHT_FLUSH = "straight_flush"
#     FOUR_OF_A_KIND = "four_of_a_kind"
#     FULLHOUSE = "full_house"
#     FLUSH = "flush"
#     STRAIGHT = "straight"
#     THREE_OF_A_KIND = "three_of_a_kind"
#     TWO_PAIR = "two_pair"
#     PAIR = "pair"
#     HIGH_CARD = "high_card"

