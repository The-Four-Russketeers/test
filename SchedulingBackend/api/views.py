from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer
from rest_framework import permissions, status
from .validations import validate_email, validate_password


class UserLogin(APIView):
	permission_classes = (permissions.AllowAny,) # anyone can access this view
	authentication_classes = (SessionAuthentication,) # specifies we want to use sessionAuthentication
	##
	def post(self, request): # posts handle http post requests from the frontend
		data = request.data #retrieves data sent from the post
		assert validate_email(data) 
		assert validate_password(data)
		serializer = UserLoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True): # checks if the data is valid based on the serializers logic
			user = serializer.check_user(data)
			login(request, user)
			return Response(serializer.data, status=status.HTTP_200_OK)
		


class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)