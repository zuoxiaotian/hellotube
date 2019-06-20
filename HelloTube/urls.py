from django.conf.urls import url

from HelloTube import settings
from . import view
 
urlpatterns = [
    url(r'^$', view.index),
    url(r'^extract', view.extract),
    url(r'^send', view.send),
    url(r'^create', view.create),
    url(r'^download/(?P<name>.+)/',view.download),
]