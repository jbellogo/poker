import React, { useState, useEffect, useCallback } from 'react';
import '../styles/Game.css';
import Hero from './Hero';
import Opponent from './Opponent';
import SocketIOClient from '../services/Client';
import ConnectionError from './ConnectionError';


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
            <ConnectionError />
        ) : (
            console.log("MAIN GAME VIEW"),
            // make this into a component for readability.
            <div className="game-container">
                <div className="table-container">
                    {/* It doesn't work like that, you need to send the list of other players from the server. 
                    Each client is independent */}
                    {console.log("players", players)}
                   
                    {players.map(player => (
                            player.sid !== hero?.sid && (
                                <Opponent
                                    name={player.name}
                                    id={player.pid}
                                    funds={player.funds}
                                    bet={player.current_bet}
                                    action={player.last_action}
                                />
                            )
                        ))}
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