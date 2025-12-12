from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Student, ClassRoom, Payment
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    students = Student.objects.filter(user=request.user).prefetch_related('payment_records')
    context = {
        'students' : students
    }
    return render(request , 'home.html' , context)


@login_required
def addStudents(request):
    classrooms = ClassRoom.objects.all()
    students = Student.objects.all()
    context = {
        'classrooms': classrooms,
        'students': students,
        'months': Student.MONTH
    }
    if request.method == 'POST':
        name = request.POST.get('name')
       
        classroom_id = request.POST.get('classroom_id')
        number = request.POST.get('number')
        join_month = request.POST.get('join_month')
        payment = request.POST.get('payment')
        email = request.POST.get('email')
        if name:
            payment = True if payment == 'on' else False
            student = Student.objects.create(
                user=request.user,
                name=name, 
             
                classroom_id=classroom_id,
                number=number , 
                join_month=join_month,
                payment=payment,
                email=email
            )
            student.save()
            return redirect('home')
        else:
             # Handle missing name (optional: could return error message)
             pass
        return redirect('home')
    else:
        return render(request , 'addstudent.html', context)

@login_required
def updateStudent(request , id):
    student = Student.objects.get(id=id, user=request.user)
    classrooms = ClassRoom.objects.all()
    context = {
        'student': student ,
        'months': Student.MONTH ,
        'classrooms': classrooms,
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        email = request.POST.get('email')
        classroom_id = request.POST.get('classroom_id')
        number = request.POST.get('number')
        join_month = request.POST.get('join_month')
        payment = request.POST.get('payment')
        if name:
            student.name = name
            student.roll = roll
            student.email = email
            student.classroom_id = classroom_id
            student.number = number
            student.join_month = join_month
            payment_status = True if payment == 'on' else False
            student.payment = payment_status
            if payment_status:
                Payment.objects.create(student=student, month=join_month)
            student.save()
            return redirect('home')
        
    return render(request , 'updatestudent.html', context)

@login_required
def deleteStudent(request , id):
    student = Student.objects.get(id=id, user=request.user)
    student.delete()
    return redirect('home')

from django.core.mail import send_mail

@login_required
def make_payment(request, id):
    student = Student.objects.get(id=id, user=request.user)
    
    if request.method == 'POST':
        month = request.POST.get('month')
        student.payment = True
        student.save()
        Payment.objects.create(student=student, month=month)
        
        # Send Email
        if student.email:
            send_mail(
                'Payment Confirmation',
                f'Hello {student.name},\n\nYour payment for the month of {month} has been successfully received.\n\nThank you!',
                'gouravdev246@gmail.com', # Use configured email
                [student.email],
                fail_silently=False,
            )
            
        return redirect('home')

    context = {
        'student': student,
        'months': Student.MONTH
    }
    return render(request, 'payment.html', context)