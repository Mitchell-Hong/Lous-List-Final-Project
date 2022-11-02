from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

# will all be routes appended onto the back of url/main
app_name = 'main'
urlpatterns = [
    # the path for the /main/ route
    path('', views.index, name='index'),
    # the route users see when they first sign in for additional info
    path('editprofile/', views.editprofile, name='editprofile'),
    # a list of all the departments that UVA has to offer
    path('coursecatalog/', views.coursecatalog, name='coursecatalog'),
    # based on which department the user clicks on it displays that departments courses
    path('coursecatalog/<str:dept>', views.deptclasses, name='deptclasses'),
    # First step in class search -- will query for department
    path('searchclass/', views.searchclassDepartment, name='searchclass'),
    # Second step in class search -- will query for specific credits, instructors, etc.
    path('searchclass/<str:filteredDepartment>', views.searchclassFilter, name='filterclasses'),
    # dummy link but will display individual users schedules for the courses they have selected so far
    path('myschedule/', views.myschedule, name='myschedule'),
    # shows users what are all the courses they have added to their shopping cart they can then choose from those to move to their schedule
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    # profile route that will show the user theirs and other profiles (they can edit theirs)
    path('profile/<int:user_id>/', views.profile, name='profile'),
    # profile that takes the user to a separate form once logged in to edit or update their profile
    path('profile/edit/', views.edit, name='edit'),
    
    
    # route that allows users to see how many friends they have as well as add new ones
    path('friendsearch/', views.friendsearch, name='friendsearch'),
    # page that allows users to accept or reject friend requests
    path('friendrequests/', views.friendrequests, name='friendrequests'),
    # page that allows users to see a list of users who they are friends with
    path('friends/<int:user_id>/', views.friends, name='friends'),

    # path that triggers a view which deletes the friend request if the user declines it
    path('friendrequests/delete/<int:fromUserID>/', views.deleterequest, name='deleterequest'),
    # path for if the user accepts the incoming friend request
    path('friendrequests/accept/<int:fromUserID>/', views.acceptrequest, name='acceptrequest'),



]

urlpatterns += staticfiles_urlpatterns()
