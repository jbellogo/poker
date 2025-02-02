## EXCHANGE \#1: Player joins game 

**Occurs onConnect, after initial handshake**

1. S: Server is running (server.py)
2. C: Client attempts to connect to the server (Client.js)

3. C: On successful connect, client sends join request to server:
{type:‘player_join_request’,  name:”John Cena”}

4. S: Server views and handles request:

    4.1. If there are enough player slots available, server ‘approves’ request:
    
        4.1.1 Server creates hero object locally using only the client’s name
        4.1.2 Server sends back Hero state looking like this: 

```json
{
    type: ‘hero_join_success’,
    data: {
        sid1: {
            "public_info": {
                "pid": int,
                "funds": int,
                "role": PlayerRole,
                "betting_status": PlayerStatus,
            },
            "private_info": {
                "hand": [],
            }
        }
    }
}
```

        4.1.3 Server sends TO ALL ACTIVE CLIENTS, an updated player list: 

```json
{
    "type": "new_player_join",
    "players": [{
            name: 'josh',
            pid: 2,
            sid: 'cP5aAdo94BRik5xeAAAG',
            funds: 5000,
            role: 'other',
        },
        {
            name: 'yo',
            pid: 2,
            sid: 'KHeJDO0QmodaFy4cAAAJ',
            funds: 5000,
            role: 'other',
        }
    ]
}
```

    4.2  If there are not enough player slots, the server disconnects the client. 

6. C: Client takes the hero_join_success message and updates it’s own players list and thisPLayer object… sounds like a side effect.
7. C: Client takes the new_player_join message and updates it’s own players list to render the new player.






