# Create classesNeeded dictionary with numbered keys and isTaken flag
def transform_for_generate_schedule(data):
    classesNeeded = {}
    for index, course in enumerate(data, 1):
        classesNeeded[index] = {
            "CourseSubject": course[0],
            "CourseNum": course[1],
            "CourseName": course[2],
            "isTaken": course[3],  # Assuming isTaken is initially set to 0 for all courses
            "CreditHours" : course[4]
        }
    return(classesNeeded)

# Get a percentage on how far the student is in their major
import math

def percentage_done(data):
    taken = 0 
    for i in data:
        if data[i]["isTaken"] == 1:
            taken+=1 # Number of classes they have taken
    percentage = math.ceil(taken/len(data) * 100) # Divide the number of classes taken by how many they need (rounded up)
    return(percentage)
