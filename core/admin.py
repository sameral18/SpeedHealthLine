from django.contrib import admin
from .models import Doctor, Patient, Appointment, PatientDischargeDetails, Question, Survey
from django.contrib import admin
from .models import Survey, Patient, Doctor

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    pass

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass





class QuestionAdmin(admin.ModelAdmin):
 pass
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1




class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']  # Customize the fields displayed in the list view

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'admitDate']  # Customize as needed

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'status']  # Customize as needed

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Question, QuestionAdmin)

