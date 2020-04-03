from spellchecker import SpellChecker

spell = SpellChecker()
spell.word_frequency.load_words(['microsoft', 'apple', 'google', 'tfl', 'copd',
                                 'rihanna', 'chatbot', 'skype', 'facebook', 'amazon', 'nhs'])


def auto_correct(sentence):
    words = sentence.split()
    # find those words that may be misspelled
    misspelled = spell.unknown(words)

    if misspelled:
        for word in misspelled:
            # Get the one `most likely` answer
            correct = spell.correction(word)
            sentence = sentence.replace(word, correct)

    return sentence

#print(auto_correct("sned email"))
#print(auto_correct("lol"))