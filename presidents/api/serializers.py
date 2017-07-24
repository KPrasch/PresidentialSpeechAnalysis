from rest_framework import serializers
from profiles.models import President, Speech



class SpeechSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Speech
        fields = ('title', 'speaker', 'date', 'body', 'ARI_score', 'ARI_display')


class PresidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = President
        fields = ('presidency_number', 'common_name', 'first_name', 'last_name',
                  'party', 'start_year', 'end_year')