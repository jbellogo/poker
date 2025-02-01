import socketio
import eventlet
import json
from models import Game

## The Server will own a Game object. It will pass messages to the game object to handle.
'''
This is how I want to store player info.
This is player state. 
{sid1: {
    "public_info": {
        "name": str,
        "pid": int,
        "sid": str,
        "funds": int,
        "role": PlayerRole,
        "last_action": "call",
        "last_action_amount:" "100",
        "betting_status": PlayerStatus,
    },
    "private_info": {
        "hand": Tuple[Card, Card],
    }
},
}

{type:‘hero_join_request’,  name:”John Cena”}
'''




class WebsocketServer:
    def __init__(self, port=8765, host='localhost'):
        
        # Create Socket.IO server
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.port = port
        self.host = host
        self.connected_clients = set() 
        ## Set of uuids, can lookup player state through game object since, 
        # for better separation of cencerns, game object will own the full player state.
        
        # Register event handlers
        self.sio.on('connect', self.connect)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('message', self.message)

        # Game specific handlers
        self.game = Game(sio=self.sio)

    def connect(self, sid, environ):
        # sid: session_id
        """
        Handle client connection
        Whats the first thing that should happen when a client connects? 
        they should send their name
        ws://localhost:8765/connect
        """
        print(f"Client connected: {sid}")
        self.connected_clients.add(sid) ## Player logic is handled once they connect.


    def disconnect(self, sid):
        """Handle client disconnection"""
        print(f"Client disconnected: {sid}")
        self.connected_clients.remove(sid)
        self.game.remove_player(sid) # Important to keep avaliable spots updated.

    def message(self, sid, data):
        """Handle incoming messages"""
        try:
            print(f"received message from {sid}: {data}", flush=True)  # Force flush
            self.game.handle_player_action(sid, data)
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e)
            }
            self.sio.emit('message', error_response, to=sid)

    def start(self):
        """Start the WebSocket server"""
        print(f"Socket.IO server starting on port {self.port}")
        eventlet.wsgi.server(eventlet.listen((self.host, self.port)), self.app)

if __name__ == '__main__':
    server = WebsocketServer()
    server.start()
