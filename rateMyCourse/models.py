#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
# Create your models here.

class IMG(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, auto_created=True)
    img = models.ImageField()

class School(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=0) # status状态，正常0，无效1

    def __str__(self):
        return self.name

class Course(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=30)
    website = models.URLField(null=True)
    description = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=10,null=True) # 选修课，必修课
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
    homework = models.FloatField(default=3.0) # 作业量
    difficulty = models.FloatField(default=3.0) # 难易度
    knowledge = models.FloatField(default=3.0) # 收获度
    satisfaction = models.FloatField(default=3.0) # 满意度
    rateCount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " " + str(self.score)

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
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    username = models.CharField(max_length=20, unique=True) # 用户名不可重复
    password = models.CharField(max_length=50)
    isTeacher = models.BooleanField(default=False)
    schoolName = models.CharField(max_length=30,null=True)
    departmentName = models.CharField(max_length=20,null=True)
    img = models.ImageField(default='user.png')
    mail = models.CharField(max_length=40)
    def __str__(self):
        return self.username

class Teacher(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    name = models.CharField(max_length=100,unique=True)
    website = models.URLField(null=True)
    img = models.ImageField(default='user.png')
    status = models.IntegerField(default=0)
    allHomeworkScore = models.IntegerField(default=0)
    allDifficultyScore = models.IntegerField(default=0)
    allKnowledgeScore = models.IntegerField(default=0)
    allSatisfactionScore = models.IntegerField(default=0)
    commentCnt = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Comment(models.Model):
    # attributes
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    anonymous = models.BooleanField(default=False)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()
    isRoot = models.BooleanField(default=True)
    parentComment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
    )
    img = models.ImageField(null=True)
    homework = models.IntegerField(default=3)  # 作业量
    difficulty = models.IntegerField(default=3)  # 难易度
    knowledge = models.IntegerField(default=3)  # 收获度
    satisfaction = models.IntegerField(default=3)  # 满意度
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    def __str__(self):
        return self.content

class SchoolCourse(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
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
    def __str__(self):
        return str(self.schoolId)+" "+str(self.courseId)


class CourseTeacher(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
    courseId = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    teacherId = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
    )
    allHomeworkScore = models.IntegerField(default=0)
    allDifficultyScore = models.IntegerField(default=0)
    allKnowledgeScore = models.IntegerField(default=0)
    allSatisfactionScore = models.IntegerField(default=0)
    commentCnt = models.IntegerField(default=0)
    class Meta:
        unique_together = ("courseId", "teacherId")
    def __str__(self):
        return str(self.courseId) + " " + str(self.teacherId)


class CommentUserCourseTeacher(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4,auto_created=True)
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
    teacherId = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
    )
    class Meta:
        unique_together = ("commentId", "userId", "courseId", "teacherId")

    def __str__(self):
        return str(self.courseId) + " " + str(self.courseId) + " " + str(self.teacherId)


class HitCount(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()
