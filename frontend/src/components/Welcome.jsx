


function Welcome() {
    return (
        <div className="welcome-container">
            <h1>Online Poker</h1>
            <h3>Welcome!</h3>
            <p> Simple poker game for you and your friends to play online. Blinds are fixed at $50/$100 and you start with $1000. </p>
            <p> Please enter your name to join the game.</p>
            <input type="text" placeholder="Enter your name" />
            <button onClick={joinGame}>Join Game</button>
        </div>
    )
}

export default Welcome;