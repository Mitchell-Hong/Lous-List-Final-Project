from django.urls import path

from . import views

# will all be routes appended onto the back of url/main
app_name = 'main'
urlpatterns = [
    # the path for the /main/ route
    path('', views.index, name='index'),
]
