import pandas as pd
from rateMyCourse.models import *
import string
print('cleaning data......')
for table in [School, Course, Teacher, SchoolCourse, CourseTeacher,CommentUserCourseTeacher,Comment]:
	table.objects.all().delete()
print('cleaning finished!')
print('importing data......')
print('please be patient......')
buaa = School(name="北京航空航天大学")
buaa.save()
school_uuid = School.objects.get(name="北京航空航天大学").id
#print(school_uuid)
df1 = pd.read_csv(open('course_data_new.csv',encoding="utf-8"))
df2 = pd.read_csv(open('teacher.csv',encoding="utf-8"))
for row in df1.iterrows():
	row = row[1]
	name = row['课程名称']
	department = row['开课院系']
	type = row['课程性质']
	description = row['课程类别']
	teachers = row['教师信息'].split('+')
	course = Course(name=name, department=department, type=type, description=description)
	course.save()
	course_uuid = course.id
	sc = SchoolCourse(schoolId=buaa, courseId=course)
	sc.save()
	for each in teachers:
		if each != "N/A":
			teacher = Teacher.objects.filter(name=each)
			if len(teacher)==0:
				search = df2.loc[df2['姓名']==each.replace(' ','')]
				if search.empty!=True:
					t_row = search.iloc[0]
					t_website = t_row['个人主页']
					t_img = t_row['个人照片']
					teacher = Teacher(name=each,website=t_website,img=t_img)
					#print(t_website,t_img)
				else:
					teacher = Teacher(name=each)
				teacher.save()
			else:
				teacher = teacher[0]
			teacher_uuid = teacher.id
			try:
				ct = CourseTeacher(courseId=course,teacherId=teacher)
				ct.save()
			except:
				continue
print('import finished!')