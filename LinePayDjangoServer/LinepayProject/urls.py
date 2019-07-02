from django.conf.urls import url
from LinepayAPP.views import *

urlpatterns = [
    url(r'^', callback),
    url(r'^confirm/$', confirm),
]