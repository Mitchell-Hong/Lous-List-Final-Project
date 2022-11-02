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
    # dummy link for when it comes time do the class search page
    path('searchclass/', views.searchclass, name='searchclass'),
    # dummy link but will display individual users schedules for the courses they have selected so far
    path('myschedule/', views.myschedule, name='myschedule'),
    # shows users what are all the courses they have added to their shopping cart they can then choose from those to move to their schedule
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    # profile route that will show the user theirs and other profiles (they can edit theirs)
    path('profile/<int:user_id>/', views.profile, name='profile'),
    # profile that takes the user to a separate form once logged in to edit or update their profile
    path('profile/edit/', views.edit, name='edit'),
    # route that allows users to see how many friends they have as well as add new ones
    path('friends/', views.friends, name='friends'),
    # page that allows users to accept or reject friend requests
    path('friendrequests/', views.friendrequests, name='friendrequests')

]

urlpatterns += staticfiles_urlpatterns()
