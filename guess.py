from re import search
from django.db import connection

guess_rate = 20


def dictionary_append(word, en):
    if en:
        match = search('\w+', word.lower()).group()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO mydictionary(word) VALUES("%s")' % match)


def count_frequency(text):
    text = text.upper()
    frequency = []
    unique = set(text)
    for char in unique:
        if char.isalpha():
            frequency.append(dict(label=char,
                                  value=round(float(text.count(char))/float(len(text))* 100, 1)))
    chart_response = {"chart": {"caption": "Light It Ceasar decode",
                                "xAxisName": "Letter",
                                "yAxisName": "percentage",
                                "numberPrefix": "%",
                                "theme": "fint"}, "data": frequency}
    return chart_response
