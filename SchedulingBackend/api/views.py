from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserSerializer
from rest_framework import permissions, status
from .validations import validate_email, validate_password
from django.db import connection
import requests 
from .services import generate_schedule


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
	

class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated, ) #ensures the user is Authenticated
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)


class getTnum(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            user_email = request.user.email
        else:
            user_email = None
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT TNumber, MajorID FROM student WHERE Email = %s", [user_email])
            result = cursor.fetchone()
            if result:
                t_number = result[0]
                major_id = result[1]
            else:
                t_number = None
                major_id = None
            return Response({'t_number': t_number, 'major_id': major_id})
        
class getClassesNeeded(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # Create an instance of getTnum view
        get_tnum_view = getTnum()

        # Call getTnum endpoint to fetch major_id
        tnum_response = get_tnum_view.get(request)
        major_id = tnum_response.data.get('major_id')

        # Retrieve class information based on major_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT courseSubject, courseNum FROM majorclasses WHERE majorID = %s", [major_id])
            result = cursor.fetchall()
            return Response(result)

    

class test(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT cn.CourseSubject, cn.CourseNum, c.CourseName, cn.IsTaken, c.CreditHours FROM classesNeeded cn JOIN courses c ON c.CourseSubject = cn.CourseSubject AND c.CourseNum = cn.CourseNum WHERE cn.Tnumber = 'T0123456';")
            result = cursor.fetchall()
        #return Response(result)
        return Response(generate_schedule(result))



    

