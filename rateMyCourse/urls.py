from django.conf.urls import url, include
from django.contrib import admin
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #GET
    url(r'^$', views.getIndex, name='getIndex'),
    url(r'^index/$', views.getIndex, name='getIndex'),
    url(r'^search/$', views.search, name='search'),
    url(r'^course/(?P<courseTeacherId>[0-9A-Za-z\-]+)/$', views.coursePage, name='coursePage'),
    url(r'^course/(?P<courseTeacherId>[0-9A-Za-z\-]+)/rate/$', views.ratePage, name='ratePage'),
    url(r'^teacher/(?P<teacherId>[0-9A-Za-z\-]+)/$', views.teacherPage, name='teacherPage'),
    url(r'^adminstrator/$', views.adminPage, name='adminPage'),

    #POST
    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^signOut/$', views.signOut, name='signOut'),
    url(r'^send_resetPWD_email/$', views.send_resetPWD_email, name='send_resetPWD_email'),
    url(r'^toResetPWD/(\w*)/$', views.toResetPWD, name='toResetPWD'),
    url(r'^resetPWD/$', views.resetPWD, name='resetPWD'),
    url(r'^submitComment/$', views.submitComment, name='submitComment'),

    #TMP GET IN INDEX
    # url(r'^getSchool/$', views.getSchool, name='getSchool'),
    url(r'^getDepartment/$', views.getDepartment, name='getDepartment'),
    # url(r'^getCourse/$', views.getCourse, name='getCourse'),
    url(r'^getComment/$', views.getComment, name='getComment'),
    # url(r'^getTeachers/$', views.getTeachers, name='getTeachers'),
    # url(r'^getOverAllRate/$', views.getOverAllRate, name='getOverAllRate'),

    url(r'^userInfo/$', views.userInfo, name='userInfo'),
    url(r'^saveUserInfo/$', views.saveUserInfo, name='saveUserInfo'),
    url(r'^saveUserPic/$', views.saveUserPic, name='saveUserPic'),
    url(r'^rank/$', views.getRank, name='getRank'),
    url(r'^addLike/$', views.addLike, name='addLike'),
    url(r'^addDislike/$', views.addDislike, name='addDislike'),

    url(r'^active/(?P<active_code>\w*)/$', views.active, name='userActive'),
    url(r'^getCaptcha/$', views.getCaptcha, name='getCaptcha'),
    url(r'^userDeleteComment/$', views.userDeleteComment, name='userDeleteComment'),
    url(r'^adminDeleteComment/$', views.adminDeleteComment, name='adminDeleteComment'),
    url(r'^getMailNum/$', views.getMailNum, name='getMailNum')
]
