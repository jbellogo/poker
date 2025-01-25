
function Player(props) {
    return (
        <div className="player-container">
            <img src={"/src/assets/user-" + props.id + ".svg"} className="player-image" alt="Player1" />
            <div className="player-info">
                <h3 className="player-name">{props.name}</h3>
                <p className="player-funds">$ {props.funds}</p>
                <p className="player-bet">$ {props.bet} <strong>{props.action}</strong></p>

            </div>

        </div>
    )
}

export default Player;