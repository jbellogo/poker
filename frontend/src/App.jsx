import './App.css'
import Game from './components/Game'
import { useState } from 'react';
import Welcome from './components/Welcome';


function App() {
    const [showGame, setShowGame] = useState(false);  // Add this state
    const [playerName, setPlayerName] = useState('');  // Add state for player name

    // Add this handler function
    const handleGameStart = (name) => {
        setPlayerName(name);
        setShowGame(true);
    };
  

  return (
    <>
      {!showGame ? (
        <Welcome onGameStart={handleGameStart} />
      ) : (
        <div>
          <Game playerName={playerName}/>
        </div>
      )}
    </>
  );
}

export default App
