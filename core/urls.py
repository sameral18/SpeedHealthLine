from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.template.defaulttags import url
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import admin
from django.urls import path, include

from .views import *
from . import views
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name=''),
    path('doctor-calender/', add_doctor_schedule, name='doctor-calendar'),
    path('download-pdf/<int:pk>', download_pdf, name='download-pdf'),
    path('aboutus', aboutus),
    path('contactus', contactus),
    path('Userclick', Userclick),
    path('adminsignup', admin_signup),
    path('doctorsignup', doctor_signup, name='doctorsignup'),
    path('patientsignup', patientsignup),
    path('Userlogin', LoginView.as_view(template_name='Userlogin.html'), name='Userlogin'),
    path('admin-profile/', admin_profile, name='admin_profile'),
    path('doctor-profile/', profile_d, name='doctor_profile'),
    path('patient-profile/', profile_p, name='patient_profile'),
    path('profile-patient/', patient_profile, name='profile-patient'),
    path('profile-doctor/', doctor_profile, name='profile-doctor'),
    path('login_user', login_user, name='login_user'),###
    path('logout', logout_user, name='logout'),
    path('admin-dashboard', admin_dashboard, name='admin-dashboard'),
    path('patient-dashboard', patient_dashboard, name='patient-dashboard'),
    path('admin-doctor', admin_doctor, name='admin-doctor'),
    #view doctor "admin"
    path('admin-view-doctor', admin_view_doctor, name='admin-view-doctor'),
    path('delete-doctor-from-core/<int:pk>', delete_doctor_from_core,
         name='delete-doctor-from-core'),
#
    path('delete-patient/<int:pk>', views.delete_patient_from_core,
         name='delete-patient'),

    path('update-doctor/<int:pk>', update_doctor, name='update-doctor'),
    path('admin-add-doctor', admin_add_doctor, name='admin-add-doctor'),
    path('admin-approve-doctor', admin_approve_doctor, name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', approve_doctor, name='approve-doctor'),
    path('reject-doctor/<int:pk>', reject_doctor, name='reject-doctor'),
    path('admin-view-doctor-specialisation', admin_doctor_specialisation,
         name='admin-view-doctor-specialisation'),
    path('admin-patient', admin_patient, name='admin-patient'),
    path('admin-view-patient', admin_view_patient, name='admin-view-patient'),
    #
    path('delete-patient-from-core/<int:pk>', delete_patient_from_core,name='delete-patient-from-core'),
    path('update-patient/<int:pk>', update_patient, name='update-patient'),
    path('admin-add-patient', admin_add_patient, name='admin-add-patient'),
    path('admin-approve-patient', admin_approve_patient, name='admin-approve-patient'),
    path('approve-patient/<int:pk>', approve_patient, name='approve-patient'),
    path('reject-patient/<int:pk>', reject_patient, name='reject-patient'),


    path('admin-appointment', admin_appointment, name='admin-appointment'),
    path('admin-view-appointment', admin_view_appointment, name='admin-view-appointment'),
    path('admin-add-appointment', admin_add_appointment, name='admin-add-appointment'),

    path('doctor-approve-appointment', doctor_approve_appointment, name='doctor-approve-appointment'),

    path('approve-appointment/<int:pk>', approve_appointment, name='approve-appointment'),
    path('reject-appointment/<int:pk>', reject_appointment, name='reject-appointment'),

    path('patient-appointment', patient_appointment, name='patient-appointment'),
    #
    path('patient-book-appointment', patient_book_appointment, name='patient-book-appointment'),
    #
    path('patient-view-appointment', patient_view_appointment, name='patient-view-appointment'),

    path('patient-doctor', patient_doctor, name='patient-doctor'),
    path('searchdoctor', search_doctor, name='searchdoctor'),
    path('doctor-dashboard', doctor_dashboard, name='doctor-dashboard'),
    path('search', search, name='search'),
    path('doctor-patient', doctor_patient, name='doctor-patient'),
    path('doctor-view-patient', doctor_view_patient, name='doctor-view-patient'),

    path('doctor-appointment', doctor_appointment, name='doctor-appointment'),
    path('doctor-view-appointment', doctor_view_appointment, name='doctor-view-appointment'),
    path('doctor-delete-appointment', doctor_delete_appointment, name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', delete_appointment, name='delete-appointment'),
    path('delete-my-appointment/<int:pk>', delete_my_appointment, name='delete-my-appointment'),


    path('discharge-patient/<int:pk>', discharge_patient, name='discharge-patient'),
    path('patient-discharge', patient_discharge, name='patient-discharge'),
    path('d-discharge-patient', d_discharge_patient_view, name='d-discharge-patient'),
    path('doctor-discharge-patient', doctor_view_discharge_patient_view, name='doctor-discharge-patient'),

    path('doctor-add-answers/<int:survey_id>/', views.doctor_add_answers, name='doctor-add-answers'),
    path('patient-add-answers/<int:survey_id>/', views.patient_add_answers, name='patient-add-answers'),

    path('admin-add-questions/<int:survey_id>/', views.admin_add_questions, name='admin-add-questions'),
    path('admin-add-answers', views.admin_add_answers, name='admin-add-answers'),
    path('admin-view-survey', views.admin_view_survey, name='admin-view-survey'),
    path('admin-add-survey', views.admin_add_survey, name='admin-add-survey'),
    path('doctor-answer-questions/<int:survey_id>/', views.doctor_answer_questions, name='doctor-answer-questions'),
    path('patient-answer-questions/<int:survey_id>/', views.patient_answer_questions, name='patient-answer-questions'),
    path('patient-view-surveys', views.patient_view_survey, name='patient-view-surveys'),
    path('doctor-view-surveys', views.doctor_view_survey, name='doctor-view-surveys'),
    path('patient-add-answers/<int:survey_id>/', views.patient_add_answers, name='patient-add-answer'),
    path('doctor-add-answers/<int:survey_id>/', views.doctor_add_answers, name='doctor-add-answer'),

]
