import socketio
import eventlet

# Create Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Store connected clients (optional, if you need to track them)
connected_clients = set()

@sio.event
def connect(sid, environ):
    """Handle client connection"""
    print(f"Client connected: {sid}")
    connected_clients.add(sid)

@sio.event
def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client disconnected: {sid}")
    connected_clients.remove(sid)

@sio.event
def message(sid, data):
    """Handle incoming messages"""
    try:
        # Process message and create response
        response = {
            "status": "success",
            "message": f"Received: {data}"
        }
        # Send response back to client
        sio.emit('message', response, to=sid)
        print(f"received message from {sid}: {data}")
        # Optionally broadcast to all other clients
        # sio.emit('message', response, skip_sid=sid)
        
    except Exception as e:
        error_response = {
            "status": "error",
            "message": str(e)
        }
        sio.emit('message', error_response, to=sid)

if __name__ == '__main__':
    # Start the server
    port = 8765
    print(f"Socket.IO server starting on port {port}")
    eventlet.wsgi.server(eventlet.listen(('localhost', port)), app)
