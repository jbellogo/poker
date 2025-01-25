import React from 'react';
import './Game.css';
import Player from './player';

const Game = () => {
    return (
      <div className="game-container">
        {/* Game content will go here */}
        <div className="table-container">
            <Player name="John Cena" id={1} funds={1000} bet={100} action="CALL" />
            <Player name="Tony Romo" id={2} funds={1000} bet={100} action="CALL" />
            <Player name="Lila" id={3} funds={1000} bet={100} action="FOLD" />
            <Player name="Maria" id={4} funds={1000} bet={100} action="CALL" />
        </div>

      </div>
    );
  };

export default Game;