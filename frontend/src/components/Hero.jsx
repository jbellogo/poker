// import "../styles/Player.css";
import "../styles/Hero.css";
import { useEffect } from 'react';
/* 
Hero is the primary Player. 
You are the primary player. 
Only you have visibility of your cards and are able to act on your behalf.
*/

const Hero = (props) => {
    useEffect(() => {
        console.log("props", props);
        console.log(`my address is /src/assets/user-${props.pid}.svg`);
    }, [props.pid]);

    return (
        <div className="hero-container"> 
            {console.log("props", props)}
            <div className="hero-col">
                <img src={`/src/assets/user-${props.pid}.svg`} className="player-image" alt="Player1" />
                <h3 className="player-name">{props.name}</h3>
                <h3 className="player-funds">${props.funds}</h3>
                <h3 className="player-bet">${props.bet} {props.action}</h3>
            </div>
            <div className="hero-col">
                <div className="hero-cards-container">
                    <img src={"/src/assets/cards/2_of_hearts.png"} className="hero-card" alt="Player1" />
                    <img src={"/src/assets/cards/ace_of_diamonds.png"} className="hero-card" alt="Player1" />
                </div>

                <div className="hero-actions-container">
                    <button className="hero-action-button">fold</button>
                    <button className="hero-action-button">call</button>
                    <button className="hero-action-button">raise</button>
                    <button className="hero-action-button">check</button>
                </div>

            </div>
        </div>
        )
    }

export default Hero;