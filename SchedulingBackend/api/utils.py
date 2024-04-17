from django.db import connection

# Create classesNeeded dictionary with numbered keys and isTaken flag
# def transform_for_generate_schedule(data):
#     classesNeeded = {}
#     for index, course in enumerate(data, 1):
#         classesNeeded[index] = {
#             "CourseSubject": course[0],
#             "CourseNum": course[1],
#             "isTaken": course[3],  # Assuming isTaken is initially set to 0 for all courses
#             "CreditHours" : course[4]
#         }
#     return(classesNeeded)
def transform_for_generate_schedule(data):
    classesNeeded = {}
    if isinstance(data, list):
        for index, course in enumerate(data, 1):
            classesNeeded[index] = {
                "CourseSubject": course[0],
                "CourseNum": course[1],
                "isTaken": course[3],  # Assuming isTaken is initially set to 0 for all courses
                "CreditHours": course[4]
            }
    elif isinstance(data, dict):
        classesNeeded = data
    else:
        raise ValueError("Invalid data format. Must be a list or a dictionary.")
    
    return classesNeeded

# Get a percentage on how far the student is in their major
import math

def percentage_done(data):
    taken = 0 
    for i in data:
        if data[i]["isTaken"] == 1:
            taken+=1 # Number of classes they have taken
    percentage = math.ceil(taken/len(data) * 100) # Divide the number of classes taken by how many they need (rounded up)
    return(percentage)

def sort_dict(input_dict):
    # Sort the dictionary items based on the CourseNum key
    sorted_items = sorted(input_dict.items(), key=lambda x: x[1]["CourseNum"])

    sorted_dict = {key: value for key, value in sorted_items}

    return sorted_dict 


def getTNumber(request):
    if request.user.is_authenticated:
        user_email = request.user.email
    else:
        user_email = None
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT TNumber FROM student WHERE Email = %s", [user_email])
        result = cursor.fetchone()
        if result:
            t_number = result[0]
        else:
            t_number = None
        return t_number
    
def get_classes_info(TNumber):
    classes_info = {}

    with connection.cursor() as cursor:
        cursor.execute("SELECT CourseSubject, CourseNum, isTaken FROM classesNeeded WHERE Tnumber = %s", [TNumber])
        result = cursor.fetchall()
        for row in result:
            course_id = f"{row[0]}-{row[1]}"
            classes_info[course_id] = {
                'CourseSubject': row[0],
                'CourseNum': row[1],
                'isTaken': row[2]
            }

        for course_id, course_info in classes_info.items():
            course_subject = course_info['CourseSubject']
            course_num = course_info['CourseNum']
            cursor.execute("SELECT CreditHours FROM courses WHERE CourseSubject = %s AND CourseNum = %s", (course_subject, course_num))
            credit_hours_result = cursor.fetchone()
            if credit_hours_result:
                credit_hours = credit_hours_result[0]
                course_info['CreditHours'] = credit_hours
            else:
                course_info['CreditHours'] = None

    return classes_info

def get_prerequisites_info(classes_info):
    prerequisites_info = []

    with connection.cursor() as cursor:
        for course_id, course_info in classes_info.items():
            course_subject = course_info['CourseSubject']
            course_num = course_info['CourseNum']
            cursor.execute("SELECT PreReqCourseSub, PreReqCourseNum FROM prerequisites WHERE CourseSubject = %s AND CourseNum = %s", (course_subject, course_num))
            prerequisites_result = cursor.fetchall()

            prerequisites_info.extend([{
                'CourseSubject': course_subject,
                'CourseNum': course_num,
                'preReqCourseSub': row[0],
                'preReqCourseNum': row[1]
            } for row in prerequisites_result])

    return prerequisites_info

def prereqs_in_order(prereq_map):
        
        duplicate_classes = []
        
        # Sort the prereqMap dictionary into an array
        for key, value in prereq_map.items():
            index_parts = key.split('-')  # Split the index string by '-'
            course_subject = index_parts[0]  # Extract Course subject
            course_number = int(index_parts[1])  # Extract Course number (converted to int)
            prerequisites = [[course[0], course[1], course_subject, course_number] for course in value]  # Course subject, number, and index parts
            duplicate_classes.append(prerequisites)
            
        split_duplicate_classes = []
        # Split the array
        
        for class_set in duplicate_classes:
            split_class_set = [[class_data[i], class_data[i + 1]] for class_data in class_set for i in range(0, len(class_data), 2)]
            split_duplicate_classes.append(split_class_set)
        
        return split_duplicate_classes

def remove_duplicate_classes(classes_needed_copy):
    prereq_map = prereqs_in_order(prereqMap)  # Assuming prereqs_in_order returns the prereqMap split up
    courses_to_remove = []  # List to store courses to remove from classes_needed_copy
    
    for course_key, course in classes_needed_copy.items():  # Iterate over key-value pairs in classes_needed_copy
        course_info = [course['CourseSubject'], course['CourseNum']]
        for prereqs in prereq_map:
            for prereq in prereqs:
                if course_info == prereq:
                    courses_to_remove.append(course_key)  # Add course_key to courses_to_remove list
    
    # Remove courses outside the loop to avoid changing dictionary size during iteration
    for course_key in courses_to_remove:
        del classes_needed_copy[course_key]
        
    return(classes_needed_copy)  

# Formats the data from the test2 API into a dictionary for our code to work
def format_majorclasses(data):
    majorclasses = {}
    for item in data:
        majorclass_id = item[0]
        majorclasses[majorclass_id] = {
            "MajorID": item[1],
            "CourseSubject": item[2],
            "CourseNum": item[3],
            "CreditHours": item[4] if item[4] is not None else '',
            "CourseType": item[5] if item[5] is not None else ''
        }
    return majorclasses

# Finds all blank elective classes for their major they need to take and returns an array
def required_electives(major_classes):
    electives = []
    for course in major_classes.values():
        if course['CourseSubject'] == "None":
            course_num = str(course['CourseNum'])[0] + "XX" +str(course['CreditHours'])
            course_info = [(course['CourseType']).upper(),course_num]
            electives.append(course_info)
    return electives
    
# Returns how many total hours are in a given semester
def hours_in_current_sem(semester):
        sem_hours = sum(int(str(course[1])[-1]) for course in semester)
        return sem_hours
