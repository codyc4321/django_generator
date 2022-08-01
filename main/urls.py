from django.conf.urls import include, url
from main.scripts import views

urlpatterns = [
    url(r'^scripts/',  include('main.scripts.urls',  namespace='scripts')),
    url(r'^$',  views.index,     name='index'),
]