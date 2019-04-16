from django.shortcuts import render, get_list_or_404
from rateMyCourse.models import *
from django.db.models import Q
import json
from urllib import request, parse
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.


def addHitCount():
	try:
		hit = HitCount.objects.get(name='hit')
	except Exception:
		hit = HitCount(name='hit', count=0)
		hit.save()
	hit.count += 1
	hit.save()


def getIndex(request):
    #addHitCount()
    return render(request, "rateMyCourse/index.html")

def signUp(request):
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
        User(username=username, mail=mail, password=password).save()
    except Exception as err:
        errmsg = str(err)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': 'mail repeated',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': 'username repeated',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': 'other error, maybe out of length',
                }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

    '''
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)
    '''

def solrSearch(keywords, school, department):
    url = "http://10.2.28.123:8080/solr/collection1/select?q=%s&rows=100&sort=rate_count+desc&wt=json&indent=true"
    keys = dict()

    ######
    # this is a fool idea to fix bug that if nothing to write in nothing you can search
    if(school == None and keywords == ''):
    	school = "北京航空航天大学"
    ######

    if(school != None):
        keys['school_name'] = school
    if(department != None):
        keys['department_name'] = department
    keys['courseId'] = keywords
    s = ' '.join([
        '+' + key + ':\"' + keys[key] + '\"' for key in keys
    ])
    t = request.urlopen(url%parse.quote(s)).read().decode('utf-8')
    t = json.loads(t)
    return [i['courseId'] for i in t['response']['docs']]


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

def search(request):
    addHitCount()
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
    '''
        for i, c_number in enumerate(courselist):
        if(c_number in courselist[:i]):
            continue
        cs = Course.objects.filter(number=c_number)
        x = getAvgScore(cs)
        courses.append({
            'name': cs[0].name,
            'ID': cs[0].number,
            'type': cs[0].coursetype,
            'credit': cs[0].credit,
            'school': cs[0].department.school.name,
            'department': cs[0].department.name,
            'rateScore': sum(x) / len(x),
            'ratenumber': sum([i.comment_set.count() for i in cs])
            })
    '''

    courseTeacherList = simpleSearch(school,department,keywords)
    for index,courseTeacher in enumerate(courseTeacherList):
        course = Course.objects.get(id=courseTeacher.courseId.id)
        teacher = Teacher.objects.get(id=courseTeacher.teacherId.id)
        comments = [cuct.commentId for cuct in
                    CommentUserCourseTeacher.objects.filter(courseId=course.id, teacherId=teacher.id)]
        homework, difficulty, knowledge, satisfaction, count, avg_score = getAvgScore(comments)
        courses.append({
            'name': course.name,
            'ID': course.id,
            'courseTeacher' : courseTeacher.id,
            'teacher': teacher.name,
            'type': course.type,
            'credit': 5,
            'school': school,
            'department': course.department,
            'rateScore': '%.1f'% avg_score,
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

def getAvgScore(comments):
    count = 0
    homework = 0
    difficulty = 0
    knowledge = 0
    satisfaction = 0
    for cmt in comments:
        homework += cmt.homework
        difficulty += cmt.difficulty
        knowledge += cmt.knowledge
        satisfaction += cmt.satisfaction
        count += 1
    if(count > 0):
        return homework / count, difficulty / count, knowledge / count, satisfaction / count, count, (homework + difficulty + knowledge + satisfaction) / (count * 4.0)
    return 3.0, 3.0, 3.0, 3.0, count, 3.0

def coursePage(request, courseTeacherId):
    addHitCount()
    courseTeacher = CourseTeacher.objects.get(id=courseTeacherId)
    course = Course.objects.get(id=courseTeacher.courseId.id)
    teacher = Teacher.objects.get(id=courseTeacher.teacherId.id)
    comments = [cuct.commentId for cuct in CommentUserCourseTeacher.objects.filter(courseId=course.id, teacherId=teacher.id)]
    homework, difficulty, knowledge, satisfaction, count, avg_score = getAvgScore(comments)
    other_teacher_info = []
    other_cts = CourseTeacher.objects.filter(courseId=course.id).filter(~Q(teacherId=teacher.id))
    for other_ct in other_cts:
        other_teacher = other_ct.teacherId
        comments = [cuct.commentId for cuct in CommentUserCourseTeacher.objects.filter(courseId=course.id, teacherId=other_teacher.id)]
        other_homework, other_difficulty, other_knowledge, other_satisfaction, other_count, other_avg_score = getAvgScore(comments)
        other_teacher_info.append({"id":other_ct.id, "name":other_teacher.name, "score":'%.1f'%other_avg_score})
    other_course_info = []
    other_cts = CourseTeacher.objects.filter(teacherId=teacher.id).filter(~Q(courseId=course.id))
    for other_ct in other_cts:
        other_course = other_ct.courseId
        comments = [cuct.commentId for cuct in CommentUserCourseTeacher.objects.filter(courseId=other_course.id, teacherId=teacher.id)]
        other_homework, other_difficulty, other_knowledge, other_satisfaction, other_count, other_avg_score = getAvgScore(comments)
        other_course_info.append({"id":other_ct.id, "name":other_course.name, "score":'%.1f'%other_avg_score})
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
        'courseteacherid': courseTeacher.id,
        'other_teacher_info': other_teacher_info,
        'other_course_info': other_course_info
        })

def ratePage(request, courseTeacherId):
    addHitCount()
    courseTeacher = CourseTeacher.objects.get(id=courseTeacherId)
    course = Course.objects.get(id=courseTeacher.courseId.id)
    teacher = Teacher.objects.get(id=courseTeacher.teacherId.id)
    return render(request, "rateMyCourse/ratePage_new.html", {
            'course': {
                'name': course.name,
                'description': course.description,
                'department': course.department,
            },
            'teacher': teacher.name,
            'aspect1': '作业量',
            'aspect2': '难度',
            'aspect3': '知识量',
            'aspect4': '满意度',
        })

def signIn(request):
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
    if(password != u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'wrong password',
            }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': u.username,
            }))

def getSchool(request):
    result = {
        'school': [s.name for s in School.objects.all()],
    }
    return HttpResponse(json.dumps(result))

def getDepartment(request):
    try:
        school = School.objects.get(name=request.GET['school'])
        department = [c.courseId.department for c in SchoolCourse.objects.filter(schoolId=school.id).distinct()]
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school not found'
            }))
    return HttpResponse(json.dumps({
        'department': list(set([d for d in department]))
        }))

def getCourse(request):
    try:
        school = School.objects.get(name=request.GET['school'])
        department = school.department_set.get(name=request.GET['department'])
        course = Course.objects.filter(school=school, department=department).distinct()
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school or department not found'
            }))
    return HttpResponse(json.dumps({
        'course': [c.name for c in course]
        }))

def getComment(request):
    try:
        courseTeacherId = request.GET['courseTeacherId']
        course = CourseTeacher.objects.get(id=courseTeacherId).courseId
        teacher = CourseTeacher.objects.get(id=courseTeacherId).teacherId
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
            'text': cmt.content.replace("\n", "<br/>"),
            'time': cmt.time.strftime('%y/%m/%d'),
            })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))

def getTeachers(request):
    try:
        teachers = CourseTeacher.objects.filter(courseId=request.GET['courseId'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get courseId or courseId not exists',
            }))
    tList = []
    for t in teachers:
        tList.append(t.teacherId.name)
    return HttpResponse(json.dumps({
        'statCode': 0,
        'teachers': tList,
        }))

def getOverAllRate(request):
    try:
        courses = Course.objects.filter(number=request.GET['courseId'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get courseId or courseId not exists',
            }))
    return HttpResponse(json.dumps({
        'statCode': 0,
        'rate': getAvgScore(courses),
        }))


def submitComment(request):
    addHitCount()
    try:
        username = request.POST['username']
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
    course = CourseTeacher.objects.get(id=courseTeacherId).courseId
    teacher = CourseTeacher.objects.get(id=courseTeacherId).teacherId
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
    return HttpResponse(json.dumps({
        'statCode': 0,
    }))

def userInfo(request):
    name = request.GET['name']
    user = User.objects.get(username = name)
    commentList=[]
    cuctList = CommentUserCourseTeacher.objects.filter(userId=user.id)
    for cuct in cuctList:
        teacher = cuct.teacherId
        course = cuct.courseId
        courseTeacher = CourseTeacher.objects.get(teacherId=teacher,courseId=course).id
        cmt = cuct.commentId
        if cmt.anonymous == True:
            continue
        commentList.append({
            'course': course.name,
            'courseTeacher': courseTeacher,
            'teacher': teacher.name,
            'rate': [cmt.homework,cmt.difficulty,cmt.knowledge,cmt.satisfaction],
            'time': cmt.time.strftime('%y/%m/%d'),
            })

    return render(request, "rateMyCourse/userInfo.html",{
	    'username':name,
	    'isTeacher':user.isTeacher,
	    'schoolName':user.schoolName,
	    'departmentName':user.departmentName,
	    'img':user.img,
	    'commentList':commentList,
    })

def saveUserInfo(request):
    school = request.POST['school']
    department = request.POST['department']
    username = request.POST['username']
    user = User.objects.filter(username=username)
    user.update(schoolName=school,departmentName=department)
    user = user[0]
    commentList = []
    return render(request, "rateMyCourse/userInfo.html", {
        'username': username,
        'isTeacher': user.isTeacher,
        'schoolName': user.schoolName,
        'departmentName': user.departmentName,
        'img': user.img,
        'commentList': commentList,
    })

def getRank(request):
    return render(request,"rateMyCourse/rankPage.html")