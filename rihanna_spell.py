from spellchecker import SpellChecker

spell = SpellChecker()


def auto_correct(sentence):
    words = sentence.split()
    # find those words that may be misspelled
    misspelled = spell.unknown(words)
    print(misspelled)
    if misspelled:
        for word in misspelled:
            # Get the one `most likely` answer
            correct = spell.correction(word)
            sentence = sentence.replace(word, correct)

    return sentence

#print(auto_correct("we are drawng stright lines"))