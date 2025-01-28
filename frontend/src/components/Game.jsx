import React, { useState, useEffect, useCallback } from 'react';
import './Game.css';
import { ActivePlayer, RegularPlayer } from './player';
import SocketIOClient from './Client';

// When you open the page, you see the welcome-screen. When you click, "join game", you see the game-screen.


// @TODO Eventually will rename this to MultiplePlayerGame to differentiate from SinglePlayerGame agains the AI.
const Game = (props) => {
    const [connectionError, setConnectionError] = useState(false);
    const [players, setPlayers] = useState([]);
    const [gameState, setGameState] = useState(null);
    
    // Define callbacks using useCallback to maintain reference stability
    const handleConnectionError = useCallback((error) => {
        setConnectionError(error);    
    }, []);

    const handlePlayerJoined = useCallback((payload) => {
        setPlayers(prevPlayers => [...prevPlayers, payload]);
    }, []);

    const handleGameState = useCallback((payload) => {
        setGameState(payload);
    }, []);

    const handlePlayerLeft = useCallback((payload) => {
        setPlayers(prevPlayers => 
            prevPlayers.filter(player => player.id !== payload.id)
        );
    }, []);

    // Initialize socket client with callbacks
    useEffect(() => {
        const socketClient = new SocketIOClient(
            'http://localhost:8765',
            props.userName,
            {
                onPlayerJoined: handlePlayerJoined,
                onGameState: handleGameState,
                onPlayerLeft: handlePlayerLeft,
                onConnectionError: handleConnectionError
            }
        );

        // Cleanup on unmount
        return () => {
            socketClient.close();
        };
    }, [handlePlayerJoined, handleGameState, handlePlayerLeft, handleConnectionError, props.userName]);




    // This is the main render function.
    return (
        <>
            {/* // We can add some conditional rendering here to handle the connection error. */}

        {connectionError ? (
            <div className="error-container">
                <h2>Connection Error</h2>
                <p>Unable to connect to the game server. Please try again later.</p>
            </div>
        ) : (
            <div className="game-container">
                <div className="table-container">
                    {/* @TODO: we will only be using the GameState message to render all this */}
                    <RegularPlayer name="John Cena" id={2} funds={1000} bet={100} action="CALL" />
                    <RegularPlayer name="Tony Romo" id={3} funds={1000} bet={100} action="CALL" />
                    <RegularPlayer name="Lila" id={4} funds={1000} bet={0} action="FOLD" />
                    <RegularPlayer name="Maria" id={5} funds={1000} bet={100} action="CALL" />
                    <ActivePlayer name={props.playerName} id={1} funds={1000} bet={100} action="CALL" />
                </div>
            </div>
        )}
    </>
    )
}

export default Game;