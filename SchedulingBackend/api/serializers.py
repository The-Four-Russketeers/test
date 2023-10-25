from rest_framework import serializers #serializers allow for database data to be configured to json and consumed by the api
from .models import UserInfo

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password')
        