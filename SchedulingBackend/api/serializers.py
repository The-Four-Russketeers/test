from rest_framework import serializers #serializers allow for database data to be configured to json and consumed by the api
from django.contrib.auth import authenticate
from rest_framework.serializers import ValidationError


class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user