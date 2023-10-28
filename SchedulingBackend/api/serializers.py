from rest_framework import serializers #serializers allow for database data to be configured to json and consumed by the api
from django.contrib.auth import authenticate, get_user_model
from rest_framework.serializers import ValidationError

class UserRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = '__all__'
	def create(self, clean_data):
		user_obj = get_user_model().objects.create_user(email=clean_data['email'], password=clean_data['password'])
		user_obj.username = clean_data['username']
		user_obj.save()
		return user_obj

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user