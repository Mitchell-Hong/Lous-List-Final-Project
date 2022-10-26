from tracemalloc import start
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
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
    if(request.user.is_authenticated):
        try:
            newUser = myUser.objects.get(id=request.user.id)
            return HttpResponseRedirect(reverse('main:index'))
        # if the user has not logged in yet then create a new user
        except:
            # users have id, name, email, summary, major, graduationYear
                newUser = myUser(id=request.user.id, name=str(request.user.first_name + " " + request.user.last_name), summary='', major='', graduationYear='')
                # beauty of this is our users will have the same ID as the socialaccount -> request.user
                form = UserForm()
                context = {
                    'form': form,
                }
                if request.POST:
                    # form but we have some of the info filled out
                    form = UserForm(request.POST, instance=newUser)
                    if form.is_valid():
                        form.save()
                        # reverse looks through all URLs defined in project and returns the one specified
                        # this is what we want so we have no hardcoded URLS
                        return HttpResponseRedirect(reverse('main:coursecatalog'))
                return render(request, 'main/editprofile.html', context)
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
        

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
    url = 'http://luthers-list.herokuapp.com/api/dept/' + dept + '/'
    response = requests.get(url)
    courses = response.json()
    coursesNoDup = { each['catalog_number'] : each for each in courses }.values()

    context = {
        'course_list': courses,
        'course_list_nodup':coursesNoDup,
    }
    return render(request, 'main/classesList.html', context)

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

# profile view which allows the user to see their profile info they entered at login as well as edit it
# only time they can hit this link is when they have already logged in WILL HAVE AN ID
def profile(request):    
    theUser = myUser.objects.get(id=request.user.id)
    context = {
        'theUser' : theUser,
    }
    return render(request, 'main/profile.html', context)




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