from django.contrib.sites import requests
from django.shortcuts import render, get_list_or_404
from rateMyCourse.models import *
from django.db.models import Q
import json
from urllib import request, parse
from django.http import HttpResponse
from django.utils import timezone
import numpy as np
import time
import os
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed


# @timeit
# def upload(request):
#     return render(request, 'rateMyCourse/templates/uploadpic/upload.html')


# @timeit
# def show(request):
#     new_img = IMG(img=request.FILES.get('img'))
#     new_img.save()
#     content = {
#         'aaa': new_img,
#     }
#     return render(request, 'rateMyCourse/templates/uploadpic/show.html', content)


@timeit
def addHitCount():
    try:
        hit = HitCount.objects.get(name='hit')
    except Exception:
        hit = HitCount(name='hit', count=0)
        hit.save()
    hit.count += 1
    hit.save()


@timeit
def getIndex(request):
    #addHitCount()
    return render(request, "rateMyCourse/index.html")


@timeit
def signUp(request):
    """
    注册后登录的代码复制了signIn，很蠢
    """
    if request.session.get('is_login', False):
        request.session.flush()
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username, mail or password',
            }))
    try:
        new_password = make_password(password)
        User(username=username, mail=mail, password=new_password).save()
    except Exception as err:
        errmsg = str(err)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': 'something wrong in mail',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': 'something wrong in username',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': 'something wrong in ... well i don\'t know',
                }))
    else:
        try:
            username = request.POST['username']
            password = request.POST['password']
        except Exception:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'errormessage': 'can not get username or mail or password',
            }))
        try:
            u = User.objects.get(username=username)
        except Exception:
            try:
                u = User.objects.get(mail=username)
            except Exception:
                return HttpResponse(json.dumps({
                    'statCode': -2,
                    'errormessage': 'username or mail doesn\'t exists',
                }))
        if not check_password(password, u.password):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': 'wrong password',
            }))
        else:
            addHitCount()
            request.session['userid'] = str(u.id)
            request.session['username'] = u.username
            request.session['is_login'] = True
            return HttpResponse(json.dumps({
                'statCode': 0,
                'username': u.username,
            }))

    '''
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)
    '''


@timeit
def simpleSearch(school, department, keywords):
    if school == None:
        courseList = Course.objects.filter(Q(name__icontains=keywords) | Q(type__icontains=keywords))
        courseTeacherList = CourseTeacher.objects.filter(courseId__in=courseList)
    else:
        if department == None:
            school = School.objects.get(name=school)
            courseIdList = [c.courseId.id for c in SchoolCourse.objects.filter(schoolId=school)]
            courseList = Course.objects.filter(id__in = courseIdList).filter(Q(name__icontains=keywords) | Q(type__icontains=keywords))
            courseTeacherList = CourseTeacher.objects.filter(courseId__in=courseList)
        else:
            school = School.objects.get(name=school)
            courseIdList = [c.courseId.id for c in SchoolCourse.objects.filter(schoolId=school)]
            courseList = Course.objects.filter(id__in = courseIdList, department=department).filter(Q(name__icontains=keywords) | Q(type__icontains=keywords))
            courseTeacherList = CourseTeacher.objects.filter(courseId__in=courseList)
    return courseTeacherList


@timeit
def search(request):
    # addHitCount()
    keywords = request.GET['keywords']
    if('school' in request.GET):
        school = request.GET['school']
    else:
        school = None
    if('department' in request.GET):
        department = request.GET['department']
    else:
        department = None

    courses = []
    pages = []
    courseTeacherList = simpleSearch(school, department, keywords)
    for ct in courseTeacherList:
        course = ct.courseId
        teacher = ct.teacherId

        count = ct.commentCnt
        if count == 0:
            avg_score = 3
        else:
            avg_score = (ct.allHomeworkScore + ct.allDifficultyScore + ct.allKnowledgeScore + ct.allSatisfactionScore) / 4 / count
        courses.append({
            'name': course.name,
            'courseTeacher' : ct.id,
            'teacher': teacher.name,
            'teacherId': teacher.id,
            'type': course.type,
            'department': course.department,
            'rateScore': '%.1f' % avg_score,
            'ratenumber': count
        })

    pn=int(len(courses)/10)+1
    for i in range(pn):
        pages.append({'number': i+1})
    return render(request, "rateMyCourse/searchResult_new.html", {
    	'courses': courses,
    	'count': len(courses),
    	'pages': pages,
    	})


@timeit
def coursePage(request, courseTeacherId):
    # addHitCount()
    courseTeacher = CourseTeacher.objects.get(id=courseTeacherId)
    course = Course.objects.get(id=courseTeacher.courseId.id)
    teacher = Teacher.objects.get(id=courseTeacher.teacherId.id)

    count = courseTeacher.commentCnt
    if count == 0:
        homework = 3
        difficulty = 3
        knowledge = 3
        satisfaction = 3
        avg_score = 3
    else:
        homework = courseTeacher.allHomeworkScore / count
        difficulty = courseTeacher.allDifficultyScore / count
        knowledge = courseTeacher.allKnowledgeScore / count
        satisfaction = courseTeacher.allSatisfactionScore / count
        avg_score = (homework + difficulty + knowledge + satisfaction) / 4

    other_teacher_info = []
    other_cts = CourseTeacher.objects.filter(courseId=course.id).filter(~Q(teacherId=teacher.id))
    for other_ct in other_cts:
        other_teacher = other_ct.teacherId
        other_count = other_teacher.commentCnt
        if other_count == 0:
            other_avg_score = 3
        else:
            other_avg_score = (other_teacher.allHomeworkScore + other_teacher.allDifficultyScore + other_teacher.allKnowledgeScore + other_teacher.allSatisfactionScore) / 4 / other_count
        other_teacher_info.append({"id":other_ct.id, "name":other_teacher.name, "teacherId":other_teacher.id,"score":'%.1f'%other_avg_score})

    other_course_info = []
    other_cts = CourseTeacher.objects.filter(teacherId=teacher.id).filter(~Q(courseId=course.id))
    for other_ct in other_cts:
        other_count = other_ct.commentCnt
        if other_count == 0:
            other_avg_score = 3
        else:
            other_avg_score = (other_ct.allHomeworkScore + other_ct.allDifficultyScore + other_ct.allKnowledgeScore + other_ct.allSatisfactionScore) / 4 / other_count
        other_course_info.append({"id":other_ct.id, "name":other_ct.courseId.name, "teacherId":other_ct.teacherId.id,"score":'%.1f'%other_avg_score})

    return render(request, "rateMyCourse/coursePage_new.html", {
        'course_name': course.name,
        'course_profession': course.department,
        'course_type': course.type,
        'course_scores': '%.1f'% avg_score,
        'percent1': str(homework*20)+'%',
        'percent2': str(difficulty * 20) + '%',
        'percent3': str(knowledge * 20) + '%',
        'percent4': str(satisfaction * 20) + '%',
        'detail1': '%.1f'%homework,
        'detail2': '%.1f'%difficulty,
        'detail3': '%.1f'%knowledge,
        'detail4': '%.1f'%satisfaction,
        'course_website': course.website if course.website != '' else '.',
        'profession_website': "https://baidu.com",
        'course_teacher': teacher.name,
        'teacherId':teacher.id,
        'courseteacherid': courseTeacher.id,
        'other_teacher_info': other_teacher_info,
        'other_course_info': other_course_info
        })


@timeit
def ratePage(request, courseTeacherId):
    # addHitCount()
    courseTeacher = CourseTeacher.objects.get(id=courseTeacherId)
    course = courseTeacher.courseId
    teacher = courseTeacher.teacherId
    return render(request, "rateMyCourse/ratePage_new.html", {
            'course': {
                'name': course.name,
                'description': course.description,
                'department': course.department,
            },
            'teacher': teacher.name,
            'aspect1': '作业量合理',
            'aspect2': '难度合理',
            'aspect3': '知识量',
            'aspect4': '满意度',
        })

@timeit
def teacherPage(request, teacherId):
    # addHitCount()
    teacher = Teacher.objects.get(id=teacherId)
    teacherId = teacher.id
    courseList = []
    cts = CourseTeacher.objects.filter(teacherId=teacherId)
    for ct in cts:
        course = ct.courseId
        courseList.append({'courseId': course.id, 'courseName': course.name, 'courseScore': (ct.allHomeworkScore + ct.allKnowledgeScore + ct.allSatisfactionScore + ct.allDifficultyScore) / ct.commentCnt / 4})
    return render(request, "rateMyCourse/teacherPage.html",{
        'teacherName':teacher.name,
        'teacherImg':teacher.img if teacher.img != "user.png" else '/static/ratemycourse/images/upload/user/user.png',
        'teacherWeb':teacher.website,
        'courseList':courseList,
        'teacherScore': (teacher.allDifficultyScore + teacher.allSatisfactionScore + teacher.allKnowledgeScore + teacher.allHomeworkScore) / teacher.commentCnt / 4
    })

@timeit
def signIn(request):
    if request.session.get('is_login', False):
        request.session.flush()
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username or mail or password',
            }))
    try:
        u = User.objects.get(username=username)
    except Exception:
        try:
            u = User.objects.get(mail=username)
        except Exception:
            return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'username or mail doesn\'t exists',
            }))
    if not check_password(password, u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'wrong password',
            }))
    else:
        addHitCount()
        request.session['userid'] = str(u.id)
        request.session['username'] = u.username
        request.session['is_login'] = True
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': u.username,
            }))


@timeit
def signOut(request):
    if request.session.get("is_login", False):
        request.session.flush()
        return HttpResponse(json.dumps({
            'statCode': 0
        }))
    else:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '用户未登录'
        }))

@timeit
def getSchool(request):
    result = {
        'school': [s.name for s in School.objects.all()],
    }
    return HttpResponse(json.dumps(result))


@timeit
def getDepartment(request):
    try:
        school = School.objects.get(name=request.GET['school'])
        department_set = SchoolCourse.objects.filter(schoolId=school.id).values("courseId__department").distinct()
        department = [ds['courseId__department'] for ds in department_set]
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school not found'
            }))
    return HttpResponse(json.dumps({
        'department': department
        }))


# @timeit
# def getCourse(request):
#     try:
#         school = School.objects.get(name=request.GET['school'])
#         department = school.department_set.get(name=request.GET['department'])
#         course = Course.objects.filter(school=school, department=department).distinct()
#     except Exception as err:
#         return HttpResponse(json.dumps({
#             'error': 'school or department not found'
#             }))
#     return HttpResponse(json.dumps({
#         'course': [c.name for c in course]
#         }))


@timeit
def getComment(request):
    try:
        courseTeacherId = request.GET['courseTeacherId']
        ct = CourseTeacher.objects.get(id=courseTeacherId)
        course = ct.courseId
        teacher = ct.teacherId
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get courseId or courseId not exists',
            }))
    cmtList = []
    cuctList = CommentUserCourseTeacher.objects.filter(courseId=course, teacherId=teacher)
    for cuct in cuctList:
        user = cuct.userId
        cmt = cuct.commentId
        cmtList.append({
            'userName': user.username if cmt.anonymous == False else '匿名用户',
            'userid': str(user.id) if cmt.anonymous == False else '',
            'text': cmt.content.replace("\n", "<br>"),
            'time': cmt.time.strftime('%y/%m/%d'),
            'avator': User.objects.get(username=user).img.url if cmt.anonymous == False else '/static/ratemycourse/images/upload/user/user.png'
            })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))


# @timeit
# def getTeachers(request):
#     try:
#         course = request.GET['courseId']
#         cts = CourseTeacher.objects.filter(courseId=course)
#     except Exception:
#         return HttpResponse(json.dumps({
#             'statCode': -1,
#             'errormessage': 'can not get courseId or courseId not exists',
#             }))
#     tList = [ct.teacherId.name for ct in cts]
#     return HttpResponse(json.dumps({
#         'statCode': 0,
#         'teachers': tList,
#         }))


# @timeit
# def getOverAllRate(request):
#     try:
#         course = request.GET['courseId']
#         courses = Course.objects.filter(number=course)
#     except Exception:
#         return HttpResponse(json.dumps({
#             'statCode': -1,
#             'errormessage': 'can not get courseId or courseId not exists',
#             }))
#     return HttpResponse(json.dumps({
#         'statCode': 0,
#         'rate': getAvgScore(courses),
#         }))


@timeit
def submitComment(request):
    # addHitCount()
    if not request.session.get('is_login', False):
        return render(request, "rateMyCourse/index.html")
    try:
        username = request.session['username']
        content = request.POST['comment']
        rate = request.POST.getlist('rate')
        for i, j in enumerate(rate):
            rate[i] = int(j)
        courseTeacherId = request.POST['courseteacher']
        anonymous = request.POST['anonymous']
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
        }))
    user = User.objects.get(username=username)
    ct = CourseTeacher.objects.get(id=courseTeacherId)
    course = ct.courseId
    teacher = ct.teacherId
    if(rate[0]<=0 or rate[0]>5 or rate[1]<=0 or rate[1]>5 or rate[2]<=0 or rate[2]>5 or rate[3]<=0 or rate[3]>5):
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information invalid! ',
        }))
    postCheckStatus=0
    for i in range(len(content)):
        if content[i]=='<':
            postCheckStatus += 1;
        elif content[i]=='>' and postCheckStatus>0:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'errormessage': '\'<\' or \'>\' is forbidden in comment',
            }))
    preComment = CommentUserCourseTeacher.objects.filter(userId=user,courseId=course,teacherId=teacher)
    if(len(preComment)==0):
        comment = Comment(
            anonymous=True if anonymous == 'true' else False,
            content=content,
            time=timezone.now(),
            homework = rate[0],
            difficulty=rate[1],
            knowledge=rate[2],
            satisfaction=rate[3]
        )
        comment.save()
        cuct = CommentUserCourseTeacher(commentId=comment,userId=user,courseId=course,teacherId=teacher)
        cuct.save()
        Teacher.objects.filter(id=teacher.id).update(allHomeworkScore=teacher.allHomeworkScore + rate[0],
                                                     allDifficultyScore=teacher.allDifficultyScore + rate[1],
                                                     allKnowledgeScore=teacher.allKnowledgeScore + rate[2],
                                                     allSatisfactionScore=teacher.allSatisfactionScore + rate[3],
                                                     commentCnt=teacher.commentCnt + 1
                                                     )
        CourseTeacher.objects.filter(id=ct.id).update(allHomeworkScore=ct.allHomeworkScore + rate[0],
                                                      allDifficultyScore=ct.allDifficultyScore + rate[1],
                                                      allKnowledgeScore=ct.allKnowledgeScore + rate[2],
                                                      allSatisfactionScore=ct.allSatisfactionScore + rate[3],
                                                      commentCnt=ct.commentCnt + 1
                                                      )
    else:
        comment = preComment[0].commentId
        rate1=comment.homework
        rate2=comment.difficulty
        rate3=comment.knowledge
        rate4=comment.satisfaction
        Comment.objects.filter(id=comment.id).update(
            anonymous=True if anonymous == 'true' else False,
            content=content,
            time=timezone.now(),
            homework = rate[0],
            difficulty=rate[1],
            knowledge=rate[2],
            satisfaction=rate[3]
        )
        Teacher.objects.filter(id=teacher.id).update(allHomeworkScore=teacher.allHomeworkScore - rate1 + rate[0],
                                                     allDifficultyScore=teacher.allDifficultyScore - rate2 + rate[1],
                                                     allKnowledgeScore=teacher.allKnowledgeScore -rate3 + rate[2],
                                                     allSatisfactionScore=teacher.allSatisfactionScore -rate4 + rate[3],
                                                     )
        CourseTeacher.objects.filter(id=ct.id).update(allHomeworkScore=ct.allHomeworkScore -rate1 + rate[0],
                                                      allDifficultyScore=ct.allDifficultyScore -rate2 + rate[1],
                                                      allKnowledgeScore=ct.allKnowledgeScore -rate3 + rate[2],
                                                      allSatisfactionScore=ct.allSatisfactionScore -rate4 + rate[3],
                                                      )
    return HttpResponse(json.dumps({
        'statCode': 0,
    }))


@timeit
def userInfo(request):
    name = request.GET['name']
    user = User.objects.get(username = name)
    commentList=[]
    cuctList = CommentUserCourseTeacher.objects.filter(userId=user.id)
    for cuct in cuctList:
        teacher = cuct.teacherId
        course = cuct.courseId
        courseTeacher = CourseTeacher.objects.get(teacherId=teacher,courseId=course)
        cmt = cuct.commentId
        if cmt.anonymous == True:
            continue
        commentList.append({
            'course': course.name,
            'courseTeacher': courseTeacher.id,
            'teacher': teacher.name,
            'rate': [cmt.homework, cmt.difficulty, cmt.knowledge, cmt.satisfaction],
            'time': cmt.time.strftime('%y/%m/%d'),
            })
    school = School.objects.get(name='北京航空航天大学')
    department_set = SchoolCourse.objects.filter(schoolId=school.id).values("courseId__department").distinct()
    departments = [ds['courseId__department'] for ds in department_set]

    return render(request, "rateMyCourse/userInfo.html",{
	    'username': name,
	    'isTeacher': user.isTeacher,
	    'schoolName': user.schoolName,
	    'departmentName': user.departmentName,
	    'img': user.img.url,
	    'commentList': commentList,
        'departments': departments,
    })


def saveUserPic(request):
    if not request.session.get('is_login', False):
        return render(request, "rateMyCourse/index.html")
    username = request.session.get('username')
    img_name = request.FILES.get('file')
    user = User.objects.get(username=username)

    old_img_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') + '/rateMyCourse' + User.objects.get(username=username).img.url
    if old_img_url != os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/') + '/rateMyCourse/rateMyCourse/static/ratemycourse/images/upload/user/user.png':
        os.remove(old_img_url)

    img_name.name = str(user.id) + '.png'
    new_img = IMG(img=img_name)
    new_img.save()
    User.objects.filter(username=username).update(img=img_name)

    commentList = []
    cuctList = CommentUserCourseTeacher.objects.filter(userId=user.id)
    for cuct in cuctList:
        teacher = cuct.teacherId
        course = cuct.courseId
        courseTeacher = CourseTeacher.objects.get(teacherId=teacher, courseId=course)
        cmt = cuct.commentId
        if cmt.anonymous == True:
            continue
        commentList.append({
            'course': course.name,
            'courseTeacher': courseTeacher.id,
            'teacher': teacher.name,
            'rate': [cmt.homework, cmt.difficulty, cmt.knowledge, cmt.satisfaction],
            'time': cmt.time.strftime('%y/%m/%d'),
        })

    return render(request, "rateMyCourse/userInfo.html", {
        'username': username,
        'isTeacher': user.isTeacher,
        'schoolName': user.schoolName,
        'departmentName': user.departmentName,
        'img': user.img.url,
        'commentList': commentList,
    })


@timeit
def saveUserInfo(request):
    if not request.session.get('is_login', False):
        return render(request, "rateMyCourse/index.html")
    school = request.POST['school']
    department = request.POST['department']
    username = request.session.get('username')
    user = User.objects.filter(username=username)
    user.update(schoolName=school,departmentName=department)

    user = User.objects.get(username=username)
    commentList = []
    cuctList = CommentUserCourseTeacher.objects.filter(userId=user.id)
    for cuct in cuctList:
        teacher = cuct.teacherId
        course = cuct.courseId
        courseTeacher = CourseTeacher.objects.get(teacherId=teacher, courseId=course)
        cmt = cuct.commentId
        if cmt.anonymous == True:
            continue
        commentList.append({
            'course': course.name,
            'courseTeacher': courseTeacher.id,
            'teacher': teacher.name,
            'rate': [cmt.homework, cmt.difficulty, cmt.knowledge, cmt.satisfaction],
            'time': cmt.time.strftime('%y/%m/%d'),
        })
    return render(request, "rateMyCourse/userInfo.html", {
        'username': username,
        'isTeacher': user.isTeacher,
        'schoolName': user.schoolName,
        'departmentName': user.departmentName,
        'img': user.img.url,
        'commentList': commentList,
    })


@timeit
def getRank(request):
    top_course_ids = []
    top_course_scores = []
    top_course_counts = []
    top_teacher_ids = []
    top_teacher_scores = []
    top_teacher_counts = []
    for cuct in CommentUserCourseTeacher.objects.all():
        ct = CourseTeacher.objects.get(courseId=cuct.courseId, teacherId=cuct.teacherId)
        count = ct.commentCnt
        avg_score = (ct.allHomeworkScore + ct.allDifficultyScore + ct.allKnowledgeScore + ct.allSatisfactionScore) / 4 / count
        if ct.id in top_course_ids:
            index = top_course_ids.index(ct.id)
            top_course_scores[index] += avg_score
            top_course_counts[index] += 1
        else:
            top_course_ids.append(ct.id)
            top_course_scores.append(avg_score)
            top_course_counts.append(1)
        if ct.teacherId.id in top_teacher_ids:
            index = top_teacher_ids.index(ct.teacherId.id)
            top_teacher_scores[index] += avg_score
            top_teacher_counts[index] += 1
        else:
            top_teacher_ids.append(ct.teacherId.id)
            top_teacher_scores.append(avg_score)
            top_teacher_counts.append(1)
    for i in range(len(top_course_scores)):
        top_course_scores[i] /= top_course_counts[i]
    for i in range(len(top_teacher_scores)):
        top_teacher_scores[i] /= top_teacher_counts[i]

    if len(top_course_scores) < 20:
        courseRange = len(top_course_scores)
    else:
        courseRange = 20

    if len(top_teacher_scores) < 20:
        teacherRange = len(top_teacher_scores)
    else:
        teacherRange = 20

    top_courses = []
    score_sorted_index = np.argsort(-np.array(top_course_scores))
    for i in range(courseRange):
        ct = CourseTeacher.objects.get(id=top_course_ids[score_sorted_index[i]])
        top_courses.append({'courseTeacherId': ct.id, 'courseName': ct.courseId.name, 'teacherId': ct.teacherId.id, 'teacherName': ct.teacherId.name, 'avgScore': '%.1f' % top_course_scores[score_sorted_index[i]]})

    top_teachers = []
    score_sorted_index = np.argsort(-np.array(top_teacher_scores))
    for i in range(teacherRange):
        teacher = Teacher.objects.get(id=top_teacher_ids[score_sorted_index[i]])
        top_teachers.append({'teacherId': teacher.id, 'teacherName': teacher.name, 'avgScore': '%.1f' % top_teacher_scores[score_sorted_index[i]]})
    return render(request, "rateMyCourse/rankPage.html", {
        'top_courses': top_courses,
        'top_teachers': top_teachers
    })