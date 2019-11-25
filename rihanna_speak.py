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


"""
for this module to work you need speechreognition and pyaudio
install speechreognition directly from pip
for pyaudio first pip install pipwin
then pipwin install pyaudio
"""
#print(speech_recog())
