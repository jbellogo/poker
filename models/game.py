from models.entities import Deck, Board, BoardStage, Player, PlayerBetResponse
from typing import List, Dict
from uuid import UUID
from models.definitions import PotState, PlayerBetResponse, BettingRoundRecord
import pprint

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
    


class Pot():
    '''
    Saves betting history in a single hand.
    awaits responses in methods betting_round()
    Gets Updated after every single player action. how would MVC design work?
    {
        "pre-flop" : [
            {
                "<player_id>" : {
                        "record" :
                "role" : "sb",
                "price_to_call" : 20
                "action" : "call",
                "amount" : 20,
            }
        ]
    }
    '''   

    def __init__(self, bb_amount:int, players: List[Player], sb_index: int = 0): 
        self.players : List[Player] = players
        self.pot_state : PotState = PotState(call_amount = bb_amount,
                                             check_allowed=False,
                                            minimum_raise=2*bb_amount,
                                            pot_size=0) ## Initial default. 
        self.hand_history = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 

        # @TODO implement blinds 
        self.sb_amount : int = bb_amount/2 # player index? id # they ust be taken from them. 
        self.bb_amount : int = bb_amount
        self.sb_player_index: int = sb_index


    def get_pot_state(self) -> PotState:
        '''
        returns the necessary information about the pot state for any player to make a decision. 
        '''
        return self.pot_state
    
    def update_pot_state(self, last_action : PlayerBetResponse, board_stage : BoardStage):
        print("LAST PLAYER ACTION: ")
        print(last_action)
        action : str = last_action['action']
        amount : int = last_action['amount_bet']
        self.pot_state['pot_size'] += amount
        # print(board_stage)
        # print(last_action)
        # Basically everytime there is a raise, we should update check_allowed and call_amount
        # Initially:
        if board_stage == BoardStage.PREFLOP:
            self.pot_state['check_allowed'] = False

        else:
            pass # check = True <-> turn = 1, Smallblind. After that look at past action

        # When is checking allowed? if board_stage is advanced and everyone has checked.
        
        # Fine tunning:
        if action == 'raise':
            self.pot_state['check_allowed'] = False
            self.pot_state['call_amount'] = amount
            self.pot_state['minimum_raise'] = 2*amount


    def overwrite_pot_state(self, new_pot_state : PotState):
        self.pot_state = new_pot_state

    def get_tailored_pot_state(self, player : Player):
        pot_copy = self.pot_state.copy()
        pot_copy['call_amount'] -= player.amount_bet_this_hand() # updates
        return pot_copy

    def betting_round(self, board_stage : BoardStage, sb_index : int):
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        @TODO NOW: SMALL AND BIG BLIND AND TURNS!!!!
        @TODO pass the small blind index and amount here'''
        active_players = len(self.players)
        players = [self.players[i%active_players] for i in range(sb_index, 2*active_players-sb_index)]
        pprint.pprint(players)

        active_players = len(self.players)
        players_to_call = active_players
        while players_to_call != 0:
            for player in self.players:
                if players_to_call == 0:
                    break
                if player.hand_status() == "active":
                    # print(f"\nplayers_to_call = {players_to_call}")
                    # print(f"active_players = {active_players}")
                    pot_copy = self.get_tailored_pot_state(player)
                    # the tailored pot state is sent to player with their respective call price. 
                    response : PlayerBetResponse = player.make_bet(pot_copy) # needs to be awaited. 
                    player_id = "player" + str(response['pid'])
                    betting_record = BettingRoundRecord(response=response, pot_state=pot_copy)
                    self.hand_history[board_stage.name].append({player_id : betting_record} )
                    ### THEN WE UPDATE. this way we store the pot_state at the time before the player makes his move
                    self.update_pot_state(response, board_stage)
                    player_action =  response['action']
                    if  player_action == "raise":
                        players_to_call = active_players-1 # all active players
                    elif player_action == "fold":
                        players_to_call-=1
                        active_players-=1
                        player.set_status("fold")
                    elif player_action == "call" or player_action == "check":
                        players_to_call -=1
                    
                    
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

class Game:
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


