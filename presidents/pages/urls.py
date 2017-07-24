from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^president/(?P<slug>[A-Za-z\s\-_]+)/$', views.president_profile, name='pres_profile'),

]