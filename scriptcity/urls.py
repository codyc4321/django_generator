from django.conf.urls import include, url

urlpatterns = [
    url(r'^',    include('main.urls', namespace='main')),
]
