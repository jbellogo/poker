import React, { useState, useEffect, useCallback } from 'react';
import '../styles/Game.css';
import Hero from './Hero';
import Opponent from './Opponent';
import SocketIOClient from '../services/Client';

// When you open the page, you see the welcome-screen. When you click, "join game", you see the game-screen.


// @TODO Eventually will rename this to MultiplePlayerGame to differentiate from SinglePlayerGame agains the AI.
const Game = (props) => {
    const [connectionError, setConnectionError] = useState(false);
    const [players, setPlayers] = useState([]); // Use this. Contains other players public information.
    const [thisPlayer, setThisPlayer] = useState(null); // Use this. Contains the this players public and private information.
    const [board, setBoard] = useState([]); 
    // need to draw out the schemas, gamestate in python already has list of player and many more things.

    // Define callbacks using useCallback to maintain reference stability
    const handleConnectionError = useCallback((error) => {
        setConnectionError(true);    
    }, []);

    const handlePlayerJoined = useCallback((data) => {
        console.log("handlePlayerJoined", data);
        setPlayers(prevPlayers => [...prevPlayers, data.public_info]);
        setThisPlayer({
            ...data.public_info,
            cards: data.private_info.cards
        });
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
            // make this into a component for readability.
            <div className="error-container">
                <h2>Connection Error</h2>
                <p>Unable to connect to the game server. Please try again later.</p>
            </div>
        ) : (
            // make this into a component for readability.
            <div className="game-container">
                <div className="table-container">
                    {/* @TODO: we will only be using the GameState message to render all this */} 
                    {players.map(player => (
                            player.id !== thisPlayer?.id && (
                                <Opponent
                                    key={player.id}
                                    name={player.name}
                                    id={player.id}
                                    funds={player.funds}
                                    bet={player.bet}
                                    action={player.action}
                                />
                            )
                        ))}
                        {/* Render Hero component for the current player */}
                        {console.log("thisPlayer", thisPlayer)}
                        {thisPlayer && (
                            <Hero
                                name={thisPlayer.name}
                                id={thisPlayer.id}
                                funds={thisPlayer.funds}
                                bet={thisPlayer.bet}
                                action={thisPlayer.action}
                            />
                        )}
                </div>
            </div>
        )}
    </>
    )
}

export default Game;