from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(School)
# admin.site.register(CourseRate)
admin.site.register(CourseKeyWord)
admin.site.register(Teacher)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(SchoolCourse)
admin.site.register(CourseTeacher)
admin.site.register(CommentUserCourseTeacher)
admin.site.register(HitCount)
admin.site.register(EmailVerifyRecord)
admin.site.register(AdminDeleteCommentRecord)
