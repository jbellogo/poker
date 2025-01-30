// Websocket client.

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

    sendMessage(payload) {
        if (this.socket && this.socket.connected) {
            this.socket.emit('message', payload); // Turns out this 'message' argument is important
            console.log('Sent message:', payload);
        } else {
            console.error('Socket.IO is not connected');
        }
    }

    handleMessage(data) {
        console.log('Received message:', data);
        // Handle different message types using callbacks.
        // Callback means that we define the function now in Game.jsx but don't call it until a message is received on SocketIOClient.
        switch (data.type) {
            case 'player_join_success':
                this.callbacks.onPlayerJoined(data.data);
                break;
            case 'game_state':
                this.callbacks.onGameState(data.data);
                break;
            case 'player_left':
                this.callbacks.onPlayerLeft(data.data);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    connect(userName) {
        // Will be called once. The first time a client connects.
        // Socket.io will handle re-connection.
        this.socket = io(this.url);
        this.socket
            .on('connect', () => {
                console.log('Connected to Socket.IO server');
                console.log('Sending player join request to server');
                this.sendMessage({ type: 'player_join_request', name: userName });
            })
            .on('message', (data) => {
                console.log('Received message');
                this.handleMessage(data);
            })
            .on('disconnect', (data) => {
                console.log('Disconnected from Socket.IO server');
            })
            .on('connect_error', (error) => {
                console.error('Socket.IO connection error:', error);
                this.callbacks.onConnectionError(error);
            })
            .on('connect_failed', (error) => console.error('Socket.IO connection failed:', error));


    }


    close() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

export default SocketIOClient;