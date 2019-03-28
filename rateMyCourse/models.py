#-*- coding: UTF-8 -*-
from django.db import models

# Create your models here.

class School(models.Model):
    # attributes
    name = models.CharField(max_length=50)

    def __str__(self):
    	return self.name

class Department(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)

    # connections
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
    	return self.name

class Teacher(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    
    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
    	return self.name

class User(models.Model):
    # attributes
    username = models.CharField(max_length=50, unique=True) # 用户名不可重复
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    '''
    grade = models.CharField(max_length=50)
    reported = models.BooleanField()
    '''
    # connections
    '''
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    '''
    def __str__(self):
    	return self.username

class Course(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    website = models.URLField()
    description = models.CharField(max_length=2000, blank=True)
    credit = models.FloatField()
    coursetype = models.CharField(max_length=50)

    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    teacher_set = models.ManyToManyField(
        Teacher,
    )
    def __str__(self):
    	return self.name

class Comment(models.Model):
    # attributes
    anonymous = models.BooleanField(default=False)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()
    # connections
    parentcomment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    term = models.CharField(max_length=50)
    total_score = models.FloatField()
    
    def __str__(self):
    	return self.content

class Rate(models.Model):
    # attributes
    A_score = models.FloatField(default=0) # 有趣程度
    B_score = models.FloatField(default=0) # 充实程度
    C_score = models.FloatField(default=0) # 课程难度
    D_score = models.FloatField(default=0) # 课程收货
    # connections
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    def __str__(self):
    	return "rate from %s"%self.user

class HitCount(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()