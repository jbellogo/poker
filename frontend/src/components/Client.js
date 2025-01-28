import { io } from 'socket.io-client';

class SocketIOClient {
    constructor(url = 'http://localhost:8765', userName, callbacks={}) {
        this.url = url;
        this.socket = null;
        this.callbacks = {
            onPlayerJoined: callbacks.onPlayerJoined || (() => {}),
            onGameState: callbacks.onGameState || (() => {}),
            onPlayerLeft: callbacks.onPlayerLeft || (() => {}),
            onConnectionError: callbacks.onConnectionError || (() => {})
        };
        this.connect(userName);
    }

    sendMessage(type, message) {
        if (this.socket && this.socket.connected) {
            this.socket.emit(type, message);
            console.log('Sent message:', message);
        } else {
            console.error('Socket.IO is not connected');
        }
    }

    handleMessage(data) {
        console.log('Received message:', data);
        // Handle different message types using callbacks.
        // Callback means that we define the function now in Game.jsx but don't call it until a message is received on SocketIOClient.
        switch (data.type) {
            case 'player_joined':
                this.callbacks.onPlayerJoined(data.payload);
                break;
            case 'game_state':
                this.callbacks.onGameState(data.payload);
                break;
            case 'player_left':
                this.callbacks.onPlayerLeft(data.payload);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    connect(userName) {
        // Will be called once. The first time a client connects.
        // Socket.io will handle re-connection.
        this.socket = io(this.url);

        const eventHandlers = {
            'connect': () => console.log('Connected to Socket.IO server'),
            'message': () => {
                console.log('Received message');
                this.handleMessage(data);
            },
            'disconnect': () => console.log('Disconnected from Socket.IO server'),
            'connect_error': (error) => {
                console.error('Socket.IO connection error:', error),
                this.callbacks.onConnectionError(error);
            },
            'connect_failed': (error) => console.error('Socket.IO connection failed:', error)
        };

        // Register all event handlers just to log them for development.
        Object.entries(eventHandlers).forEach(([event, handler]) => {
            this.socket.on(event, handler);
        });


    }


    close() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

export default SocketIOClient;