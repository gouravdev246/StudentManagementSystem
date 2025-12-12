from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=5)

    def __str__(self):
        return self.name
class Student(models.Model):
    MONTH = (
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=10 , blank=True , null=True)
    classroom = models.ForeignKey(ClassRoom , on_delete=models.CASCADE)
    join_month = models.CharField(max_length=10 , choices=MONTH , default="January")
    number = models.CharField(max_length=10)
    payment = models.BooleanField(default=False)
    
    payment_date = models.DateField(auto_now_add=True)



    def __str__(self):
        return f"{self.name} - {self.roll}"

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_records')
    month = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} - {self.month}"
