from PyDictionary import PyDictionary
import config

dictionary=PyDictionary()


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
    response = dictionary.synonym(query)

    return response


def find_antonym(query):
    response = dictionary.antonym(query)

    return response


def translate_(query, lang):
    response = dictionary.translate(query,config.trans_code[lang.capitalize()])

    return response


#print(translate_('hello', 'igbo'))
