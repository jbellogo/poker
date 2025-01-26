import React from 'react';
import './Game.css';
import { ActivePlayer, RegularPlayer } from './player';

const Game = () => {
    return (
    <div>
        <h1 className='title'>Online Poker</h1>
        <div className="game-container">
            <div className="table-container">
                <ActivePlayer name="Me" id={1} funds={1000} bet={100} action="CALL" />
                <RegularPlayer name="John Cena" id={2} funds={1000} bet={100} action="CALL" />
                <RegularPlayer name="Tony Romo" id={3} funds={1000} bet={100} action="CALL" />
                <RegularPlayer name="Lila" id={4} funds={1000} bet={100} action="FOLD" />
                <RegularPlayer name="Maria" id={5} funds={1000} bet={100} action="CALL" />
            </div>
        </div>
      </div>
    );
  };

export default Game;