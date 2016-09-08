from collections import Iterable
from django.http import JsonResponse
from .ceasar_encode import caesar


__all__ = [
    'api_encode_handler',
    'api_decode_handler',
    'api_frequency_handler',
    'api_guess_handler',
]


def encode_helper(request):
    text = request.GET.get('text') or ''
    offset = request.GET.get('offset')
    if offset and offset.isdigit():
        offset = int(offset)
    else:
        offset = 0
    return text, offset


def api_encode_handler(request):
    text, offset = encode_helper(request)
    result = caesar(text, offset, encrypt=True)
    return JsonResponse({'success': True, 'result': result, 'offset': offset})


def api_decode_handler(request):
    text, offset = encode_helper(request)
    result = caesar(text, offset, encrypt=False)
    return JsonResponse({'success': True, 'result': result, 'offset': offset})


def api_frequency_handler(request):
    text = request.GET.get('text') or ''
    unique_chars = {char for char in text if char.isalpha()}
    frequency = [{'label': char, 'value': round(text.count(char) / len(text) * 100, 2)} for char in unique_chars]
    return JsonResponse({'success': True, 'frequency': frequency})


def api_guess_handler(request):
    text = request.GET.get('text') or ''
    best_key, guess_rate, guess_text = caesar.guess_encode(text)
    if best_key == 0:
        return JsonResponse({'success': True,
                             'is_encrypted': False})

    return JsonResponse({'success': True,
                         'is_encrypted': True,
                         'best_key': best_key,
                         'guess_rate': round(guess_rate, 2) * 100,
                         'guess_text': guess_text})
