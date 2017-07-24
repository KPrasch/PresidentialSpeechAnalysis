"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api import views as apiviews
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'presidents', apiviews.PresidentViewSet)
router.register(r'speeches', apiviews.SpeechViewSet)


urlpatterns = [

    # Django Admin
    url(r'^admin/', admin.site.urls),

    # Public Front End PAges
    url(r'', include('pages.urls', namespace='pages')),

    # REST API
    url(r'^api/v1/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

