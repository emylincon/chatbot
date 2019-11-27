from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
#from chatbot import get_response
from rihanna1 import get_response
from rihanna import rihanna_voice
from threading import Thread


class ChatServer(WebSocket):

    def handleMessage(self):
        # echo message back to client
        message = self.data
        response = str(get_response(message))
        # self.sendMessage(response)  f"{text};{result}"
        if ";" in response:                               # handling speak button clicked and the response
            result = response.split(';')
            response = result[1]
            reply = result[0] + ';'
            '''
            h1 = Thread(target=self.sendMessage, args=(reply,))
            h2 = Thread(target=rihanna_voice, args=(say,))
            h1.start()
            h2.start()
            '''
            if ("\n" and "|") in response:                        # handling both newline and link provided
                say = ""
                for i in response.split('\n'):
                    if '|' in i:
                        say += "\n" + i.split('|')[0]
                    else:
                        say += i
                display_response = response.replace("\n", "<br>").replace("|", "")
                answer = reply + display_response
                h1 = Thread(target=self.sendMessage, args=(answer,))
                h2 = Thread(target=rihanna_voice, args=(say,))
                h1.start()
                h2.start()
            elif "\n" in response:
                display_response = response.replace("\n", "<br>")      # handling new line
                answer = reply + display_response
                h1 = Thread(target=self.sendMessage, args=(answer,))
                h2 = Thread(target=rihanna_voice, args=(response,))
                h1.start()
                h2.start()
            elif "|" in response:                                 # handling links provided in reply
                say = response.split('|')[0] + "\n Link provided"
                _reply_ = response.replace("|", "")
                answer = reply + _reply_
                h1 = Thread(target=self.sendMessage, args=(answer,))
                h2 = Thread(target=rihanna_voice, args=(say,))
                h1.start()
                h2.start()

            else:
                answer = reply + response
                h1 = Thread(target=self.sendMessage, args=(answer,))
                h2 = Thread(target=rihanna_voice, args=(response,))
                h1.start()
                h2.start()
        elif ("\n" and "|") in response:  # handling both newline and link provided
            say = ""
            for i in response.split('\n'):
                if '|' in i:
                    say += "\n" + i.split('|')[0]
                else:
                    say += i
            display_response = response.replace("\n", "<br>").replace("|", "")

            h1 = Thread(target=self.sendMessage, args=(display_response,))
            h2 = Thread(target=rihanna_voice, args=(say,))
            h1.start()
            h2.start()
        elif "\n" in response:
            display_response = response.replace("\n", "<br>")  # handling new line

            h1 = Thread(target=self.sendMessage, args=(display_response,))
            h2 = Thread(target=rihanna_voice, args=(response,))
            h1.start()
            h2.start()
        elif "|" in response:  # handling links provided in reply
            say = response.split('|')[0] + "\n Link provided"
            reply = response.replace("|", "")
            h1 = Thread(target=self.sendMessage, args=(reply,))
            h2 = Thread(target=rihanna_voice, args=(say,))
            h1.start()
            h2.start()

        else:
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
