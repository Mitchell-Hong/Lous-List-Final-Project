from django.db import models

# Create your models here.
# https://docs.djangoproject.com/en/4.1/ref/models/fields/
# refrence for different types of fields django

class myUser(models.Model):
    # we are going to ID users by this id as primary key
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    summary = models.TextField(max_length=500)
    major = models.CharField(max_length=20)
    graduationYear = models.IntegerField()

    def __str__(self):
        return self.name