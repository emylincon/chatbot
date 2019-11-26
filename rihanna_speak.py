import speech_recognition as sr
import pyttsx3


def rihanna_voice(word_speech):
    engine = pyttsx3.init()
    engine.say(word_speech)
    engine.runAndWait()


def speech_recog():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print('speak')
        rihanna_voice("listening")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            #print("{}".format(text))
            return text
        except:
            #print('sorry could not recognize your voice')
            return 'sorry could not recognize your voice'


"""
for this module to work you need speechreognition and pyaudio
install speechreognition directly from pip
for pyaudio first pip install pipwin
then pipwin install pyaudio
"""
#print(speech_recog())
