from django.test import RequestFactory, TestCase
from django.urls import reverse
from main.models import myUser, department, course
from .views import editprofile

# Create your tests here.
class URLTest(TestCase):
    def test_main_page_url(self):
        response = self.client.get('/main/')
        self.assertTrue(response.status_code == 200)

    def test_fake_url(self):
        response = self.client.get('/fake/')
        self.assertFalse(response.status_code == 200)

    def test_edit_profile_url(self):
        response = self.client.get('/main/editprofile/')
        self.assertTrue(response.status_code == 200)

    def test_course_catalog_url(self):
        response = self.client.get('/main/coursecatalog/')
        self.assertTrue(response.status_code == 200)

    def test_search_class_url(self):
        response = self.client.get('/main/searchclass/')
        self.assertTrue(response.status_code == 200)

    def test_my_schedule_url(self):
        response = self.client.get('/main/myschedule/')
        self.assertTrue(response.status_code == 200)

    def test_shopping_cart_url(self):
        response = self.client.get('/main/shoppingcart/')
        self.assertTrue(response.status_code == 200)

class UserTestCase(TestCase):
    def setUp(self, id=0, name="", email="", summary="", major="", graduationYear=0):
        self.factory = RequestFactory()
        return myUser.objects.create(id = id,name=name,email=email,summary=summary,major=major,graduationYear=graduationYear)

    def test_user_creation(self):
        user = self.setUp(id = 1,name="FirstLast",email="FL1@gmailcom",summary="sum",major="CS",graduationYear=2024)
        self.assertTrue(isinstance(user,myUser))
        self.assertEqual(user.__str__(), user.name)

class DepartmentTestCase(TestCase):
    def setUp(self, abbreviation="abv", departmentName="CS"):
        return department.objects.create(abbreviation=abbreviation,departmentName=departmentName)

    def test_department_creation(self):
        dep = self.setUp()
        self.assertTrue(isinstance(dep, department))
        self.assertEqual(dep.__str__(),dep.abbreviation)

class CourseTestCase(TestCase):
    def setUp(self,courseNumber=1,description="desc",instructorName="Name",instructorEmail="Name@gmail.com",semesterCode=1,courseSection="a",credits="3",lectureType="In Person",classCapacity=20,classEnrollment=12,classSpotsOpen=8,waitlist=0,waitlistMax=5,meeting_days="Mon Wed Fri",start_time="9:00",end_time="9:50",room_location="Rice 130"):
        dep = department.objects.create(abbreviation="CS",departmentName="Computer Science")
        return course.objects.create(department=dep,courseNumber=courseNumber,description=description,instructorName=instructorName,instructorEmail=instructorEmail,semesterCode=semesterCode,courseSection=courseSection,credits=credits,lectureType=lectureType,classCapacity=classCapacity,classEnrollment=classEnrollment,classSpotsOpen=classSpotsOpen,waitlist=waitlist,waitlistMax=waitlistMax,meeting_days=meeting_days,start_time=start_time,end_time=end_time,room_location=room_location)

    def test_course_creation(self):
        c = self.setUp()
        self.assertTrue(isinstance(c, course))
        self.assertEqual(c.__str__(),(str(c.department)+" "+str(c.courseNumber)))
