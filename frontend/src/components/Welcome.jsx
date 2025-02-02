import '../styles/Welcome.css';
import { useState } from 'react';


function Welcome({ onGameStart }) {
    const [localname, setLocalName] = useState(''); // Initialise state as ''

    return (
        <div className="welcome-container">
            <div className="welcome-content">
                <h1>Online Poker</h1>
                <h3>Welcome!</h3>
                <p> Simple poker game for you and your friends to play online. Blinds are fixed at $50/$100 and you start with $1000. </p>
                <p> Please enter your name to join the game.</p>
                <input type="text" placeholder="Enter your name" value={localname} onChange={(e) => setLocalName(e.target.value)}/>
                <button onClick={() => onGameStart(localname)} disabled={!localname.trim()}>Join Game</button> {/* Disabled if name without whitespaces is empty */}
            </div>
        </div>
    )
}

export default Welcome;