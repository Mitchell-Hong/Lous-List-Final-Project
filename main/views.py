from tracemalloc import start
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.views import generic
from django.urls import reverse
from .forms import UserForm
from .models import Friend_Request, FriendList, myUser, department, course
# this is used for making HTTP requests from an external API with django
import requests

# allows for HTTP requests from the API

# Create your views here.
# simple display of what is shown at /main/ route
def index(request):
    context = {
        'theUser':request.user.id
    }
    return render(request, 'main/index.html', context)

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
    departments = department.objects.all() # data is a list of departments {"subject": abbrev}
    noDep = True
    Instructors = []
    classTypes = []
    input = request.GET.get('depSelect', None)
    filteredInstructor = request.GET.get('instructor', None)
    filteredClassType = request.GET.get('classType', None)
    filteredCredits = request.GET.get('credits', None)
    if input:
        noDep = False
        url = 'http://luthers-list.herokuapp.com/api/dept/' + input + '/'
        response = requests.get(url)
        courses = response.json()
        coursesNoDup = { each['catalog_number'] : each for each in courses }.values()
        for i in coursesNoDup:
            Instructors.append(i['instructor']['name'])
    context = {
        'department_results' : departments,
        'instructors': Instructors,
        'noDepartment': noDep,
        # tab tells the HTML what the depict as the active tab
        'tab' : 'coursecatalog',
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





## ALL RELATED TO THE FRIENDS SYSTEM (PROFILE, EDITING, SEEING FRIENDS ETC)



# profile view which allows the user to see their profile info they entered at login as well as edit it
# only time they can hit this link is when they have already logged in WILL HAVE AN ID
def profile(request, user_id):
    # profile of the individual the user is looking at
    theUser = myUser.objects.get(id=user_id)
    
    # boolean value that determines whether or not the users are friends by default is False
    isFriend = False
    # get a list of all the friends of the user currently using the website
    has_friend = FriendList.objects.filter(user=request.user.id).first()
    allFriends = []
    if has_friend:
        allFriends = has_friend.friends.all()   
        if theUser in allFriends:
            isFriend = True

    # only able to send a Friend Request to people who you are not already friends with therefore
    # a friendRequest can either be already sent and you will get a message telling you that
    # or it will be created and sent for the first time and the message will alert you of that
    messageSent = ''
    if request.method == 'POST':
        from_user = myUser.objects.get(id=request.user.id)
        to_user = theUser
        friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)

        # if the friend request was created for the first time alerts the user that it was sent
        if created:
            messageSent = 'Friend Request was sent!'
        else:
            messageSent = 'Friend Request has already been sent!'

    # theUser passes along ifno about the user profile we are looking at, message sent is just
    # alerting the user to assure them their request was sent
    # isFriend is a boolean value (can only see a user's email and schedule if you are friends with
    # them and you cannot send someone a FriendRequest if you are already friend with them)
    context = {
        'theUser' : theUser,
        'messageSent' : messageSent,
        'isFriend': isFriend,
    }
    return render(request, 'main/profile.html', context)


# allows the user to edit his profile (the button to get here can only be viewed on the HTML
# profile where the user is looking at his own profile)
def edit(request):
    activeUser = myUser.objects.get(id=request.user.id)
    form = UserForm(instance=activeUser)
    context={'form':form}
    if request.POST:
        # form but we have some of the info filled out
        form = UserForm(request.POST, instance=activeUser)
        if form.is_valid():
            form.save()
            # reverse looks through all URLs defined in project and returns the one specified
            # this is what we want so we have no hardcoded URLS
            return HttpResponseRedirect(reverse('main:coursecatalog'))
    return render(request, 'main/editprofileloggedin.html', context)


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



################   FRIENDS VIEWS AND LOGIC     ################################


# this displays all of the active friend requests and allows users to accept or delete them
def friendrequests(request):
    friend_requests = Friend_Request.objects.filter(to_user_id=request.user.id)
    context = {
        'friend_requests': friend_requests
    }
    return render(request, 'main/friendrequests.html', context)

# this is the link that is hit if the user decides to delete the friend request
def deleterequest(request, fromUserID):
    # activeUser is the person who is checking their friend requests
    activeUser = myUser.objects.get(id=request.user.id)
    # from user is the person who sent the friend request
    fromUser = myUser.objects.get(id=fromUserID)
    # go and get the specific friend request since we know it exists and then delete it
    friendRequest = Friend_Request.objects.get(from_user=fromUser, to_user=activeUser)
    friendRequest.delete()
    # return to the same page where hopefully that friend request has been deleted
    return HttpResponseRedirect(reverse('main:friendrequests'))


def acceptrequest(request, fromUserID):
    # activeUser is the person who is checking their friend requests
    activeUser = myUser.objects.get(id=request.user.id)
    # from user is the person who sent the friend request
    fromUser = myUser.objects.get(id=fromUserID)
    # go and get the specific friend request since we know it exists and then delete it
    friendRequest = Friend_Request.objects.get(from_user=fromUser, to_user=activeUser)

    # see whether or not each user has an exisiting friends list or if one needs to be made
    friendListActiveUser, createdActive = FriendList.objects.get_or_create(user=activeUser)
    friendListFromUser, createdFrom = FriendList.objects.get_or_create(user=fromUser)

    # add the fromUser to the activeUsers friends list AND VICE VERSA
    friendListActiveUser.friends.add(fromUser)
    friendListFromUser.friends.add(activeUser)
    # increment the number of friends each user has
    fromUser.numFriends = fromUser.numFriends + 1
    activeUser.numFriends = activeUser.numFriends + 1
    fromUser.save()
    activeUser.save()

    # delete the friend request since it has been processed
    friendRequest.delete()
    return HttpResponseRedirect(reverse('main:friendrequests'))


def friends(request, user_id):

    theUser = myUser.objects.get(id=user_id)
    # we are basically checking whether or not the user has friends since you cannot call .all()
    # on a "None". Essentially trying to find all on a null object does not work
    has_friend = FriendList.objects.filter(user=theUser).first()
    allFriends = []
    if has_friend:
        allFriends = has_friend.friends.all()
    # passing all the friends that a user has into context so they can go to the front end
    context = {
        'allFriends': allFriends,
    }

    return render(request, 'main/friends.html', context)


# allows the user to search for other users on the app by name (corresponds to addfriend/ path)
def addfriend(request):
    # do not allow users to find ppl they are already friends with on this page
    has_friend = FriendList.objects.filter(user=request.user.id).first()
    allFriends = []
    if has_friend:
        allFriends = has_friend.friends.all()

    # list of all the Users on the site so far (only show the top ten results on front end)
    # exlcudes the user himself as well as all people he is already friends with
    shownUsers = myUser.objects.all().exclude(id=request.user.id).exclude(id__in=allFriends)
    # the user input provided to search for their friends
    input = request.GET.get('friendsearch', None)
    if input:
        # filter on a specific item inside the model then __ some form of filtering in python
        shownUsers = myUser.objects.filter(name__icontains=input).exclude(id=request.user.id)
    context = {
        'shownUsers' : shownUsers,
    }
    return render(request, 'main/addfriend.html', context)







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