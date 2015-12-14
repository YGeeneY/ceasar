from re import search as re_search
from django.db import connection as conn
from .guess import *

az = [chr(x) for x in range(ord('a'), ord('z') + 1)]  # creating alphabet
az_len = len(az)


def encrypt_letter(letter, offset, en):
    """
    :param letter: 1 letter at time that passing through de_encrypt_text function
    :param offset: ROT
    :return: one letter or char at time
    """
    if not letter.isalpha():  # Good to not encrypt something if you dont know how. Just return as it is
        return letter
    if en:
        position = (az.index(letter.lower()) + offset) % az_len  # Using wiki formula encode letter
    elif not en:
        position = (az.index(letter.lower()) - offset + az_len) % az_len
    if letter.isupper():  # and return it in default case
        return az[position].upper()
    elif letter.islower():
        return az[position].lower()


def de_encrypt_text(text, offset, en=True):  # passing each letter through cycle of de/encrypting
    """
    :param text: text to be translated
    :param offset: ROT value
    :param en: if True - encode/ if false - decode
    :return: translated text
    """
    value = ''
    for word in text.split():
        # dictionary_append(word, en)
        # un-comment if you want to grow dictionary in sqlite
        for letter in word:
            value += encrypt_letter(letter, offset, en)
        value += ' '
    return value


def choose(mytext, key=None):
    '''
    :param mytext: text
    :param key: to iterate with guess_translation function statement
    :return: % of luck, guess text that is decoded
    '''
    clean_text = ""
    for word in set(mytext.split()):
        word = re_search('[a-z]*', word.lower()).group()
        if word:
            clean_text += '\'%s\' ,' % word
    cursor = conn.cursor()
    query = 'SELECT COUNT(*) FROM mydictionary WHERE word IN (%s)' % clean_text[:-2]
    cursor.execute(query)
    response = cursor.fetchone()[0]
    return response, mytext, key


def guess_translation(text):
    """
    :param text: text to gues if it is encrypted
    :return: if statement runs choose() function to guess if text is clear. Else iterate with key to get clean text
    """
    total_unique_words = len(set(text.split()))
    answer = choose(text)[0]
    guess = round((float(answer) / total_unique_words) * 100, 1)

    if guess <= 20:  # if text is clear more than :
        possibilities = []

        for i in range(az_len):
            possibilities.append(choose(de_encrypt_text(text, i, False), i))
        answer = (sorted(possibilities, reverse=True)[0])  # get text with best encoding, and encryption key

        percent = round((answer[0] / total_unique_words) * 100, 1)
        decoded_text = answer[1]
        key = answer[2]
        response = "Looks like text is encrypted!\n" \
                   " For %s percent you can decode it with ROT %s.\n Decoded text starts with:\n" \
                   " '%s'..." % (percent, key, decoded_text[:120])
        response = {'guess_text': response}

    else:
        response = ({'guess_text': '%s percents that text doesn\'t encrypted. Choose ROT, and click encode.' % guess})
    return response


