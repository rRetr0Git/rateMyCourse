#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class School(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=0)

    def __str__(self):
    	return self.name

class Course(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False)
    name = models.CharField(max_length=20)
    website = models.URLField(null=True)
    description = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=10,null=True)
    status = models.IntegerField(default=0)
    def __str__(self):
    	return self.name

class CourseRate(models.Model):
    # attributes
    id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False
    )
    score = models.FloatField(default=3.0)
    homework = models.FloatField(default=3.0)#作业量
    difficulty = models.FloatField(default=3.0)#难易度
    knowledge = models.FloatField(default=3.0)#收获度
    satisfaction = models.FloatField(default=3.0)#满意度
    rateCount = models.IntegerField(default=0)

class CourseKeyWord(models.Model):
    # attributes
    id = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False
    )
    keyword1 = models.CharField(max_length=10, null=True)
    keyword2 = models.CharField(max_length=10, null=True)
    keyword3 = models.CharField(max_length=10, null=True)
    keyword4 = models.CharField(max_length=10, null=True)
    keyword5 = models.CharField(max_length=10, null=True)

class User(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True)
    username = models.CharField(max_length=20, unique=True) # 用户名不可重复
    password = models.CharField(max_length=50)
    isTeacher = models.BooleanField(default=False)
    schoolName = models.CharField(max_length=30,null=True)
    departmentName = models.CharField(max_length=20,null=True)
    img = models.URLField(blank=True,null=True)
    def __str__(self):
    	return self.username

class Teacher(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False)
    name = models.CharField(max_length=10)
    website = models.URLField(null=True)
    img = models.URLField(null=True)
    status = models.IntegerField(default=0)
    def __str__(self):
    	return self.name

class Comment(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False)
    anonymous = models.BooleanField(default=False)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()
    isRoot = models.BooleanField(default=True)
    parentComment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
    )
    img = models.URLField(blank=True,null=True)
    homework = models.IntegerField(default=3)  # 作业量
    difficulty = models.IntegerField(default=3)  # 难易度
    knowledge = models.IntegerField(default=3)  # 收获度
    satisfaction = models.IntegerField(default=3)  # 满意度
    def __str__(self):
    	return self.content

class SchoolCourse(models.Model):
    schoolId = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
    )
    courseId = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ("schoolId", "courseId")


class CourseTeacher(models.Model):
    courseId = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    teacherId = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ("courseId", "teacherId")


class CommentUserCourse(models.Model):
    commentId = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    userId = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    courseId = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ("commentId", "userId","courseId")


class HitCount(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()