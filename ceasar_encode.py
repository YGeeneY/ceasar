from string import ascii_lowercase as alphabet
from django.db import connection as conn
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'ceasar3.settings'


class CaesarCypher:
    alpha_len = len(alphabet)
    min_guess_rate = 0.2

    def __call__(self, text, offset, encrypt=True):
        if not encrypt:
            offset = self.alpha_len - offset
        result = []
        for letter in text:
            if not letter.isalpha():
                result.append(letter)
                continue
            letter_to_process = letter.lower()
            processed_letter = self._encrypt_letter(letter_to_process, offset)
            if letter.isupper():
                processed_letter = processed_letter.upper()
            result.append(processed_letter)
        return ''.join(result)

    def _encrypt_letter(self, letter, offset=0):
        position = (alphabet.find(letter) + offset) % self.alpha_len
        return alphabet[position]

    @staticmethod
    def __how_many_do_i_know(text):
        clean_words = filter(lambda x: x.isalpha(), text.split())
        clean_words = ['\'{}\''.format(x) for x in clean_words]
        cursor = conn.cursor()
        query = 'SELECT COUNT(*) FROM mydictionary WHERE word IN ({})'.format(",".join(clean_words))
        cursor.execute(query)
        response = cursor.fetchone()[0]
        return response / len(clean_words)

    def guess_encode(self, text):
        options = [self(text, offset, encrypt=False) for offset in range(self.alpha_len)]
        best_option = [self.__how_many_do_i_know(option) for option in options]
        best_key, guess_rate = max(enumerate(best_option), key=lambda x: x[-1])
        guess_text = options[best_key]
        return best_key, guess_rate, guess_text

caesar = CaesarCypher()
