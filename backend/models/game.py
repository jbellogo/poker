
from models.player import Player
from models.board import Board
from models.deck import Deck
from typing import List, Dict, Optional
from uuid import UUID
from models.definitions import *
import pprint
from models.config import * # Global variables, better practice to use json.
from models.pot import Pot
import asyncio
import copy



class Game():
    def __init__(self, sio = None, max_players : int = MAX_PLAYERS, sb_amount : int = SB_AMOUNT, initial_player_funds : int = INITIAL_PLAYER_FUNDS):
        self.sio = sio # socketio server
        self.max_players = max_players
        self.sb_amount = sb_amount
        self.initial_player_funds = initial_player_funds

        # variables
        self.players : List[Player] = []
        self.pot : Pot = Pot(sb_amount=sb_amount)
        self.deck : Deck =  Deck()
        self.board : Board = Board()
        self.rounds : List[BoardStage] = ["PREFLOP", "FLOP", "TURN", "RIVER"]
        self.hand_history : Dict[str, List[BettingRoundRecord]] = {"PREFLOP": [], "FLOP":[], "TURN":[], "RIVER":[]} 
        # self.initialize_hand() # Cannot be done on an empty player list.

    
    def add_player(self, sid: str, player_name: str):
        self.players.append(
            Player(name = player_name,
                   pid = len(self.players)+1, 
                   sid = sid, 
                   funds = self.initial_player_funds))

    def clear_board(self):
        self.deck : Deck = Deck()
        self.board : Board = Board()


    def update_player_turns(self) -> None:
        '''
        shifts the players list to the left, 
        effectively updating the sb_index.
        sb_index remains 0 throughout.
        '''
        # @TODO this will give us problems in keeping blinds across hand cycles.
        self.players.append(self.players.pop(0)) # one at a time.


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
        resetting their amount bet this hand to 0.
        '''
        # some of this shuold be done once per hand, some of this once per betting round.
        self.pot.initialize(board_stage)
        self.board.initialize(board_stage, self.deck)
        # for player in self.players:
        #     player.reset_bet_total()  # this is initializing blinds.



    def get_state(self) -> GameState:
        '''
        Returns a Game state for the player with his personalized call amount. 
        '''
        pot : PotState = self.pot.get_state()
        board : BoardState = self.board.get_state()
        return GameState(pot= pot, board=board)



    def get_players_to_call(self) -> int:
        '''
        Returns the number of players to call.
        Since this is used after a raise, isnt it just active players - 1?
        '''
        # count : int = 0
        players = []
        for player in self.players:
            if player.get_betting_status() == "active":
                # print(f"player {player.get_id()} bet total: {player.get_bet_total()} ==? {self.pot.get_state()['call_total']}")
                if player.get_bet_total() != self.pot.get_state()['call_total']:
                    players.append(player)
        return players
    

    # def update_lim(self, turn : int, lim : int, last_action : PlayerAction) -> int:
    #     additional_turns = 0
    #     if last_action == "raise" or last_action == "all-in":
    #         additional_turns = self.get_players_to_call()
    #         return turn + additional_turns + 1
    #     # elif last_action == "fold":
    #     #     return lim + 1
    #     return lim # the original number of turns



    async def betting_round(self, board_stage : BoardStage) -> None:  
        '''
        Single betting round ie preflop or flop or etc. 
        Awaits active player actions
        Updates player status from action response, ie all-in, folded, etc.
        '''
        self.initialize_betting_round(board_stage)
        # print(f"\n---------STARTING BETTING ROUND {board_stage}")
        players_to_call = [player for player in self.players if player.get_betting_status() == "active"]
        # set turn order

        # print(f"players_to_call: {[player.get_id() for player in players_to_call]}")
        while True:
            if len(players_to_call) == 0:
                break

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
        self.clear_board()
        for player in self.players:
            self.deck.deal_cards(player)

        for round in self.rounds:
            self.board.set_round(round)
            self.deck.deal_cards(self.board)

            # 1) Show Board
            self.board.show()  ## Once we have a frontend, this game logic will go there. 
            # 2) Betting Round 

            await self.betting_round(round) 
            # Awaits player responses and uploads pot and player status. 
            # This should update the pot and this should be made visible in real time. 
        self.update_player_turns() # responsible for this
        self.determine_winner()

    

    def get_player_state(self, sid):
        for player in self.players:
            if player.get_sid() == sid:
                return player.get_state()


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

    def start(self):
        pass

    def determine_winner(self):
        pass

        
       
