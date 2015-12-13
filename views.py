from django.shortcuts import render
from django.http import JsonResponse

from .ceasar_encode import *
from .guess import *


def OnlyOne(request):
    if request.is_ajax():  # handling ajax
        text = request.GET.get('text')
        offset = int(request.GET.get('offset'))
        encode = (request.GET.get('encode'))
        frequency = count_frequency(text)
        # defining the values
        if encode == 'encode':
            encode = 1
        elif encode == 'decode':
            encode = 0
        elif encode == 'just_frequency':
            guess = guess_translation(text)
            return JsonResponse({"success": True,
                                 "frequency": frequency,
                                 "guess": guess['guess_text']})

        decoded = de_encrypt_text(text, offset, encode)
        return JsonResponse({"success": True, "text": decoded, "frequency": frequency})
    else:  # if ajax fail same form is rendering
        return render(request, 'ceasar/content.html')