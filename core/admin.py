from django.contrib import admin
from .models import Doctor, Patient, Appointment, PatientDischargeDetails


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

