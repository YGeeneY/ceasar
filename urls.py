from django.conf.urls import url
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    url(r'^api/encode$', api_encode_handler),
    url(r'^api/decode$', api_decode_handler),
    url(r'^api/frequency$', api_frequency_handler),
    url(r'^api/guess$', api_guess_handler),
    url(r'^$', TemplateView.as_view(template_name='ceasar/content.html')),
]
