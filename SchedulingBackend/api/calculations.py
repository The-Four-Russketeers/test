def preCheck(classes_info, prerequisites_info):
    sorted_classes = []
    visited = set()

    def dfs(course_subject, course_num):
        if (course_subject, course_num) in visited:
            return
        visited.add((course_subject, course_num))

        for pre_req in prerequisites_info:
            if pre_req['CourseSubject'] == course_subject and pre_req['CourseNum'] == course_num:
                pre_req_subject = pre_req['preReqCourseSub']
                pre_req_num = pre_req['preReqCourseNum']
                dfs(pre_req_subject, pre_req_num)

        sorted_classes.append((course_subject, course_num, is_taken, creditHours))

    for course in classes_info:
        course_subject = course['CourseSubject']
        course_num = course['CourseNum']
        is_taken = course['isTaken']
        creditHours = course['CreditHours']  
        dfs(course_subject, course_num)
       

    return sorted_classes

# def getPreqsArray(classes_info, prerequisites_info):
#     prereqMap = {}

#     for prereq in prerequisites_info:
#         course_key = (prereq['CourseSubject'], prereq['CourseNum'])
#         prereq_key = (prereq['preReqCourseSub'], prereq['preReqCourseNum'])

#         if course_key in [(course['CourseSubject'], course['CourseNum']) for course in classes_info]:
#             course_id = f"{course_key[0]}-{course_key[1]}"
#             if course_id not in prereqMap:
#                 prereqMap[course_id] = set()
#             prereqMap[course_id].add(prereq_key)

#     for course_id in prereqMap:
#         prereqMap[course_id] = list(prereqMap[course_id])

#     return prereqMap



def getPreqsArray(classes_info, prerequisites_info):
    prereqMap = {}

    # Iterate through prerequisites_info to build prereqMap
    for prereq in prerequisites_info:
        course_key = (prereq['CourseSubject'], prereq['CourseNum'])
        prereq_key = (
            prereq['preReqCourseSub'], prereq['preReqCourseNum'])

        # Check if course_key exists in classes_info
        course_id = f"{course_key[0]}-{course_key[1]}"
        if course_id in classes_info:
            if course_id not in prereqMap:
                prereqMap[course_id] = []
            prereqMap[course_id].append(prereq_key)

    # Sort prerequisites within the course key based on courseNum
    for course_id, prereqs in prereqMap.items():
        prereqMap[course_id] = sorted(
            prereqs, key=lambda x: x[1])  # Sort by the second element (courseNum)

    # Sort prereqMap keys based on courseNum
    prereqMap = dict(sorted(prereqMap.items(), key=lambda item: item[0].split(
        '-')[1]))  # Sort by courseNum of the keys

    # Convert keys to include isTaken and CreditHours
    new_prereqMap = {}
    for course_id, prereqs in prereqMap.items():
        new_prereqs = []
        for prereq in prereqs:
            prereq_course_subject, prereq_course_num = prereq
            # Retrieve course info from classes_info using prereq key
            prereq_course_id = f"{prereq_course_subject}-{prereq_course_num}"
            course_info = classes_info.get(prereq_course_id)
            if course_info:
                is_taken = course_info.get('isTaken', 0)
                credit_hours = course_info.get('CreditHours', None)
                new_prereqs.append((prereq_course_subject, prereq_course_num, is_taken, credit_hours))
            else:
                # If course info not found, append None values
                new_prereqs.append((prereq_course_subject, prereq_course_num, None, None))

        # Construct the new key as a string concatenating courseID, isTaken, and CreditHours
        if new_prereqs:  # Check if new_prereqs is not empty
            is_taken = new_prereqs[0][2]
            credit_hours = new_prereqs[0][3]
            new_key = f"{course_id}-{is_taken}-{credit_hours}"
        else:
            new_key = f"{course_id}-0-None"  # Default values if new_prereqs is empty
        new_prereqMap[new_key] = new_prereqs
    
    return new_prereqMap






def checkIfTaken(classes):
    classesNotTaken = []
    for class_info in classes:
        if len(class_info) >= 3 and class_info[2] != 1:
            classesNotTaken.append(class_info)
    return classesNotTaken




    
