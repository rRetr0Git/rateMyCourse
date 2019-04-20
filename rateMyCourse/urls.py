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

    #POST
    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^submitComment/$', views.submitComment, name='submitComment'),

    #TMP GET IN INDEX
    url(r'^getSchool/$', views.getSchool, name='getSchool'),
    url(r'^getDepartment/$', views.getDepartment, name='getDepartment'),
    # url(r'^getCourse/$', views.getCourse, name='getCourse'),
    url(r'^getComment/$', views.getComment, name='getComment'),
    # url(r'^getTeachers/$', views.getTeachers, name='getTeachers'),
    # url(r'^getOverAllRate/$', views.getOverAllRate, name='getOverAllRate'),

    url(r'^userInfo/$', views.userInfo, name='userInfo'),
    url(r'^saveUserInfo/$',views.saveUserInfo,name='saveUserInfo'),
    url(r'^rank/$',views.getRank,name='getRank'),

    # test for modifying user's avatar
    # url(r'^upload', views.upload),
    # url(r'^show', views.show),
] ## + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
