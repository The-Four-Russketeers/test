from rest_framework import serializers #serializers allow for database data to be configured to json and consumed by the api
from django.contrib.auth import get_user_model, authenticate
from rest_framework.serializers import ValidationError

userModel = get_user_model()

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password']) #Changed username to email
		if not user:
			raise ValidationError('user not found')
		return user
	
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = userModel
		fields = ('email', 'username')


class ClassInfoSerializer(serializers.Serializer):
	courseSubject = serializers.CharField()
	courseNum = serializers.CharField() 
	preReqCourseSub = serializers.CharField() 
	preReqCourseNum = serializers.CharField() 