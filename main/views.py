from tracemalloc import start
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse
from .forms import UserForm
from .models import myUser, department, course
# this is used for making HTTP requests from an external API with django
import requests

# allows for HTTP requests from the API

# Create your views here.
# simple display of what is shown at /main/ route
def index(request):
    return render(request, 'main/index.html')

def editprofile(request):
    '''
    CODE TO LOAD IN DEPARTMENT DATA
    '''
    # fetching the data and storing it once in DB for users when they are filling out intro form
    # url = 'http://luthers-list.herokuapp.com/api/deptlist/'
    # response = requests.get(url)
    # data = response.json()
    # for i in data:
    #     try:
    #         deps = department.objects.get(abbreviation=i['subject'])
    #     except:
    #         deps = department(abbreviation = i['subject'])
    #         deps.save()

    # request.user.id gives and id to each user, request.user will be the name of the user
    # https://docs.djangoproject.com/en/4.1/ref/contrib/auth/ info about user fields

    # try and get the model from the database if it exists then this user has signed in before
    # do not make him fill out the form again just redirect to main
    try:
        newUser = myUser.objects.get(id=request.user.id)
        return HttpResponseRedirect(reverse('main:index'))
    # if the user has not logged in yet then create a new user
    except:
        # users have id, name, email, summary, major, graduationYear
        newUser = myUser(id=request.user.id, name=str(request.user), summary='', major='', graduationYear='')
        # beauty of this is our users will have the same ID as the socialaccount -> request.user
        form = UserForm()
        context = {'form':form}
        if request.POST:
            # form but we have some of the info filled out
            form = UserForm(request.POST, instance=newUser)
            if form.is_valid():
                form.save()
                # reverse looks through all URLs defined in project and returns the one specified
                # this is what we want so we have no hardcoded URLS
                return HttpResponseRedirect(reverse('main:coursecatalog'))
        return render(request, 'main/editprofile.html', context)

# view for the course catalog tab has a list of departments that user can click on to choose
def coursecatalog(request):
    departments = department.objects.all() # data is a list of departments {"subject": abbrev}
    context = {
        'department_results' : departments,
        # tab tells the HTML what the depict as the active tab
        'tab' : 'coursecatalog',
    }
    return render(request,'main/coursecatalog.html', context)

# dynamic routing based on which department the user clicked a list of all classes that belong to that department appear
def deptclasses(request, dept):
    courses = course.objects.filter(department = department.objects.get(abbreviation = dept))
    context = {
        'course_list' : courses,
        'tab' : 'course_list'
    }
    return render(request, 'main/classesList.html', context)
    '''
    CODE TO LOAD IN COURSE DATA FOR EACH DEPARTMENT
    LEAVE COMMENTED OUT MAY USE IN THE FUTURE BUT HEROKU CANNOT SUPPORT THIS MUCH DATA (9000 CLASSES)
    may not have this Heroku
    '''
    # departments = department.objects.all()
    # for deps in departments:
    #     dept = deps.abbreviation
    #     url = 'http://luthers-list.herokuapp.com/api/dept/' + dept + '/'
    #     response = requests.get(url)
    #     data = response.json()
    #     for entry in data:
    #         try :
                # Checks to see if the entry is already found in the database --- a valid meetings entry
    #             if (len(entry['meetings']) > 0):
    #                 courses = course.objects.get(department = department.objects.get(abbreviation = dept), courseNumber = entry['course_number'], description = entry['description'],
    #                 instructorName = entry['instructor']['name'], instructorEmail = entry['instructor']['email'], semesterCode = entry['semester_code'],
    #                 courseSection = entry['course_section'], credits = entry['units'], lectureType = entry['component'],
    #                 classCapacity = entry['class_capacity'], classEnrollment = entry['enrollment_total'],
    #                 classSpotsOpen = entry['enrollment_available'], waitlist = entry['wait_list'], waitlistMax = entry['wait_cap'],
    #                 meeting_days = entry['meetings'][0]['days'], start_time = entry['meetings'][0]['start_time'],
    #                 end_time = entry['meetings'][0]['end_time'], room_location = entry['meetings'][0]['facility_description'])
    #             else :
                    # Checks to see if the entry is already found in the database --- a non valid meetings entry
    #                 courses = course.objects.get(department = department.objects.get(abbreviation = dept), courseNumber = entry['course_number'], description = entry['description'],
    #                 instructorName = entry['instructor']['name'], instructorEmail = entry['instructor']['email'], semesterCode = entry['semester_code'],
    #                 courseSection = entry['course_section'], credits = entry['units'], lectureType = entry['component'],
    #                 classCapacity = entry['class_capacity'], classEnrollment = entry['enrollment_total'],
    #                 classSpotsOpen = entry['enrollment_available'], waitlist = entry['wait_list'], waitlistMax = entry['wait_cap'],
    #                 meeting_days = "", start_time = "",
    #                 end_time = "", room_location = "")
    #         except :
                # Code that inserts a new course into the database. This checks to see if the meetings has a valid entry
    #             if (len(entry['meetings']) > 0):
    #                 courses = course(department = department.objects.get(abbreviation = dept), courseNumber = entry['course_number'], description = entry['description'],
    #                 instructorName = entry['instructor']['name'], instructorEmail = entry['instructor']['email'], semesterCode = entry['semester_code'],
    #                 courseSection = entry['course_section'], credits = entry['units'], lectureType = entry['component'],
    #                 classCapacity = entry['class_capacity'], classEnrollment = entry['enrollment_total'],
    #                 classSpotsOpen = entry['enrollment_available'], waitlist = entry['wait_list'], waitlistMax = entry['wait_cap'],
    #                 meeting_days = entry['meetings'][0]['days'], start_time = entry['meetings'][0]['start_time'],
    #                 end_time = entry['meetings'][0]['end_time'], room_location = entry['meetings'][0]['facility_description'])
    #                 courses.save()
    #             else :
                # Code that inserts a new course into the database. This checks to see if the meetings does not have a valid entry
    #                 courses = course(department = department.objects.get(abbreviation = dept), courseNumber = entry['course_number'], description = entry['description'],
    #                 instructorName = entry['instructor']['name'], instructorEmail = entry['instructor']['email'], semesterCode = entry['semester_code'],
    #                 courseSection = entry['course_section'], credits = entry['units'], lectureType = entry['component'],
    #                 classCapacity = entry['class_capacity'], classEnrollment = entry['enrollment_total'],
    #                 classSpotsOpen = entry['enrollment_available'], waitlist = entry['wait_list'], waitlistMax = entry['wait_cap'],
    #                 meeting_days = "", start_time = "",
    #                 end_time = "", room_location = "")
    #                 courses.save()
    # return HttpResponse(data)

# class search dummy implementation for now
def searchclass(request):
    context = {
        'tab' : 'searchclass',
    }
    return render(request,'main/searchclass.html', context)

# myschedule dummy implementation for now
def myschedule(request):
    context = {
        'tab' : 'myschedule',
    }
    return render(request,'main/myschedule.html', context)

# shopping cart dummy implementation for now
def shoppingcart(request):
    context = {
        'tab' : 'shoppingcart',
    }
    return render(request,'main/shoppingcart.html', context)