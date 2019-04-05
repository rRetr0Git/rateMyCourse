from django.shortcuts import render, get_list_or_404
from rateMyCourse.models import *
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
    keys['course_name'] = keywords
    s = ' '.join([
        '+' + key + ':\"' + keys[key] + '\"' for key in keys
    ])
    t = request.urlopen(url%parse.quote(s)).read().decode('utf-8')
    t = json.loads(t)
    return [i['course_number'] for i in t['response']['docs']]

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
    courselist = solrSearch(keywords, school, department)
    courses = []
    pages = []
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

    pn=int(len(courses)/10)+1
    for i in range(pn):
        pages.append({'number': i+1})
    return render(request, "rateMyCourse/searchResult.html", {
    	'courses': courses,
    	'count': len(courses),
    	'pages': pages,
    	})

def getAvgScore(courses):
    x = [0] * 4
    count = 0
    for c in courses:
        for rate in c.rate_set.all():
            x[0] += rate.A_score
            x[1] += rate.B_score
            x[2] += rate.C_score
            x[3] += rate.D_score
            count += 1
    if(count > 0):
        for i in range(4):
            x[i] /= count
    return x

def coursePage(request, course_number):
    addHitCount()
    courses = get_list_or_404(Course, number=course_number)
    # courses = Course.objects.filter(number=course_number)
    x = getAvgScore(courses)
    return render(request, "rateMyCourse/coursePage.html", {
        'course_name': courses[0].name,
        'course_credit': courses[0].credit,
        'course_profession': courses[0].department.name,
        'course_type': courses[0].coursetype,
        'course_scores': '%.1f'%(sum(x) / 4),
        'detail1': '有趣程度：%.1f'%(x[0]),
        'detail2': '充实程度：%.1f'%(x[1]),
        'detail3': '课程难度：%.1f'%(x[2]),
        'detail4': '课程收获：%.1f'%(x[3]),
        'course_website': courses[0].website if courses[0].website != '' else '.',
        'profession_website': courses[0].department.website if courses[0].department.website != '' else '.',
        })

def ratePage(request, course_number):
    addHitCount()
    cs = get_list_or_404(Course, number=course_number)
    return render(request, "rateMyCourse/ratePage.html", {
            'course': {
                'name': cs[0].name,
                'school': cs[0].department.school.name,
                'department': cs[0].department.name,
            },
            'aspect1': '有趣程度',
            'aspect2': '充实程度',
            'aspect3': '课程难度',
            'aspect4': '课程收获',
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
        print("world")
        school = School.objects.get(name=request.GET['school'])
        department = school.department_set.get(name=request.GET['department'])
        course = Course.objects.filter(school=school, department=department).distinct()
        print(course)
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school or department not found'
            }))
    return HttpResponse(json.dumps({
        'course': [c.name for c in course]
        }))

def getComment(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    cmtList = []
    for c in courses:
        for cmt in c.comment_set.all():
            cmtList.append({
                'userName': cmt.user.username if cmt.anonymous == False else '匿名用户',
                'text': cmt.content.replace("\n", "<br/>"),
                'time': cmt.time.strftime('%y/%m/%d'),
                'iTerm': cmt.term,
                'iTeacher': ','.join([t.name for t in cmt.course.teacher_set.all()]),
                'iTotal': cmt.total_score,
                })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))

def getTeachers(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    tList = []
    for c in courses:
        tList.append([
            t.name for t in c.teacher_set.all()
            ])
    return HttpResponse(json.dumps({
        'statCode': 0,
        'teachers': tList,
        }))

def getOverAllRate(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    return HttpResponse(json.dumps({
        'statCode': 0,
        'rate': getAvgScore(courses),
        }))


def submitComment(request):
    addHitCount()
    try:
        username = request.POST['username']
        comment = request.POST['comment']
        rate = request.POST.getlist('rate')
        for i, j in enumerate(rate):
            rate[i] = int(j)
        course_number = request.POST['course_number']
        anonymous = request.POST['anonymous']
        term = request.POST['term']
        teacher = request.POST.getlist('teacher')
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))
    cset = Course.objects.filter(number=course_number)
    # print(rate, teacher)
    for t in teacher:
        cset = cset.filter(teacher_set__name=t)
    # print(cset)
    # assert(len(cset) == 1)
    crs = cset[0]
    # print(anonymous)
    Comment(
        anonymous=True if anonymous == 'true' else False,
        content=comment,
        time=timezone.now(),
        user=User.objects.get(username=username),
        course=crs,
        term=term,
        total_score = sum(rate) / len(rate),
        ).save()
    Rate(
        user=User.objects.get(username=username),
        course=crs,
        A_score=rate[0],
        B_score=rate[1],
        C_score=rate[2],
        D_score=rate[3],
        ).save()
    return HttpResponse(json.dumps({
        'statCode': 0,
        }))
