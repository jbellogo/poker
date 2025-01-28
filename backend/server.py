import socketio
import eventlet
from models import Game

## The Server will own a Game object. It will pass messages to the game object to handle.

class WebsocketServer:
    def __init__(self, port=8765, host='localhost'):
        # Create Socket.IO server
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.port = port
        self.host = host
        self.connected_clients = set()
        
        # Register event handlers
        self.sio.on('connect', self.connect)
        self.sio.on('disconnect', self.disconnect)
        self.sio.on('message', self.message)

        # Game specific handlers
        self.game = Game()

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

    def message(self, sid, data):
        """Handle incoming messages"""
        try:
            # Process message and create response
            response = {
                "status": "success",
                "message": f"Received: {data}"
            }
            # Send response back to client
            self.sio.emit('message', response, to=sid)
            print(f"received message from {sid}: {data}")
            # Optionally broadcast to all other clients
            # self.sio.emit('message', response, skip_sid=sid)
            
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
