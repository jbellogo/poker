from models.card_entities import Deck, Board, Player
from typing import List, Dict
from uuid import UUID


# both hand and pot state, and game logic can be separated into three classes?
# state class should have both hand and pot. 

NUM_PLAYERS = 5

class State(BaseModel):
    '''
    Game logic. Keeps state. Keeps turns. 
    State plays one Hand class at a time, sets turns, updates list of players, and player wealth. 

    '''
    players : List[Player] = [Player(i) for i in range(0, NUM_PLAYERS)]

    def __init__(self, num_players : int, small_blind : int, big_blind : int) -> None:
        # if someone who has less than others goes all in, then there are multiple pots.
        # if there is a tie, the pot is divided. 
        # now you need to think of a way in which you'd like to persist hand histories.
        self.players : List[Player] = [Player(i) for i in range(0, num_players)]
        


    # start the small blind at index 0
    def start(): 
        while(True):
            # update players
            # play hand
            hand.play()


class PreBetState(TypedDict):
    call_amount : int 
    check_allowed : bool
    minimum_raise : int
    pot_size : int
    



class Pot:
    '''
    Saves betting history in a single hand.
    awaits responses in methods betting_round()

    {
        
        "<player_uui>" : {
            "role" : "small_blind",
            "action" : "Call",
            "amount" : 20,
            "price_to_call" : 20
            }
    }


    '''
    pre_bet_state : PreBetState
    
    ## What does pot state look like?
    def __init__(self, sb_amount:int, players: List[Player], sb_player_id: UUID) -> None:
        self.players : List[Player] = players
        self.calling_amount : int = self.bb_amount


        self.pot_size : int

        # @TODO implement blinds 
        # self.sb_amount : int = sb_amount # player index? id # they ust be taken from them. 
        # self.bb_amount : int = sb_amount*2
        # self.sb_player_id: UUID = sb_player_id
        self.betting_history : Dict[BoardStage, List[IndividualBet]]


    def get_pre_bet_info(self) -> PreBetState:
        '''
        returns the necessary information about the pot state for any player to make a decision. 
        '''
        return self.pre_bet_state
    def update_pre_bet_state(self, last_action : PlayerBetResponse):

        {
        "call_amount" : self.calling_amount,
        "check_allowed" : True, #@TODO add logic
        "minimum_raise" : 2*self.calling_amount,         
        "pot_size" : self.pot_size
        # "small_blind_uuid" : self.sb_amount
    }


    

    async def betting_round(self):
        # go around once or as many times as there are raises!!!. 
        for player in self.players:
            response = await player.make_bet(self.pot) ## all changes are reflected on the pot. 
            self.pot_size += response.amount
            self.update_pre_bet_state(response)
            # if response_action == "raise":
            #     # everyone needs to call or raise.



        


            
class Hand(BaseModel):

    '''     
    Acts as dealer: Creates a deck, deals cards to board and players
    will need to take list[pleyrs] as a reference to update their cards. 
    Also takes "TURN" for the index of the small blind starting 

    '''
    def __init__(self, sb_amount:int, players: List[Player], sb_player_id: UUID):
        self.sb_amount = sb_amount   # Passed and updated every hand. 
        self.players = players
        self.sb_player_id = sb_player_id
        # Initialized per Hand.
        self.board : Board = Board()
        self.deck : Deck = Deck()    
        self.pot : Pot = Pot(sb_amount=sb_amount, players=players, sb_player_id =sb_player_id)


    def start(self):
        for player in self.players:
            self.deck.deal_cards(player)

        
        ## RUNS FOR STAGES PREFLOP, FLOP, TURN, RIVER.
        while(self.board.next_stage()):
            ## 1) render the board
            print(self.board)
            ## 2) await betting round. 
            self.pot.betting_round() 
            ## 3) update the board. 
            self.deck.deal_cards(self.board)
        
        ## 4) Determine winner. 
            
    def persist_hand():
        ''' saves hand data/state to database'''
        pass




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

