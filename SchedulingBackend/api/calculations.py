def can_take_class(classes_needed, prerequisites):
    for i in classes_needed:
        course = [classes_needed[i]["CourseSubject"], classes_needed[i]["CourseNum"]]

        if classes_needed[i]["isTaken"] == 0:
            for a in prerequisites:
                if course == [prerequisites[a]["CourseSubject"], prerequisites[a]["CourseNum"]]:
                    for j in classes_needed:
                        if (prerequisites[a]["PreReqCourseSub"], prerequisites[a]["PreReqCourseNum"]) == (classes_needed[j]["CourseSubject"], classes_needed[j]["CourseNum"]) and classes_needed[j]["isTaken"] == 0:
                            course_needed = [prerequisites[a]["PreReqCourseSub"], prerequisites[a]["PreReqCourseNum"]] 
                            print("\nThis student cannot take", course, classes_needed[i]["CourseName"], " until they take ", course_needed)
                            break
                    else:
                        continue


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

        sorted_classes.append((course_subject, course_num, is_taken))

    for course in classes_info:
        course_subject = course['CourseSubject']
        course_num = course['CourseNum']
        is_taken = course['isTaken']  
        dfs(course_subject, course_num)
       

    return sorted_classes



def checkIfTaken(classes):
    classesNotTaken = []
    for class_info in classes:
        if len(class_info) >= 3 and class_info[2] != 1:
            classesNotTaken.append(class_info)
    return classesNotTaken


