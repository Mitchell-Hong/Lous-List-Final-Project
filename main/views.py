from django.shortcuts import render, get_object_or_404

# Create your views here.
# simple display of what is shown at /main/ route
def index(request):
    return(render, 'main/index.html')