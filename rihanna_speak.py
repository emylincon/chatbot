import speech_recognition as sr


def speech_recog():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('speak now...')
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            #print("{}".format(text))
            return text
        except:
            #print('sorry could not recognize your voice')
            return 'sorry could not recognize your voice'


#https://www.youtube.com/watch?v=x8U71SarzKE
#https://github.com/soumilshah1995/Html-Css-javascript-with-Python-using-Eel-eel-tutorials
#print(speech_recog())