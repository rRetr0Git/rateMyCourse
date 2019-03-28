from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(School)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Rate)
admin.site.register(HitCount)
