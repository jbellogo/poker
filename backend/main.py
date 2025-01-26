from server import WebsocketServer
from models import Game



if __name__ == "__main__":
    
    server = WebsocketServer()
    server.start()
    game = Game()
    game.start()
