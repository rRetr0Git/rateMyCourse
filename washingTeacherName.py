import pandas as pd
from rateMyCourse.models import *
import string
import re


print('washing teacher name......')

dirtyTeachers = Teacher.objects.filter(name__regex=".*[ ].*")
for i in dirtyTeachers:
    print(i.name)
for dirtyTeacher in dirtyTeachers:
    if re.match(r".*[a-zA-Z].*", dirtyTeacher.name):
        continue
    else:
        print(dirtyTeacher.name + 'need to be processed')
        dirtyTeacherId = dirtyTeacher.id
        dirtyTeacherName = dirtyTeacher.name

        cleanTeacherName = dirtyTeacher.name.replace(' ', '')
        cleanTeachers = Teacher.objects.filter(name=cleanTeacherName)

        if len(cleanTeachers) != 0: # clean name exists
            if len(cleanTeachers) > 1: # error
                print(cleanTeacherName + ' repeats!')
                break
            cleanTeacherId = cleanTeachers[0].id
            # modify CourseTeacher & CommentUserCourseTeacher
            dirtyCTs = CourseTeacher.objects.filter(teacherId=dirtyTeacherId)
            for dirtyCT in dirtyCTs:
                if len(CourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=cleanTeacherId)) != 0:
                    CourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=dirtyTeacherId).delete()
                    dirtyCUCTs = CommentUserCourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=dirtyTeacherId)
                    for dirtyCUCT in dirtyCUCTs:
                        Comment.objects.filter(id=dirtyCUCT.commentId.id).delete()
                    CommentUserCourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=dirtyTeacherId).delete()
                else:
                    CourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=dirtyTeacherId).update(teacherId=cleanTeacherId)
                    CommentUserCourseTeacher.objects.filter(courseId=dirtyCT.courseId, teacherId=dirtyTeacherId).update(teacherId=cleanTeacherId)
            # modify Teacher
            Teacher.objects.filter(name=dirtyTeacherName).delete()
            print("combine " + dirtyTeacherName + " with " + cleanTeacherName)
        else: # clean name doesn't exist
            # modify Teacher
            Teacher.objects.filter(name=dirtyTeacherName).update(name=cleanTeacherName)
            print("change " + dirtyTeacherName + " to " + cleanTeacherName)