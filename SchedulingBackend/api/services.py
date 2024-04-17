import copy
import math
from .utils import transform_for_generate_schedule, percentage_done, sort_dict, remove_duplicate_classes,prereqs_in_order,hours_in_current_sem,format_majorclasses,required_electives

def generate_schedule(classes_needed, hours_per_semester, total_major_hours,prereqMap,majorClasses):

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
    
    semesters = [] # All semesters and classes will be stored in this array

    transformed_data = transform_for_generate_schedule(classes_needed) # Transform the data from the API to a dictionary
    sorted_data = sort_dict(transformed_data) # Sort the dictionary by course number
    classes_needed_copy = copy.deepcopy(sorted_data) # Create a copy of the dictionary for editing purposes
    temp = 0
    
    percentage = percentage_done(transformed_data) # Get a percentage on how far along the student is in their major

    #1). Remove duplicate classes from classes_needed_copy dictionary that appear in the prereqs array
    
    modified_dict = remove_duplicate_classes(classes_needed_copy) # modified_dict has all prerequisite classes in prereqMap(Wilson's code) removed from classes_needed_copy
    
    #2). Run the program with classes_needed_copy array (with no duplicate classes) with hours_per_semester set to -= 7
    
    hours_per_semester_temp = hours_per_semester 
    #hours_per_semester_temp-=6
 
    classes_per_semester = hours_per_semester_temp/3 # Number of projected classes to be taken each semester 5
    classes_per_semester-=2 # Temporarily remove at least 2 classes for each semester 3
    hours_per_semester_temp = classes_per_semester*3
    math.ceil(hours_per_semester_temp)
    
    while total_major_hours > 0:
        semester_hours = 0  # Track the total credit hours added to the current semester
        semester_courses = []  # Courses for the current semester
        for course_key, course_info in list(modified_dict.items()):  # Use list() to create a copy for safe iteration
            course = [course_info["CourseSubject"], course_info["CourseNum"]]
            if (course_info["CreditHours"] + temp <= hours_per_semester_temp \
                and semester_hours + course_info["CreditHours"] <= hours_per_semester_temp \
                and course_info["isTaken"] == 0) \
                or (course_info["CreditHours"] + temp <= hours_per_semester_temp+1 \
                and semester_hours + course_info["CreditHours"] <= hours_per_semester_temp+1 \
                and course_info["isTaken"] == 0) \
                or (course_info["CreditHours"] + temp <= hours_per_semester_temp+2 \
                and semester_hours + course_info["CreditHours"] <= hours_per_semester_temp+2 \
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
    semesters.append([])# Manually add another semester for appending later
    
    #3). Add the prereqs array classes semester by semester (make sure do not go over hour per semester limit)
    prereq_courses = prereqs_in_order(prereqMap)
    
  
    for semester_index in range(len(semesters)): # For every semester_index in the semester array
        sem_hours = hours_in_current_sem(semesters[semester_index]) # Find how many hours are in the current semester
        for sets in range(len(prereq_courses)): # Traverse through each set in prereq_courses array
            for prereq in prereq_courses[sets]: # For an individual prerequisite class in the set
                prereq_hours = int(str(prereq[1])[-1]) # Find how many hours the individual prereq class has
                if not prereq_hours + sem_hours > hours_per_semester: # If adding the class does not go over the requested amount of hours per semester
                    # Check if the course level is 4000+
                    if int(prereq[1]) >= 4000:
                        # Check if there are already 4000 level classes in the current semester
                        if any(int(course[1]) >= 4000 for course in semesters[semester_index]):
                            # Add the course to the current semester
                            semesters[semester_index].append(prereq)
                            prereq_courses[sets].remove(prereq) # Remove the class that was added from the prereq_courses
                            sem_hours += prereq_hours # Update the current semester hours with the newely added class
                    else:
                        # Add the course to the current semester
                        semesters[semester_index].append(prereq)
                        prereq_courses[sets].remove(prereq) # Remove the class that was added from the prereq_courses
                        sem_hours += prereq_hours # Update the current semester hours with the newely added class
                else:
                    break
    
   
    #4). Add in the blank electives variables
    formatted_data = format_majorclasses(majorClasses) # Calls the format_majorclasses function and saves the returned dicionary to formatted_data
    electives = required_electives(formatted_data)

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
    
    def add_electives(semesters, electives, hours_per_semester):
        for semester_index in range(len(semesters)):
            sem_hours = hours_in_current_sem(semesters[semester_index])  # Calculate total hours in the current semester
            remaining_hours = hours_per_semester - sem_hours  # Calculate remaining hours needed for electives
    
            # Iterate over a copy of the electives array to avoid modifying it while iterating
            for elective in electives.copy():
                elective_hours = int(elective[1][-1])  # Extract the last digit of elective's course number
    
                # Check if adding the elective does not exceed the requested hours_per_semester by more than 2 hours
                if elective_hours <= remaining_hours + 2:
                    semesters[semester_index].append(elective)  # Add elective to the current semester
                    remaining_hours -= elective_hours  # Deduct elective hours from remaining hours
    
                    # Remove the added elective from the electives array to avoid duplicates
                    electives.remove(elective)
    
                    # Check if adding the elective brings the total hours to the requested hours_per_semester
                    if hours_in_current_sem(semesters[semester_index]) >= hours_per_semester:
                        break  # Move to the next semester if the hours limit is met
    add_electives(semesters,electives,hours_per_semester)
    
    return {"semesters":semesters,
            "percentage": percentage}


