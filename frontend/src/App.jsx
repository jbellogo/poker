import './App.css'
import Game from './components/Game'
import { useState } from 'react';
import Welcome from './components/Welcome';


function App() {
    const [showGame, setShowGame] = useState(false);
    const [playerName, setPlayerName] = useState('');

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
          <Game userName={playerName}/>
        </div>
      )}
    </>
  );
}

export default App
