// import "../styles/Player.css";
import "../styles/Hero.css";
/* 
Hero is the primary Player. 
You are the primary player. 
Only you have visibility of your cards and are able to act on your behalf.
*/

export default function Hero(props) {
    return (
        <div className="hero-container"> 
            <div className="hero-col">
                <img src={"/src/assets/user-" + props.id + ".svg"} className="player-image" alt="Player1" />
                <h3 className="player-name">{props.name}</h3>
                <h3 className="player-funds">${props.funds}</h3>
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


