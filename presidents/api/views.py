from rest_framework import viewsets
from profiles.models import President, Speech
from .serializers import SpeechSerializer, PresidentSerializer


class PresidentViewSet(viewsets.ModelViewSet):
    queryset = President.objects.order_by('-presidency_number')
    serializer_class = PresidentSerializer


class SpeechViewSet(viewsets.ModelViewSet):
    queryset = Speech.objects.all()
    serializer_class = SpeechSerializer