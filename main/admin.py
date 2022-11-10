from django.contrib import admin
from .models import myUser, course, department, Friend_Request, FriendList, ShoppingCart
# Register your models here.

admin.site.register(myUser)
admin.site.register(course)
admin.site.register(department)
admin.site.register(Friend_Request)
admin.site.register(FriendList)
admin.site.register(ShoppingCart)