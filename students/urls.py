from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [

    path('' , views.home , name="home"),
    path('addStudents/' , views.addStudents , name="addStudents"),
    path('updateStudent/<int:id>' , views.updateStudent , name="updateStudent"),
    path('deleteStudent/<int:id>' , views.deleteStudent , name="deleteStudent"),
    path('payment/<int:id>', views.make_payment, name='make_payment')
]
