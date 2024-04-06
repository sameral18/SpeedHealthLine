from django import forms
from django.contrib.auth.models import User
from . import models
from django import forms
from .models import Doctor, DoctorSchedule, Appointment


#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
#
class AdminProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)  # Make password field optional

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'maxlength': 100}),  # Set maximum length for username field
        }

#1
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
#1
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','certificate_file']


#
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
#
class PatientForm(forms.ModelForm):

    class Meta:
        model=models.Patient
        fields=['mobile','status']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name ", to_field_name="user_id")
    appointmentDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Date'}))
    appointmentTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}))
    timeslots = forms.ModelChoiceField(queryset=DoctorSchedule.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Timeslots'}))

    class Meta:
        model = Appointment
        fields = ['description', 'appointmentDate', 'appointmentTime', 'timeslots']

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'doctorId' in self.data:
            try:
                doctor_id = int(self.data.get('doctorId'))
                self.fields['timeslots'].queryset = DoctorSchedule.objects.filter(doctor_id=doctor_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['timeslots'].queryset = self.instance.doctor.timeslots.all()



#
class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.filter(status=True), empty_label="Doctor Name and Department", to_field_name="user_id", widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Doctor'}))
    appointmentDate = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Date'}))
    appointmentTime = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Appointment Time'}))
    timeslots = forms.ModelChoiceField(queryset=DoctorSchedule.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Timeslots'}))

    class Meta:
        model = Appointment
        fields = ['description', 'appointmentDate', 'appointmentTime', 'timeslots']

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }
#2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'doctorId' in self.data:
            try:
                doctor_id = int(self.data.get('doctorId'))
                self.fields['timeslots'].queryset = DoctorSchedule.objects.filter(doctor_id=doctor_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['timeslots'].queryset = self.instance.doctor.timeslots.all()


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


#
class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ['date', 'time']
# forms.py
from django import forms
from django.forms import formset_factory, ModelForm
from .models import Survey, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

SurveyQuestionFormSet = formset_factory(QuestionForm, extra=1)

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', ]

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(label=question.question_text, required=False)





