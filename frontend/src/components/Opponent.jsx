import "../styles/Opponent.css";
import "../styles/Player.css";

export default function Opponent(props) {
    return (
        <div className="opponent-container">
            <img src={"/src/assets/user-" + props.id + ".svg"} className="player-image" alt="Player1" />
            <div className="opponent-info">
                <h3 className="player-name">{props.name}</h3>
                <p className="player-funds">$ {props.funds}</p>
                <p className="player-bet">$ {props.bet} <strong>{props.action}</strong></p>
            </div>
        </div>
    )
}

