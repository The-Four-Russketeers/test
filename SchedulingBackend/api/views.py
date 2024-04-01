from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserLoginSerializer, UserSerializer, ClassInfoSerializer
from rest_framework import permissions, status
from .validations import validate_email, validate_password
from django.db import connection
from rest_framework.exceptions import NotAuthenticated
import requests 
from .calculations import preCheck, checkIfTaken


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
        

    
from rest_framework.exceptions import NotAuthenticated

class getClassesNeeded(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        get_tnum_view = getTnum()

        try:
            tnum_response = get_tnum_view.get(request)
            TNumber = tnum_response.data.get("t_number")

            if TNumber is None:
                return Response({'error': 'TNumber not found'}, status=status.HTTP_400_BAD_REQUEST)

            with connection.cursor() as cursor:
                cursor.execute("SELECT CourseSubject, CourseNum, isTaken FROM classesNeeded WHERE Tnumber = %s", [TNumber])
                result = cursor.fetchall()
                classes_info = [{'CourseSubject': row[0], 'CourseNum': row[1], 'isTaken': row[2]} for row in result]

                prerequisites_info = []
                for course in classes_info:
                    course_subject = course['CourseSubject']
                    course_num = course['CourseNum']

                    cursor.execute("SELECT PreReqCourseSub, PreReqCourseNum FROM prerequisites WHERE CourseSubject = %s AND CourseNum = %s", (course_subject, course_num))
                    prerequisites_result = cursor.fetchall()

                    prerequisites_info.extend([{'CourseSubject': course_subject,
                                                'CourseNum': course_num,
                                                'preReqCourseSub': row[0],
                                                'preReqCourseNum': row[1]} for row in prerequisites_result])

                sortedClassesNeeded = preCheck(classes_info, prerequisites_info) 
                sortedClassesNeeded = checkIfTaken(sortedClassesNeeded)
                return Response(sortedClassesNeeded)

        except NotAuthenticated:
            print("Authentication required")  
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    

class test(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM courses")
            result = cursor.fetchall()
        return Response(result)



    

