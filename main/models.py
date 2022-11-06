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

    # followed friends tutorial at https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
    numFriends = models.SmallIntegerField(default=0)
    # schedule fields so that we can build a schedule for each user
    schedule = models.TextField(max_length=500, default="")
    # shoppingcart = models.TextField(max_length=500, default="")

    def __str__(self):
        return self.name

class FriendList(models.Model):
    user = models.OneToOneField(myUser, related_name='user', on_delete=models.CASCADE)
    friends = models.ManyToManyField(myUser, default='', blank=True, related_name='friends')

class Friend_Request(models.Model):
    # foreign key allows tables to be easily linked together
    # the related name field basically allows us to specify the instance of each of the models
    # django will do this by default if we do not, but in this case it is useful for us to do
    from_user = models.ForeignKey(myUser, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(myUser, related_name='to_user', on_delete=models.CASCADE)


class department(models.Model):
    abbreviation = models.CharField(max_length=10)
    departmentName = models.CharField(max_length=30)

    def __str__(self):
        return self.abbreviation


class course(models.Model):
    # course info CS 1110 Intro to Python
    department = models.ForeignKey(department, on_delete=models.CASCADE)
    courseNumber = models.IntegerField()
    description = models.CharField(max_length=100)

    # instructor name and email of who teaches the course
    instructorName = models.CharField(max_length=100)
    instructorEmail = models.EmailField(max_length=100)

    # class info about which semester course is taught in, credits, section, and type of class
    semesterCode = models.IntegerField()
    courseSection = models.CharField(max_length=30)
    credits = models.CharField(max_length=30)
    lectureType = models.CharField(max_length=30)

    # all numbers related to waitlist and remaining class seats
    classCapacity = models.IntegerField()
    classEnrollment = models.IntegerField()
    classSpotsOpen = models.IntegerField()
    waitlist = models.IntegerField()
    waitlistMax = models.IntegerField()

    # meeting information
    meeting_days = models.CharField(max_length=100, default = "")
    start_time = models.CharField(max_length=100, default = "")
    end_time = models.CharField(max_length=100, default = "")
    room_location = models.CharField(max_length=100, default = "")
    # def __str__(self):
    #     return self.courseNumber


    def __str__(self):
        dep =  self.department
        num = self.courseNumber
        return str(dep) + " " + str(num)


class ShoppingCart(models.Model):
    user = models.OneToOneField(myUser, on_delete=models.CASCADE)
    courses = models.ManyToManyField(course, related_name = 'courses')