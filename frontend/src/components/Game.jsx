import React from 'react';
import './Game.css';
import { ActivePlayer, RegularPlayer } from './player';
import SocketIOClient from './Client';


// When you open the page, you see the welcome-screen. When you click, "join game", you see the game-screen.


// Where do I put this?
const client = new SocketIOClient();

const sendMessage = () => {
    client.sendMessage('message', { type: 'test_message', content: 'Hello Server!' });
}

const playerJoin = () => {
    client.sendMessage('player_join', { type: 'player_join', content: {name: "Me", id: 1, funds: 1000} });
}


const Game = () => {
    // Should I put this in the App component directly?
    const [showGame, setShowGame] = useState(false);  // Add this state

    // Add this handler function
    const handleGameStart = () => {
        setShowGame(true);
        playerJoin();  // Assuming you want to call this when joining
    };

    return (
        <div>
            <h1 className='title'>Online Poker</h1>
            {!showGame ? (
                <Welcome onGameStart={handleGameStart} />
            ) : (
                // ... existing game container code ...
                <div className="game-container">
                    <div className="table-container">
                        <RegularPlayer name="John Cena" id={2} funds={1000} bet={100} action="CALL" />
                        <RegularPlayer name="Tony Romo" id={3} funds={1000} bet={100} action="CALL" />
                        <RegularPlayer name="Lila" id={4} funds={1000} bet={0} action="FOLD" />
                        <RegularPlayer name="Maria" id={5} funds={1000} bet={100} action="CALL" />
                        <ActivePlayer name="Me" id={1} funds={1000} bet={100} action="CALL" />
                    </div>
                </div>
            )}
        </div>
    );
};

export default Game;