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
    const [hero, setHero] = useState(null); // Use this. Contains the this players public and private information.
    const [board, setBoard] = useState([]); 
    
    useEffect(() => {
        // Move callback definitions inside useEffect
        const handleConnectionError = (error) => {
            setConnectionError(true);    
        };

        const handleHeroJoined = (data) => {
            console.log("handleHeroJoined", data);
            setHero({
                ...data.public_info,
                cards: data.private_info.cards
            });
        };

        const handleOpponentJoined = (data) => {
            console.log("handleOpponentJoined", data);
            setPlayers(data.filter(player => player.sid !== hero?.sid));
        };

        const socketClient = new SocketIOClient(
            'http://localhost:8765',
            props.userName,
            {
                onHeroJoined: handleHeroJoined,
                onOpponentJoined: handleOpponentJoined,
                onConnectionError: handleConnectionError,
            }
        );

        return () => {
            socketClient.close();
        };
    }, [props.userName]); // Only depends on userName now

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
                    {/* It doesn't work like that, you need to send the list of other players from the server. 
                    Each client is independent */}
                    {/* {players.map(player => (
                            player.id !== hero?.id && (
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
                        Render Hero component for the current player */}
                    {console.log("hero", hero)}
                    {hero && (
                        <Hero
                            name={hero.name}
                            pid={hero.pid}
                            role={hero.role}
                            funds={hero.funds}
                            action={hero.last_action}
                            bet={hero.current_bet}
                            cards={hero.cards}
                            bettingStatus={hero.betting_status}
                        />
                    )}
                </div>
            </div>
        )}
    </>
    )
}

export default Game;