from PyDictionary import PyDictionary
from googletrans import Translator
import config

dictionary=PyDictionary()


def selector(msg):
    if msg[:len("dictionary meaning for")] == "dictionary meaning for":
        msg = msg[len("dictionary meaning for") + 1:].strip()
        return find_meaning(msg)
    elif msg[:len("dictionary synonym for")] == "dictionary synonym for":
        msg = msg[len("dictionary synonym for") + 1:].strip()
        return find_synonym(msg)
    elif msg[:len("dictionary antonym for")] == "dictionary antonym for":
        msg = msg[len("dictionary antonym for") + 1:].strip()
        return find_antonym(msg)
    elif msg[:len("dictionary translate")] == "dictionary translate":
        msg = msg[len("dictionary translate") + 1:].strip().split(' to ')
        return translate_sentence(msg[0], msg[1])


def find_meaning(query):
    response = dictionary.meaning(query)
    reply = "<table id='t01'>\
                  <tr>\
                    <th>Word Type</th>\
                    <th>Meaning</th>\
                  </tr>\
                "
    for i in response:
        meaning = ''
        if len(response[i]) > 1:
            for j in response[i]:
                meaning += f"<p>{j.replace(';', ',')}."
        else:
            meaning = response[i][0]
        reply += f"<tr>\
                            <td>{i}</td>\
                            <td>{meaning}</td>\
                          </tr>"
    return reply


def find_synonym(query):
    try:
        response = dictionary.synonym(query)

    except Exception as e:
        return f"Error in find_synonym: {e}"

    return response


def find_antonym(query):
    try:
        response = dictionary.antonym(query)
    except Exception as e:
        return f"Error in find_antonym: {e}"

    return response


def translate_(query, lang):
    try:
        response = dictionary.translate(query,config.trans_code[lang.capitalize()])
    except Exception as e:
        return f"Error in find_translate_: {e}"
    return response


def translate_sentence(query, lang):
    try:
        translator = Translator()
        dest = config.trans_code[lang.capitalize()]
        obj = translator.translate(query, dest=dest)
        response = obj.text
        if is_alpha(obj.text):
            pronunciation = obj.text
        else:
            pronunciation = obj.extra_data['translation'][1][-1]
        #pronunciation = obj.pronunciation
        reply = {'display': response, 'say': pronunciation}
    except Exception as e:
        return f"Error in translate_sentence: {e} \n request: {query} \n l: {lang}"
    return reply

def aball(query,lang):
    translator = Translator()
    dest = config.trans_code[lang.capitalize()]
    obj = translator.translate(query, dest=dest)
    response = obj.text
    if is_alpha(obj.text):
        pronunciation = obj.text
    else:
        pronunciation = obj.extra_data['translation'][1][-1]
    # pronunciation = obj.pronunciation
    reply = {'display': response, 'say': pronunciation}
    return reply


def translate_sentence_code(query, lang):
    try:
        translator = Translator()
        obj = translator.translate(str(query), dest=lang)
        response = obj.text
        if is_alpha(obj.text):
            pronunciation = obj.text
        else:
            pronunciation = obj.extra_data['translation'][1][-1]
        #pronunciation = obj.pronunciation
        reply = {'display': response, 'say': pronunciation}

    except Exception as e:
        return f"Error in translate_sentence_code: {e} \n request: {query} \n l: {lang}"
    return reply


def is_alpha(word):
    try:
        return word.encode('ascii').isalpha()
    except:
        return False


def detect_lang(query):
    try:
        translator = Translator()
        return translator.detect(query).lang

    except Exception as e:
        return f"detect_lang error: {e}"

#print(translate_('hello', 'igbo'))
#print(selector("dictionary translate smart cities to japanese"))

#a = translate_sentence_code(query='hello', lang='ja')
#print(aball(query='hello', lang='japanese'))