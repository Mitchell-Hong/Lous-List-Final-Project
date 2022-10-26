from django.forms import ModelForm
from django import forms
from .models import myUser, department

class UserForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['email', 'major', 'graduationYear', 'summary']

class searchclassForm(forms.Form):
    department_choices = department.objects.all()
    into_text = []
    for deps in department_choices:
        into_text.append((deps.abbreviation, deps.abbreviation))
    department = forms.CharField(label = "Select the department", widget=forms.Select(choices = into_text))
    fields = ['department']
    #class Meta:
