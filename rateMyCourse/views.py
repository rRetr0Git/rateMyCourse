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
from rateMyCourse.utils.send_email import send_my_email
from rateMyCourse.utils.generate_captcha import get_captcha
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import filetype

# Create your views here.

def timeit(method):
    """装饰器，记录函数运行时间

    Args:
        method: method to be timed.

    Returns:
        timed: time of running the method.
    """
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
    """访问次数统计，登录时被调用。访问次数保存在数据库中

    """
    try:
        hit = HitCount.objects.get(name='hit')
    except Exception:
        hit = HitCount(name='hit', count=0)
        hit.save()
    hit.count += 1
    hit.save()


def get_captcha_and_save_session(request):
    """获取验证码，将正确结果存入session。每次点击登录/注册时被调用

        Returns:
            sign_in_captcha_path: path of captcha when sign in.
            sign_up_captcha_path: path of captcha when sign up.
    """
    sign_in_captcha_path, sign_in_captcha_string = get_captcha()
    resetPWD_captcha_path, resetPWD_captcha_string = get_captcha()
    sign_up_captcha_path, sign_up_captcha_string = get_captcha()
    request.session['sign_in_captcha_string'] = sign_in_captcha_string
    request.session['resetPWD_captcha_string'] = resetPWD_captcha_string
    request.session['sign_up_captcha_string'] = sign_up_captcha_string
    return sign_in_captcha_path, resetPWD_captcha_path, sign_up_captcha_path


@timeit
def getIndex(request):
    """定向到主页

    """
    #addHitCount()
    return render(request, "rateMyCourse/index.html")

@timeit
def getCaptcha(request):
    """生成验证码，返回验证码路径和值。具体过程调用get_captcha_and_save_session

        Returns:
            sign_in_captcha_path: path of captcha.
            sign_up_captcha_path: correct value of captcha.
    """
    sign_in_captcha_path, resetPWD_captcha_path, sign_up_captcha_path = get_captcha_and_save_session(request)
    return HttpResponse(json.dumps({
        'sign_in_captcha_url': sign_in_captcha_path,
        'resetPWD_captcha_url': resetPWD_captcha_path,
        'sign_up_captcha_url': sign_up_captcha_path,
    }))


@timeit
def signUp(request):
    """用户注册，保证用户名和邮箱唯一后，发送注册邮件。邮件未验证时无法登陆

    Returns:
        statCode: status of current sign up.
    """
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
        captcha = request.POST['captcha']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '请填写信息',
            }))
    try:
        validate_email(mail)
    except ValidationError:
        return HttpResponse(json.dumps({
            'statCode': -6,
            'errormessage': '邮箱格式错误',
        }))
    print('input: ' + captcha)
    print('correct: ' + request.session.get('sign_up_captcha_string', 'False'))
    if captcha.lower() != request.session.get('sign_up_captcha_string', 'False').lower():
        return HttpResponse(json.dumps({
            'statCode': -5,
            'errormessage': '验证码错误',
        }))
    if request.session.get('is_login', False):
        request.session.flush()
    try:
        new_password = make_password(password)
        if len(User.objects.filter(mail=mail)) != 0:
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': '邮箱重复',
            }))
        if len(User.objects.filter(username=username)) != 0:
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': '用户名重复',
            }))
        status, email_id = send_my_email(request, mail, 'register')
        if status == -1:
            return HttpResponse(json.dumps({
                'statCode': -7,
                'errormessage': '邮件发送失败',
            }))
        User(username=username, mail=mail, password=new_password, status=1).save()# status为0表示有效用户
    except Exception as err:
        errmsg = str(err)
        print(errmsg)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': '邮箱格式错误或邮箱已存在',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': '用户名格式错误或用户名已存在',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': '出了一些bug……',
                }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))


@timeit
def simpleSearch(school, department, keywords):
    """完成数据库查找工作

    Args:
        school: school name to search.
        department: department to search.
        keywords: keywords to search.

    Return:
        courseTeacherList: courses information.
    """
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
    """根据学校、专业进行搜索。调用simpleSearch完成数据库查找工作

    Args:
        request: contains school, department and keyword.

    Returns:
        courses: courses information.
        count: count of courses.
        pages: count of pages to display courses.
    """
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
    try:
        page = int(request.GET['page'])
    except:
        return render(request, "rateMyCourse/index.html")
    print(keywords, page)
    courses = []
    pages = []
    courseTeacherList = simpleSearch(school, department, keywords)
    courses_count = len(courseTeacherList)
    if courses_count != 0 and page > ((courses_count-1)/10+1) or page < 0:
        return render(request, "rateMyCourse/index.html")
    for ctcnt in range((page - 1) * 10, page * 10):
        if(courses_count == 0 or ctcnt >= len(courseTeacherList)):
            break
        ct = courseTeacherList[ctcnt]
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
    if courses_count%10==0:
        pn = int(courses_count / 10)
    else:
        pn=int(courses_count/10)+1
    return render(request, "rateMyCourse/searchResult_new.html", {
    	'courses': courses,
    	'count': courses_count,
    	'pages': pn,
    	})


@timeit
def coursePage(request, courseTeacherId):
    """得到课程具体信息。courseTeacherId标识了一门课程和一个教师的组合

    Args:
        courseTeacherId: id to identify a course of one teacher.

    Returns:
        course_name: name of course.
        course_profession: department of course.
        course_type: type of course.
        course_scores: avg score of course.
        percent1: the first score of course.
        percent2: the second score of course.
        percent3: the third score of course.
        percent4: the fourth score of course.
        detail1: description of the first score.
        detail2: description of the second score.
        detail3: description of the third score.
        detail4: description of the fourth score.
        course_website: website of course.
        profession_website: website of teacher.
        course_teacher: name of teacher.
        teacherId: id of teacher.
        courseteacherid: id of the course-teacher pair.
        other_teacher_info: other info of teacher to recommendation.
        other_course_info: other info of course to recommendation.
    """
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
    """得到评分页信息。未登录时无法点击

    Args:
        courseTeacherId: id to identify a course of one teacher.

    Returns:
        course: information of course.
        teacher: name of teacher.
        aspect1: description of the first score.
        aspect2: description of the second score.
        aspect3: description of the third score.
        aspect4: description of the fourth score.
    """
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
    """得到教师页信息

    Args:
        teacherId: id of teacher.

    Returns:
        teacherName: name of teacher.
        teacherImg: image path of teacher.
        teacherWeb: website of teacher.
        courseList: courses info of teacher.
        teacherScore: avg score of teacher.
    """
    # addHitCount()
    teacher = Teacher.objects.get(id=teacherId)
    teacherId = teacher.id
    courseList = []
    cts = CourseTeacher.objects.filter(teacherId=teacherId)
    for ct in cts:
        course = ct.courseId
        courseList.append({'courseId': ct.id, 'courseName': course.name, 'courseScore': '%.1f' % ((ct.allHomeworkScore + ct.allKnowledgeScore + ct.allSatisfactionScore + ct.allDifficultyScore) / ct.commentCnt / 4) if ct.commentCnt!=0 else "暂无评分"})
    return render(request, "rateMyCourse/teacherPage.html",{
        'teacherName':teacher.name,
        'teacherImg':teacher.img if teacher.img != "user.png" else '/static/ratemycourse/images/upload/user/user.png',
        'teacherWeb':teacher.website,
        'courseList':courseList,
        'teacherScore': '%.1f' % ((ct.allHomeworkScore + ct.allKnowledgeScore + ct.allSatisfactionScore + ct.allDifficultyScore) / ct.commentCnt / 4) if ct.commentCnt != 0 else "暂无评分"    })

@timeit
def signIn(request):
    """用户登录，将信息写入session

    """
    try:
        username = request.POST['username']
        password = request.POST['password']
        captcha = request.POST['captcha']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '请填写信息',
            }))
    print('input: ' + captcha)
    print('correct: ' + request.session.get('sign_in_captcha_string', 'False'))
    if captcha.lower() != request.session.get('sign_in_captcha_string', 'False').lower():
        return HttpResponse(json.dumps({
            'statCode': -5,
            'errormessage': '验证码错误',
        }))
    if request.session.get('is_login', False):
        request.session.flush()
    try:
        u = User.objects.get(username=username)
    except Exception:
        try:
            u = User.objects.get(mail=username)
        except Exception:
            return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': '用户名或邮箱不存在',
            }))
    if not check_password(password, u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': '密码错误',
            }))
    elif u.status == 1:
        return HttpResponse(json.dumps({
            'statCode': -4,
            'errormessage': '账户未激活，请查收邮件',
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
    """用户注销，清除session信息

    """
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
    """主页得到学校信息

    Returns:
        school: list of school.
    """
    result = {
        'school': [s.name for s in School.objects.all()],
    }
    return HttpResponse(json.dumps(result))


@timeit
def getDepartment(request):
    """主页得到专业信息

    Returns:
        department: list of department.
    """
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
    """得到课程评论

    Returns:
         comments: info of comments.
    """
    try:
        courseTeacherId = request.GET['courseTeacherId']
        ct = CourseTeacher.objects.get(id=courseTeacherId)
        course = ct.courseId
        teacher = ct.teacherId
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '课程不存在',
            }))
    cmtList = []
    cuctList = CommentUserCourseTeacher.objects.filter(courseId=course, teacherId=teacher).order_by("-commentId__time")
    for cuct in cuctList:
        user = cuct.userId
        cmt = cuct.commentId
        cmtList.append({
            'userName': user.username if cmt.anonymous == False else '匿名用户',
            'userid': str(user.id) if cmt.anonymous == False else '',
            'text': cmt.content.replace("\n", "<br>"),
            'time': cmt.time.strftime('%y/%m/%d'),
            'avator': User.objects.get(username=user).img.url if cmt.anonymous == False else '/static/ratemycourse/images/upload/user/user.png',
            'goodTimes': cmt.like,
            'badTimes': cmt.dislike,
            'commentId': str(cmt.id)
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
    """提交评论，更新课程和教师评分

    """
    # addHitCount()
    if not request.session.get('is_login', False):
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': '请登录后再评论',
        }))
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
            'errormessage': '请填写评价信息',
        }))
    user = User.objects.get(username=username)
    ct = CourseTeacher.objects.get(id=courseTeacherId)
    course = ct.courseId
    teacher = ct.teacherId
    if(rate[0]<=0 or rate[0]>5 or rate[1]<=0 or rate[1]>5 or rate[2]<=0 or rate[2]>5 or rate[3]<=0 or rate[3]>5):
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '评分格式错误',
        }))
    postCheckStatus=0
    for i in range(len(content)):
        if content[i]=='<':
            postCheckStatus += 1
        elif content[i]=='>' and postCheckStatus>0:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'errormessage': '评论内容不合法，请勿包含\'<\'或\'>\'',
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
    """得到用户信息

    Returns:
        username: name of user.
	    isTeacher: identify if user is a teacher.
	    schoolName: school of user.
	    departmentName: department of user.
	    img: image of user.
	    commentList: comment of user.
        departments: departments list to change user department.
    """
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
	    'schoolName': user.schoolName if user.schoolName != None else '暂无',
	    'departmentName': user.departmentName if user.departmentName != None else '暂无',
	    'img': user.img.url,
	    'commentList': commentList,
        'departments': departments,
    })


@timeit
def saveUserPic(request):
    """更改用户头像

    Returns:
        the same as userInfo.
    """
    if not request.session.get('is_login', False):
        return render(request, "rateMyCourse/index.html")
    username = request.session.get('username')
    img_name = request.FILES['smfile']
    user = User.objects.get(username=username)

    kind = filetype.guess(img_name)
    if kind is None:
        print("Wrong picture type")
    elif kind.extension != "jpg" and kind.extension != "png":
        print("Wrong picture type 2")
    else:
        old_img_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') + '/rateMyCourse' + User.objects.get(username=username).img.url
        if old_img_url != os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/') + '/rateMyCourse/rateMyCourse/static/ratemycourse/images/upload/user/user.png':
            os.remove(old_img_url)

        img_name.name = str(user.id) + str(time.time()) + "." + kind.extension
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
    """更改用户信息

    Returns:
        the same as userInfo.
    """
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
    """得到排名页信息

    Returns:
        top_courses: top courses info.
        top_teachers: top teachers info.
    """
    top_courses = []
    top_course_ids = []
    top_course_avg_scores = []
    top_course_scores = []
    for ct in CourseTeacher.objects.filter(commentCnt__gt=0):
        top_course_ids.append(ct.id)
        top_course_scores.append({'s1': '%.1f' % (ct.allHomeworkScore / ct.commentCnt), 's2': '%.1f' % (ct.allDifficultyScore / ct.commentCnt), 's3': '%.1f' % (ct.allKnowledgeScore / ct.commentCnt), 's4': '%.1f' % (ct.allSatisfactionScore / ct.commentCnt), 'c': ct.commentCnt})
        top_course_avg_scores.append((ct.allHomeworkScore + ct.allDifficultyScore + ct.allKnowledgeScore + ct.allSatisfactionScore) / ct.commentCnt / 4)
    score_sorted_index = np.argsort(-np.array(top_course_avg_scores))
    if len(top_course_avg_scores) < 20:
        courseRange = len(top_course_avg_scores)
    else:
        courseRange = 20
    for i in range(courseRange):
        ct = CourseTeacher.objects.get(id=top_course_ids[score_sorted_index[i]])
        top_courses.append({'courseTeacherId': ct.id, 'courseName': ct.courseId.name, 'teacherId': ct.teacherId.id, 'teacherName': ct.teacherId.name, 'avgScore': '%.1f' % top_course_avg_scores[score_sorted_index[i]], 'score': top_course_scores[score_sorted_index[i]]})

    top_teachers = []
    top_teacher_ids = []
    top_teacher_avg_scores = []
    top_teacher_scores = []
    for teacher in Teacher.objects.filter(commentCnt__gt=0):
        top_teacher_ids.append(teacher.id)
        top_teacher_scores.append({'s1': '%.1f' % (teacher.allHomeworkScore / ct.commentCnt), 's2': '%.1f' % (teacher.allDifficultyScore / ct.commentCnt), 's3': '%.1f' % (teacher.allKnowledgeScore / ct.commentCnt), 's4': '%.1f' % (teacher.allSatisfactionScore / ct.commentCnt), 'c': teacher.commentCnt})
        top_teacher_avg_scores.append((teacher.allHomeworkScore + teacher.allDifficultyScore + teacher.allKnowledgeScore + teacher.allSatisfactionScore) / teacher.commentCnt / 4)
    score_sorted_index = np.argsort(-np.array(top_teacher_avg_scores))
    if len(top_teacher_avg_scores) < 20:
        teacherRange = len(top_teacher_avg_scores)
    else:
        teacherRange = 20
    for i in range(teacherRange):
        teacher = Teacher.objects.get(id=top_teacher_ids[score_sorted_index[i]])
        top_teachers.append({'teacherId': teacher.id, 'teacherName': teacher.name, 'avgScore': '%.1f' % top_teacher_avg_scores[score_sorted_index[i]], 'score': top_teacher_scores[score_sorted_index[i]]})

    return render(request, "rateMyCourse/rankPage.html", {
        'top_courses': top_courses,
        'top_teachers': top_teachers
    })

@timeit
def addLike(request):
    """相应点赞

    """
    commentId = request.POST['commentId']
    like = Comment.objects.get(id=commentId).like
    Comment.objects.filter(id=commentId).update(like=like + 1)
    return render(request, "rateMyCourse/coursePage_new.html", {})

@timeit
def addDislike(request):
    """相应点踩

    """
    commentId = request.POST['commentId']
    dislike = Comment.objects.get(id=commentId).dislike
    Comment.objects.filter(id=commentId).update(dislike=dislike + 1)
    return render(request, "rateMyCourse/coursePage_new.html", {})


@timeit
def active(request, active_code):
    """激活邮箱验证用户

    Args:
         active_code: code to make user active.
    """
    try:
        record = EmailVerifyRecord.objects.get(code=active_code, type='register', valid=0)
        User.objects.filter(mail=record.email).update(status=0)
        EmailVerifyRecord.objects.filter(code=active_code, type='register', valid=0).update(valid=1)
        return render(request, 'rateMyCourse/index.html', {'msg': '激活成功'})
    except:
        return render(request, 'rateMyCourse/index.html', {'msg': '激活失败'})


@timeit
def send_resetPWD_email(request):
    """发送重置密码邮件

    """
    try:
        email = request.POST['email']
        captcha = request.POST['captcha']
    except:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '请填写信息',
        }))
    try:
        validate_email(email)
    except ValidationError:
        return HttpResponse(json.dumps({
            'statCode': -6,
            'errormessage': '邮箱格式错误',
        }))
    print('input: ' + captcha)
    print('correct: ' + request.session.get('resetPWD_captcha_string', 'False'))
    if captcha.lower() != request.session.get('resetPWD_captcha_string', 'False').lower():
        return HttpResponse(json.dumps({
            'statCode': -5,
            'errormessage': '验证码错误',
        }))
    try:
        user = User.objects.get(mail=email)
        status, emailRecordId = send_my_email(request, email, 'resetPWD')
        if status == -1:
            return HttpResponse(json.dumps({
                'statCode': -1,
                'errormessage': '邮件发送失败',
            }))
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '用户不存在',
        }))


@timeit
def toResetPWD(request, reset_code):
    """点击重置密码邮件，跳转到重置页面，10分钟内有效

    """
    try:
        record = EmailVerifyRecord.objects.get(code=reset_code, type='resetPWD', valid=0)
        prevtime = record.time
        if (timezone.now() - prevtime).seconds > 600:
            return render(request, "rateMyCourse/index.html", {'msg': '重置密码失败，重置链接已过期。'})
        else:
            return render(request, "rateMyCourse/resetPassword.html")
    except:
        return render(request, "rateMyCourse/index.html", {'msg': '重置密码失败。'})

@timeit
def resetPWD(request):
    """重置密码

    Args:
        reset_code：code to reset password
    """
    try:
        password = request.POST['password']
        reset_code = request.POST['reset_code']
        record = EmailVerifyRecord.objects.get(code=reset_code, type='resetPWD', valid=0)
        record.valid=1
        record.save()
        email = EmailVerifyRecord.objects.get(code=reset_code, type='resetPWD').email
        User.objects.filter(mail=email).update(password=make_password(password), status=0)
        return HttpResponse(json.dumps({
            'statCode': 0,
        }))
    except:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '重置密码失败',
        }))