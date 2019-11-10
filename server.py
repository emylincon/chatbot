from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
#from chatbot import get_response
from rihanna import get_response
from rihanna import rihanna_voice
from threading import Thread


class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        message = self.data
        response = str(get_response(message))
        # self.sendMessage(response)
        h1 = Thread(target=self.sendMessage, args=(response,))
        h2 = Thread(target=rihanna_voice, args=(response,))
        h1.start()
        h2.start()
        '''
        if str(response)[:3] == '- -':
            rihanna_voice(str(response)[3:])
        elif str(response)[0] == '-':
            rihanna_voice(str(response)[1:])
        else:
            rihanna_voice(response)
        '''

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, ChatServer)
server.serveforever()
