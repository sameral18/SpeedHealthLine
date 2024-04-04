from django.contrib import admin
from .models import Doctor, Patient, Appointment, PatientDischargeDetails, Question, Survey, Option, Answer, Message
from django.contrib import admin
from .models import Survey, Patient, Doctor

# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    pass

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass



class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

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
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(Message)
