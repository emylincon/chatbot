from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
#from chatbot import get_response
from rihanna import get_response
from rihanna import rihanna_voice
from threading import Thread
import ast
import json


class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        message = self.data
        response = get_response(message)
        # self.sendMessage(response)  f"{text};{result}"

        if response[0] == '{':
            response = ast.literal_eval(response)
            h1 = Thread(target=self.sendMessage, args=(json.dumps(response),))
            h1.start()
        else:
            h1 = Thread(target=self.sendMessage, args=(response,))
            h2 = Thread(target=rihanna_voice, args=(response,))
            h1.start()
            h2.start()

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()

