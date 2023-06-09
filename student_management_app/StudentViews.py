from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime,time # To Parse input DateTime into Python Date Time Object
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.forms import PayPalIPNForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .forms import SubscriptionForm


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    
    context={
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects,
        "subject_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "student_template/student_home_template.html", context)


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    course = student.course_id # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)







@login_required
def payment(request):
    try:
        student = Students.objects.get(admin=request.user)
    except Students.DoesNotExist:
        return HttpResponseForbidden("Access denied.")
    amount = 10  # You can change this value based on your subscription pricing

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "Subscription",
        "invoice": f"INV-{student.id}-{int(time.time())}",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
        "custom": str(request.user.id),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "student_template/payment.html", {"form": form, "student":student})

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payment_done(request):
    student_id = request.GET.get('custom')
    student = Students.objects.get(admin=request.user)
    amount = 10  # Use the same value as in make_payment view
    student.create_transaction(amount)
    return render(request, 'student_template/payment_done.html')

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'student_template/payment_cancelled.html')







logger = logging.getLogger(__name__)

@csrf_exempt
def paypal_ipn(request):
    # Verify the IPN received from PayPal
    form = PayPalIPNForm(request.POST)
    if form.is_valid():
        ipn = form.save()
        logger.info(f"PayPal IPN received: {ipn}")

        # Update the student's balance
        try:
            student = Students.objects.get(admin=ipn.custom)
            student.balance += Decimal(ipn.mc_gross)
            student.save()
            logger.info(f"Updated balance for student: {student.id} to {student.balance}")
        except Students.DoesNotExist:
            logger.error(f"Student not found for user ID: {ipn.custom}")
    else:
        logger.error("Invalid PayPal IPN received")

    return HttpResponse(status=200)


from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Students
from .forms import SubscriptionForm
@login_required

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            months = form.cleaned_data['months']
            student = Students.objects.get(admin=request.user)
            if student.purchase_subscription(months):
                messages.success(request, f'Successfully purchased a {months}-month subscription.')
            else:
                messages.error(request, 'Not enough balance to purchase the subscription.')
            return redirect('subscribe')  # Replace 'subscription' with the appropriate URL name
    else:
        form = SubscriptionForm()
    student = Students.objects.get(admin=request.user)
    subscription_status = 'active' if student.has_paid() else 'inactive'
    return render(request, 'student_template/subscribe.html', {'form': form, 'subscription_status': subscription_status,})

from django.http import HttpResponseForbidden

def require_subscription(view_func):
    def _wrapped_view(request, *args, **kwargs):
        student = Students.objects.get(admin=request.user)
        if student.has_paid():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You need an active subscription to access this page.')

    return _wrapped_view

from .decorators import require_subscription

@login_required
@require_subscription
def restricted_view(request):
    # Your view logic here
    return render(request, 'student_template/restricted_page.html')

from .models import Video

def video_list(request):
    return render(request, 'student_template/videos.html', {'videos': Video.objects.all()})





