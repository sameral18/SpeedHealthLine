from django.contrib import admin
from .models import Doctor, Patient, Appointment, PatientDischargeDetails, Question, Survey, Answer, DoctorSchedule


class AppointmentAdmin(admin.ModelAdmin):
    pass

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass

class QuestionAdmin(admin.ModelAdmin):
    pass

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer_text']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    inlines = [QuestionInline]  # Inline questions in the survey admin

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'mobile', 'admitDate']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'status']

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(DoctorSchedule)
