from rateMyCourse.models import *
import os
import pandas as pd
# delete all
for m in [School, Teacher, Course, Rate, Department]:
	m.objects.all().delete()

rootPath = "rateMyCourse/static/courseInfo/"
dfs = []
for file in os.listdir(rootPath):
	path = os.path.join(rootPath, file)
	dfs.append(pd.read_csv(open(path,encoding="gbk")))

for i, df in enumerate(dfs):
	dfs[i] = df.drop_duplicates()

# school
buaa = School(name="北京航空航天大学")
buaa.save()

# department
department = set()
for df in dfs:
	for dep in df['开课学院'].unique():
		department.add(dep)
buf = []
for dep in department:
	buf.append(Department(name=dep, school=buaa))
Department.objects.bulk_create(buf)

# teacher
teacher = dict()
for df in dfs:
	for entry in df.iterrows():
		entry = entry[1]
		tstr = entry['老师']
		dep = Department.objects.get(name=entry['开课学院'])
		for t in tstr.split('|'):
			if(len(t) == 3 and t[1] == ' '):
				t = t[0] + t[2]
			if(t == '暂无信息'):
				break
			teacher[t] = dep
buf = []
for t in teacher:
	buf.append(Teacher(name=t, department=teacher[t]))
Teacher.objects.bulk_create(buf)

# course
course = dict()
for df in dfs:
	for entry in df.iterrows():
		entry = entry[1]
		number = entry['课程编号']
		name = entry['课程名']
		coursetype = entry['类型'] + ',' + entry['分类']
		credit = entry['学分']
		department = entry['开课学院']
		teacher = entry['老师'].split('|')
		for i, t in enumerate(teacher):
			if(len(t) == 3 and t[1] == ' '):
				teacher[i] = t[0] + t[2]
			if(t == '暂无信息'):
				teacher.remove(t)
		c = Course(number=number, name=name, coursetype=coursetype, credit=credit, department=Department.objects.get(name=department))
		c.save()
		for t in teacher:
			c.teacher_set.add(Teacher.objects.get(name=t))
		c.save()
