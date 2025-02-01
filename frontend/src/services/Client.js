// Websocket client.

import { io } from 'socket.io-client';


class SocketIOClient {
    constructor(url = 'http://localhost:8765', userName, callbacks={}) {
        this.url = url;
        this.socket = null;
        this.callbacks = {
            onHeroJoined: callbacks.onHeroJoined || (() => {}),
            onOpponentJoined: callbacks.onOpponentJoined || (() => {}),
            onConnectionError: callbacks.onConnectionError || (() => {}),
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
        if (data != null) {
            // Handle different message types using callbacks.
            // Callback means that we define the function now in Game.jsx but don't call it until a message is received on SocketIOClient.
            switch (data.type) {
                case 'hero_join_success':
                    this.callbacks.onHeroJoined(data.data);
                    break;
                case 'new_player_join':
                    this.callbacks.onOpponentJoined(data.players);
                    break;
                default:
                    console.log('Unknown message type:', data.type);
            }
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
                this.sendMessage({ type: 'hero_join_request', name: userName });
            })
            .on('message', (data) => {
                console.log('Received message');
                this.handleMessage(data);
            })
            .on('disconnect', (error) => {
                console.log('Disconnected from Socket.IO server', error);
                this.callbacks.onConnectionError(error);
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