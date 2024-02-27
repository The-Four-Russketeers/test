from django.db import connection

class CourseDataFetcher:

    def getCourses(tnumber):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT courseSubject, courseNum
            FROM courses
            WHERE Tnumber = %s """, [tnumber])
            results = cursor.fetchall()
            
            courses_dict = {}
            
            for row in results:
                course_subject = row[0]
                course_num = row[1]
                courses_dict[course_subject] = course_num
            
            return courses_dict