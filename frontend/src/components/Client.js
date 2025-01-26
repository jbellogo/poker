import { io } from 'socket.io-client';

class SocketIOClient {
    constructor(url = 'http://localhost:8765') {
        this.url = url;
        this.socket = null;
        this.connect();
    }

    connect() {
        this.socket = io(this.url);

        this.socket.on('connect', () => {
            console.log('Connected to Socket.IO server');
        });

        this.socket.on('message', (data) => {
            console.log('Received message:', data);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from Socket.IO server');
        });

        this.socket.on('connect_error', (error) => {
            console.error('Socket.IO connection error:', error);
        });
    }

    sendMessage(type, message) {
        if (this.socket && this.socket.connected) {
            this.socket.emit(type, message);
            console.log('Sent message:', message);
        } else {
            console.error('Socket.IO is not connected');
        }
    }

    close() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

export default SocketIOClient;