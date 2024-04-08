import copy
from .utils import transform_for_generate_schedule, percentage_done, sort_dict

def generate_schedule(classes_needed):

    semesters = []

    #TAKE IN THESE VARIABLES
    hours_per_semester = 15  # This is where we need to pass how many hours they want
    total_major_hours = 120 # This is where we need to get how many hours they need for their major

    
    transformed_data = transform_for_generate_schedule(classes_needed)
    sorted_data = sort_dict(transformed_data)
    classes_needed_copy = copy.deepcopy(sorted_data)
    temp = 0
   
    percentage = percentage_done(transformed_data)
    
    while total_major_hours > 0:
        
        semester_hours = 0  # Track the total credit hours added to the current semester
        semester_courses = []  # Courses for the current semester
        for course_key, course_info in list(classes_needed_copy.items()):  # Use list() to create a copy for safe iteration
            course = [course_info["CourseSubject"], course_info["CourseNum"]]
            
            if (course_info["CreditHours"] + temp <= hours_per_semester \
                and semester_hours + course_info["CreditHours"] <= hours_per_semester \
                and course_info["isTaken"] == 0) \
                or (course_info["CreditHours"] + temp <= hours_per_semester+1 \
                and semester_hours + course_info["CreditHours"] <= hours_per_semester+1 \
                and course_info["isTaken"] == 0):
                semester_courses.append(course)
                temp += course_info["CreditHours"]
                semester_hours += course_info["CreditHours"]
                del classes_needed_copy[course_key]  # Remove the course from classes_needed after adding to a semester
        
        if semester_courses:
            semesters.append(semester_courses)
            total_major_hours -= temp
            temp = 0
        else:
            break
    return {"semesters":semesters,
            "percentage": percentage}

