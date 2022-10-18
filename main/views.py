from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse
from .forms import UserForm
from .models import myUser
import requests

# allows for HTTP requests from the API

# Create your views here.
# simple display of what is shown at /main/ route
def index(request):
    return render(request, 'main/index.html')

def editprofile(request):
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
                return HttpResponseRedirect(reverse('main:index'))     
        return render(request, 'main/editprofile.html', context)


def coursecatalog(request):
    url = 'http://luthers-list.herokuapp.com/api/deptlist/'
    response = requests.get(url)
    data = response.json()      # data is a list of departments {"subject": abbrev}
    departments = []
    for i in data:
        tempDepartment = i["subject"]
        departments.append(tempDepartment)
        
    return HttpResponse(departments)