from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

# will all be routes appended onto the back of url/main
app_name = 'main'
urlpatterns = [
    # the path for the /main/ route
    path('', views.index, name='index'),
    path('editprofile/', views.editprofile, name='editprofile'),
    

    # these paths are used to get the data from the API
    path('coursecatalog/', views.coursecatalog, name='coursecatalog'),

]

urlpatterns += staticfiles_urlpatterns()
