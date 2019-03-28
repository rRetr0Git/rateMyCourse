from django.test import TestCase
from django.test import Client
from rateMyCourse.models import *
from rateMyCourse.views import *

import json
# Create your tests here.

class APITestCase(TestCase):
	def test_addHitCount(self):
		HitCount(name='hit', count=0).save()
		hit1 = HitCount.objects.get(name='hit').count
		addHitCount()
		hit2 = HitCount.objects.get(name='hit').count
		self.assertEqual(hit1, hit2 - 1)

	def test_signUp(self):
		c = Client()
		response = json.loads(c.post('/signUp/', {'username': 'testuser', 'password': 'testpassword'}).content)
		self.assertEqual(response['statCode'], -1)
		response = json.loads(c.post('/signUp/', {'username': 'testuser', 'password': 'testpassword', 'mail': 'testemail@test.com'}).content)
		self.assertEqual(response['statCode'], 0)
		response = json.loads(c.post('/signUp/', {'username': 'testuser2', 'password': 'testpassword', 'mail': 'testemail@test.com'}).content)
		self.assertEqual(response['statCode'], -2)

	def test_signIn(self):
		c = Client()
		User(username='testuser', mail='testemail@test.com', password='testpassword').save()
		response = json.loads(c.post('/signIn/', {'username': 'testuser', 'password': 'testpassword'}).content)
		self.assertEqual(response['statCode'], 0)
		response = json.loads(c.post('/signIn/', {'username': 'testuser2', 'password': 'testpassword'}).content)
		self.assertEqual(response['statCode'], -2)
		response = json.loads(c.post('/signIn/', {'username': 'testuser', 'password': 'wrongpassword'}).content)
		self.assertEqual(response['statCode'], -3)


	def test_getSchool(self):
		c = Client()
		School(name="testschool1").save()
		School(name="testschool2").save()
		response = json.loads(c.get('/getSchool/').content)
		self.assertEqual(response['school'], ['testschool1', 'testschool2'])

	def test_getDepartment(self):
		c = Client()
		s = School(name="testschool")
		s.save()
		Department(name="testdep1", school=s).save()
		Department(name="testdep2", school=s).save()
		response = json.loads(c.get('/getDepartment/', {'school': 'testschool'}).content)
		self.assertEqual(response['department'], ['testdep1', 'testdep2'])

	def test_getTeachers(self):
		c = Client()
		crs = Course(number="testcourse", credit=3)
		crs.save()
		t1 = Teacher(name="teacher1")
		t2 = Teacher(name="teacher2")
		t1.save()
		t2.save()
		crs.teacher_set.add(t1)
		crs.teacher_set.add(t2)
		crs.save()
		response = json.loads(c.get('/getTeachers/', {'course_number': 'testcourse'}).content)
		self.assertEqual(response['statCode'], 0)
		self.assertEqual(response['teachers'], [["teacher1", "teacher2"]])

	def test_getComments(self):
		c = Client()
		crs = Course(number="testcourse", credit=3)
		crs.save()
		t1 = Teacher(name="teacher1")
		t2 = Teacher(name="teacher2")
		t1.save()
		t2.save()
		crs.teacher_set.add(t1)
		crs.teacher_set.add(t2)
		crs.save()
		response = json.loads(c.get('/getTeachers/', {'course_number': 'testcourse'}).content)
		self.assertEqual(response['statCode'], 0)
		self.assertEqual(response['teachers'], [["teacher1", "teacher2"]])


	def test_getOverAllRate(self):
		c = Client()
		crs = Course(number="testcourse", credit=3)
		crs.save()
		t1 = Teacher(name="teacher1")
		t2 = Teacher(name="teacher2")
		t1.save()
		t2.save()
		crs.teacher_set.add(t1)
		crs.teacher_set.add(t2)
		crs.save()
		response = json.loads(c.get('/getTeachers/', {'course_number': 'testcourse'}).content)
		self.assertEqual(response['statCode'], 0)
		self.assertEqual(response['teachers'], [["teacher1", "teacher2"]])