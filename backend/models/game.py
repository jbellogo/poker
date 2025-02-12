
from models.player import Player
from models.board import Board
from models.deck import Deck
from typing import List, Dict, Optional
from uuid import UUID
from models.definitions import *
import pprint
from models.config import *
from models.pot import Pot
from models.hands import get_best_hand, get_winner
import asyncio
import copy



class Game():
    def __init__(self, sio = None, seed : Optional[int] = None, max_players : int = MAX_PLAYERS, sb_amount : int = SB_AMOUNT, initial_player_funds : int = INITIAL_PLAYER_FUNDS):
        self.sio = sio # socketio server
        self.max_players = max_players
        self.sb_amount = sb_amount
        self.initial_player_funds = initial_player_funds

        # variables
        self.players : List[Player] = []
        self.pot : Pot = Pot(sb_amount=sb_amount)
        self.deck : Deck =  Deck(seed=seed)
        self.board : Board = Board()
        self.hand_history : Dict[str, List[BettingRoundRecord]] = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 

    
    def add_player(self, sid: str, player_name: str):
        self.players.append(
            Player(name = player_name,
                   pid = len(self.players)+1, 
                   sid = sid, 
                   funds = self.initial_player_funds))

    def clear_board(self):
        self.deck : Deck = Deck()
        self.deck.initialize()
        self.board : Board = Board()


    def update_player_turns(self) -> None:
        '''
        shifts the players list to the left, 
        effectively updating the sb_index.
        sb_index remains 0 throughout.
        '''
        self.players.append(self.players.pop(0))


    def persist_player_action(self, response: PlayerBetResponse, game_state: GameState, player_state: PlayerState) -> None:        
        betting_record = BettingRoundRecord(sid= response['sid'], 
                                            response=response, 
                                            game_state=game_state,
                                            player_state=player_state) 
        stage : str = game_state['board']['stage']
        self.hand_history[stage].append(betting_record)


    def remove_player(self, sid: str) -> None:
        self.players = [player for player in self.players if player.get_sid() != sid]

    def get_hand_history(self):
        return self.hand_history

    def persist_betting_round(self):
        pass

    def initialize_hand(self):
        '''
        Initialize the hand, ie blinds, cards, etc.
        Once per hand, ie one PREFLOP, FLOP, TURN, RIVER cycle
        ASSUMES TURNS ARE ALREADY UPDATED
        '''
        # clear board
        self.clear_board()

        # set roles
        for i, player in enumerate(self.players):
            if i == 0: 
                player.set_role("sb")
                player.collect_blind(self.sb_amount)
            elif i==1: 
                player.set_role("bb")
                player.collect_blind(self.sb_amount)
            else: 
                player.set_role("other")
            # deal cards
            self.deck.deal_cards(player)

        # collect blinds
        self.pot.collect_blinds(self.sb_amount)

        # start at player #3
        self.update_player_turns()
        self.update_player_turns()



    def initialize_betting_round(self, board_stage : BoardStage):
        '''
        initialize pot and board.
        '''
        self.pot.initialize(board_stage)
        self.board.set_stage(board_stage)
        self.deck.deal_cards(self.board)




    def get_state(self) -> GameState:
        '''
        Returns a Game state for the player with his personalized call amount. 
        '''
        pot : PotState = self.pot.get_state()
        board : BoardState = self.board.get_state()
        return copy.deepcopy(GameState(pot= pot, board=board))



    def get_players_to_call(self) -> int:
        '''
        Returns the number of players to call.
        Since this is used after a raise, isnt it just active players - 1?
        '''
        players = []
        for player in self.players:
            if player.get_betting_status() == "active":
                # print(f"player {player.get_id()} bet total: {player.get_bet_total()} ==? {self.pot.get_state()['call_total']}")
                if player.get_bet_total() != self.pot.get_state()['call_total']:
                    players.append(player)
        return players
    


    async def betting_round(self, board_stage : BoardStage) -> None:  
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        Updates player status from action response, ie all-in, folded, etc.
        '''
        # print(f"\n---------STARTING BETTING ROUND {board_stage}")
        players_to_call = [player for player in self.players if player.get_betting_status() == "active"]
        # set turn order

        # print(f"players_to_call: {[player.get_id() for player in players_to_call]}")
        while len(players_to_call) > 0:


            # print(f"pot state: {self.pot.get_state()}")
            for i, player in enumerate(players_to_call):
                # print(f"\nplayer {player.get_id()} status: {player.get_betting_status()}")

                # get player action
                state : GameState = self.get_state()
                response : Optional[PlayerBetResponse] = await player.make_bet(state)
                self.persist_player_action(response, state, player.get_state())

                # update pot state
                last_action = response['action']
                # print(f" --- action: {last_action}")
                last_player_total = player.get_bet_total()
                next_player_total = players_to_call[(i+1)%len(players_to_call)].get_bet_total()
                self.pot.update_pot_state(last_action=response, last_player_total=last_player_total, next_player_total=next_player_total)
            players_to_call = self.get_players_to_call()
            
        self.persist_betting_round()
        await asyncio.sleep(0.1)  ## might be necessary until we have the calls


    async def play_hand(self):
        # Initialize clean Deck and Board
        self.initialize_hand()

        for round in ["PREFLOP", "FLOP", "TURN", "RIVER"]:
            self.initialize_betting_round(round)
            # 1) Emit Board State
            self.board.show()  ## Once we have a frontend, this game logic will go there. 

            # 2) Betting Round 
            await self.betting_round(round) 

        self.update_player_turns()
        winners = self.determine_winner()
        print(f"winners: {winners}")
        # self.pay_winners(winners)



    def get_player_state(self, sid):
        for player in self.players:
            if player.get_sid() == sid:
                return player.get_state()


    def determine_winner(self) -> list[str]:
        hands = {}
        active_players = [player for player in self.players if player.get_betting_status() == "active"]
        print(f"board cards: {self.board.get_cards()}")
        for player in active_players:
            print(f"player {player.get_id()} cards: {player.get_cards()}")
            hands[player.get_sid()] = get_best_hand(player.get_cards() + self.board.get_cards())
        winners = get_winner(hands)
        # self.pot.reset()
        return winners


    def start(self):
        # # maybe handle lobby here
        # while True:
        #     if len(self.players) >= 2:
        #         self.initialize_hand()
        #         self.play_hand()
        pass


    def handle_player_action(self, sid, data):
        '''
        Interacts with the socketio server to handle player actions.
        '''
        type = data['type']
        if type == 'hero_join_request':
            if len(self.players)+1 < MAX_PLAYERS:
                self.add_player(sid, data['name'])
                # Sent to hero, with his information.
                self.sio.emit('message', {"type": "hero_join_success", 'data' : self.get_player_state(sid)}, to=sid)
                # Sent to all other players, with the updated list of players.
                players_public_info = [player.get_state()['public_info'] for player in self.players]
                self.sio.emit('message', {"type": "new_player_join", "players" : players_public_info})

            else:
                self.sio.emit('message', {"type": "player_join_failure", "message": "Game is full"}, to=sid)
                self.sio.disconnect(sid)