from django import forms 
from django.forms import Form
from student_management_app.models import Courses, SessionYearModel
from .models import Video


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email Адрес", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Пароль", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="Имя", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Фамилия", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Логин", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Адрес", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))


    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []
    
    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" до "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []
    
    gender_list = (
        ('Male','Мужской'),
        ('Female','Женский')
    )
    
    course_id = forms.ChoiceField(label="Курс", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Пол", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Год Сессии", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Аватар", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    balance = forms.DecimalField(label='Баланс', max_digits=8, widget=forms.NumberInput(attrs={"class":"form-control"}))
    subscribed = forms.BooleanField(label='Активная подписка', widget=forms.CheckboxInput(attrs={"class":"form-control"}))




class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email Адрес", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="Имя", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Фамилия", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Логин", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Адрес", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    #For Displaying Courses
    try:
        courses = Courses.objects.all()
        course_list = []
        for course in courses:
            single_course = (course.id, course.course_name)
            course_list.append(single_course)
    except:
        course_list = []

    #For Displaying Session Years
    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)
            
    except:
        session_year_list = []

    
    gender_list = (
        ('Male','Мужской'),
        ('Female','Женский')
    )
    
    course_id = forms.ChoiceField(label="Курс", choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Пол", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Год Сессии", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    # session_start_year = forms.DateField(label="Session Start", widget=DateInput(attrs={"class":"form-control"}))
    # session_end_year = forms.DateField(label="Session End", widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Аватар", required=False, widget=forms.FileInput(attrs={"class":"form-control"}))
    balance = forms.DecimalField(label='Баланс', max_digits=8, widget=forms.NumberInput(attrs={"class":"form-control"}))
    subscribed = forms.BooleanField(label='Активная подписка')


class SubscriptionForm(forms.Form):
    months = forms.IntegerField(min_value=1, label='Число месяцев')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video_file',)