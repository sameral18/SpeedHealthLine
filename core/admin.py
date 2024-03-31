from django.contrib import admin
from .models import Doctor, Patient, Appointment, PatientDischargeDetails, Question, Survey, Option, Answer


# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
class AppointmentAdmin(admin.ModelAdmin):
    pass
class PatientAdmin(admin.ModelAdmin):
    pass
class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass

admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Appointment, AppointmentAdmin)

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(Answer)
