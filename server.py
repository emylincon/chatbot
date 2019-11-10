from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
#from chatbot import get_response
from rihanna import get_response
from rihanna import rihanna_voice


class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        message = self.data
        response = get_response(message)
        self.sendMessage(response)
        if str(response)[:3] == '- -':
            rihanna_voice(str(response)[3:])
        elif str(response)[0] == '-':
            rihanna_voice(str(response)[1:])
        else:
            rihanna_voice(response)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()
