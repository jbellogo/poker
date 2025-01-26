

function ActivePlayer(props) {
    return (
        <div className="active-player-container">
            <div className="active-player-info-container">
                <img src={"/src/assets/user-" + props.id + ".svg"} className="player-image" alt="Player1" />
                <div className="player-info">
                    <h3 className="player-name">{props.name}</h3>
                    <p className="player-funds">$ {props.funds}</p>
                </div>
                <div className="player-cards">
                    <img src={"/src/assets/cards/2_of_hearts.png"} className="player-card" alt="Player1" />
                    <img src={"/src/assets/cards/ace_of_diamonds.png"} className="player-card" alt="Player1" />
                </div>
            </div>
            <div className="active-player-action-container">
                <button className="player-action-button">Fold</button>
                <button className="player-action-button">Call</button>
                <button className="player-action-button">Raise</button>
                <button className="player-action-button">Check</button>
            </div>
        </div>
        )
    }

function RegularPlayer(props) {
    return (
        <div className="regular-player-container">
            <img src={"/src/assets/user-" + props.id + ".svg"} className="player-image" alt="Player1" />
            <div className="player-info">
                <h3 className="player-name">{props.name}</h3>
                <p className="player-funds">$ {props.funds}</p>
                <p className="player-bet">$ {props.bet} <strong>{props.action}</strong></p>
            </div>
        </div>
    )
}


// function Player(props) {
//     if (props.id === 1) {
//         return (<ActivePlayer name={props.name} id={props.id} funds={props.funds} bet={props.bet} action={props.action} />)
//     }
//     else {
//         return (<RegularPlayer name={props.name} id={props.id} funds={props.funds} bet={props.bet} action={props.action} />)
//     }
// }
export { ActivePlayer, RegularPlayer };