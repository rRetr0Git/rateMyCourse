import pandas as pd
from rateMyCourse.models import *
import string

for table in [School, Course, Teacher, SchoolCourse, CourseTeacher]:
	table.objects.all().delete()

buaa = School(name="北京航空航天大学")
buaa.save()
school_uuid = School.objects.get(name="北京航空航天大学").id
print(school_uuid)
df = pd.read_csv(open('filtered.csv',encoding="utf-8"))

for row in df.iterrows():
	row = row[1]
	name = row['课程名称']
	department = row['开课院系']
	type = row['课程性质']
	description = row['课程类别']
	teachers = row['教师信息'].split('+')
	for each in teachers:
		if each != "N/A":
			course = Course(name=name, department=department, type=type, description=description)
			course.save()
			course_uuid = course.id
			teacher = Teacher(name=each)
			teacher.save()
			teacher_uuid = teacher.id
			ct = CourseTeacher(courseId=course,teacherId=teacher)
			ct.save()
			sc = SchoolCourse(schoolId=buaa,courseId=course)
			sc.save()