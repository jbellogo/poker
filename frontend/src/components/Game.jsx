import React from 'react';
import './Game.css';
import { ActivePlayer, RegularPlayer } from './player';
import SocketIOClient from './Client';

const client = new SocketIOClient();

const sendMessage = () => {
    client.sendMessage('message', { type: 'test_message', content: 'Hello Server!' });
}

const Game = () => {
    // const [client, setClient] = React.useState(null);

    // React.useEffect(() => {
    //     // Create WebSocket client when component mounts
    //     const wsClient = new WebSocketClient();

    //     // Set up any event listeners here
    //     // Example:
    //     wsClient.sendMessage({ type: 'message', content: 'Hello Server!' });

    //     // Store the client in state
    //     setClient(wsClient);

    //     // Cleanup function to close connection when component unmounts
    //     return () => {
    //         if (wsClient) {
    //             wsClient.close();
    //         }
    //     };
    // }, []); // Empty dependency array means this runs once on mount


    return (
    <div>
        <h1 className='title'>Online Poker</h1>
        <button onClick={sendMessage}>Send MEssage</button>


        {/* Game container starts here */}
        <div className="game-container">
            <div className="table-container">
                <RegularPlayer name="John Cena" id={2} funds={1000} bet={100} action="CALL" />
                <RegularPlayer name="Tony Romo" id={3} funds={1000} bet={100} action="CALL" />
                <RegularPlayer name="Lila" id={4} funds={1000} bet={0} action="FOLD" />
                <RegularPlayer name="Maria" id={5} funds={1000} bet={100} action="CALL" />
                <ActivePlayer name="Me" id={1} funds={1000} bet={100} action="CALL" />
            </div>
        </div>
      </div>
    );
  };

export default Game;