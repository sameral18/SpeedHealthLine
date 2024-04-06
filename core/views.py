from django.views.generic import ListView
from django.contrib.auth.hashers import make_password

from django.views.generic import CreateView

from django.contrib.auth.models import Group

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from django.conf import settings
from django.db.models import Q

from .forms import AdminProfileForm, DoctorScheduleForm, \
    AnswerForm


def home_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('login_user')
    return render(request, 'index.html')


def Userclick(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'index.html')
    return render(request, 'Userclick.html')






def admin_signup(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('Userlogin')
    return render(request, 'adminsignup.html', {'form': form})


def doctor_signup(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('Userlogin')
    return render(request, 'doctorsignup.html', context=mydict)


def patientsignup(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        else:
            return render(request, 'index.html')
        return HttpResponseRedirect('Userlogin')
    return render(request, 'patientsignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()



from django.contrib.auth import logout

def login_user(request):
    try:
        if is_admin(request.user):
            return redirect('admin-dashboard')
        elif is_doctor(request.user):
            account_approval = models.Doctor.objects.filter(user_id=request.user.id, status=True).exists()
            if account_approval:
                return redirect('doctor-dashboard')
            else:
                messages.warning(request, 'Your doctor account is pending approval.')
                return render(request, 'doctor_wait_for_approval.html')
        elif is_patient(request.user):
            account_approval = models.Patient.objects.filter(user_id=request.user.id, status=True).exists()
            if account_approval:
                return redirect('patient-dashboard')
            else:
                messages.warning(request, 'Your patient account is pending approval.')
                return render(request, 'patient_wait_for_approval.html')
        else:
            messages.error(request, 'Unknown user role.')
            logout(request)
            return render(request, 'index.html')
    except Exception as e:
        print(f"Error in login_user: {e}")
        messages.error(request, 'An error occurred. Please try again.')
        logout(request)
        return render(request, 'index.html')
def logout_user(request):
    logout(request)
    return render(request, 'index.html')


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_dashboard(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by('-id')
    patients = models.Patient.objects.all().order_by('-id')
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = models.Appointment.objects.all().filter(status=False).count()
    mydict = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'appointmentcount': appointmentcount,
        'pendingappointmentcount': pendingappointmentcount,
    }
    return render(request, 'admin_dashboard.html', context=mydict)


# this view for sidebar click on User page
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_doctor(request):
    return render(request, 'admin_doctor.html')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_doctor(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'admin_view_doctor.html', {'doctors': doctors})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def delete_doctor_from_core(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def update_doctor(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)

    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request, 'admin_update_doctor.html', context=mydict)


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_doctor(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request, 'admin_add_doctor.html', context=mydict)


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_approve_doctor(request):
    # those whose approval are needed
    doctors = models.Doctor.objects.all().filter(status=False)
    return render(request, 'admin_approve_doctor.html', {'doctors': doctors})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def approve_doctor(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def reject_doctor(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_doctor_specialisation(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'admin_doctor_specialisation.html', {'doctors': doctors})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_patient(request):
    return render(request, 'admin_patient.html')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_patient(request):
    patients = models.Patient.objects.all().filter(status=True)
    return render(request, 'admin_view_patient.html', {'patients': patients})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def delete_patient_from_core(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def update_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request, 'admin_update_patient.html', context=mydict)



@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_patient(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request, 'admin_add_patient.html', context=mydict)


# ------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_approve_patient(request):
    # those whose approval are needed
    patients = models.Patient.objects.all().filter(status=False)
    return render(request, 'admin_approve_patient.html', {'patients': patients})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def approve_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    patient.status = True
    patient.save()
    return redirect(reverse('admin-approve-patient'))


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def reject_patient(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')


# --------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
# -----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_appointment(request):
    return render(request, 'admin_appointment.html')


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_appointment(request):
    appointments = models.Appointment.objects.filter(status=True).order_by('-id')
    #appointments = models.Appointment.objects.filter(patientId=request.user.id, status=True).order_by('-id')
    return render(request, 'admin_view_appointment.html', {'appointments': appointments})


from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from . import forms


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_appointment(request):
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            doctor_id = appointmentForm.cleaned_data['doctorId'].user_id
            patient_id = appointmentForm.cleaned_data['patientId'].user_id
            # Retrieve doctor and patient names
            doctor = models.User.objects.get(id=doctor_id)
            patient = models.User.objects.get(id=patient_id)
            appointment.doctorId = doctor_id
            appointment.patientId = patient_id
            appointment.doctorName = doctor.first_name
            appointment.patientName = patient.first_name
            # Check if doctor name and department match
            if doctor.first_name != appointmentForm.cleaned_data['doctorId'].user.first_name:
                messages.error(request, 'Doctor name or department does not match.')
                return redirect('admin-add-appointment')
            appointment.status = True
            appointment.save()
            return HttpResponseRedirect('admin-view-appointment')
    else:
        appointmentForm = forms.AppointmentForm()

    return render(request, 'admin_add_appointment.html', {'appointmentForm': appointmentForm})





# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_patient(request):
    mydict = {
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'doctor_patient.html', context=mydict)


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_view_patient(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def search(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).filter(
          Q(user__first_name__icontains=query))
    return render(request, 'doctor_patient.html', {'patients': patients, 'doctor': doctor})




@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_appointment(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_appointment.html', {'doctor': doctor})
@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def profile_d(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'profile_d.html', {'doctor': doctor})
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def profile_p(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    return render(request, 'profile_p.html', {'patient': patient, 'doctors': doctors})

@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.filter(status=True).order_by('-id')
    patientid = []
    for a in appointments:
        doctor = a.timeslots
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        doctor = a.timeslots
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def delete_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        doctor = a.timeslots
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_approve_appointment(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.filter(status=False).order_by('-id')
    return render(request, 'doctor_approve_appointment.html', {'appointments': appointments})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def approve_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect('doctor-approve-appointment')


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def reject_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor-approve-appointment')

# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    mydict = {
        'PatientName': patient.get_name,
        'UserName': patient.get_name,
        'Address': patient.address,
        'Mobile': patient.mobile,
        'a': patient.assignedDoctorId,
        'AdmitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', context=mydict)





from datetime import date






import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return


def download_pdf(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'mobile':dischargeDetails[0].mobile,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html',dict)


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    # for three cards
    patientcount = models.Patient.objects.filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentcount = models.Appointment.objects.filter(status=True, doctorName=request.user.username).count()
    patientdischarged = models.PatientDischargeDetails.objects.filter(assignedDoctorName=request.user.first_name).count()

    # for table in doctor dashboard
    appointments = models.Appointment.objects.filter(status=True).order_by('-id')

    patients = models.Patient.objects.filter(status=True).order_by('-id')
    appointments = zip(appointments, patients)

    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'patientdischarged': patientdischarged,
        'appointments': appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'doctor_dashboard.html', context=mydict)

@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_appointment(request):
    appointments = models.Appointment.objects.filter(status=True).order_by('-id')
    return render(request, 'patient_appointment.html', context={'patient': Patient, 'appointments': appointments})




from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import PatientAppointmentForm
from .models import Doctor, DoctorSchedule, Patient, Answer


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_book_appointment(request):
    if request.method == 'POST':
        appointmentForm = PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            doctor_id = request.POST.get('doctorId')
            description = request.POST.get('description')

            try:
                doctor = Doctor.objects.get(user_id=doctor_id)
            except Doctor.DoesNotExist:
                messages.error(request, 'Invalid doctor selected.')
                return redirect('patient-book-appointment')

            timeslots = DoctorSchedule.objects.all()
            if not timeslots.exists():
                messages.error(request, 'No timeslots available for the selected doctor.')
                return redirect('patient-book-appointment')

            # Check if doctor name and department match
            if doctor.user.first_name != appointmentForm.cleaned_data['doctorId'].user.first_name :
                messages.error(request, 'Doctor name or department does not match.')
                return redirect('patient-book-appointment')

            # Save appointment
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = doctor_id
            appointment.patientId = request.user.id
            appointment.doctorName = doctor.user.first_name
            appointment.patientName = request.user.first_name
            appointment.status = True
            appointment.save()  # Save the appointment first

            # Now set the timeslots
            appointment.timeslots.set(request.POST.get('timeslots'))

            messages.success(request, 'Appointment booked successfully.')
            return HttpResponseRedirect('patient-view-appointment')

    else:
        appointmentForm = PatientAppointmentForm()

    patient = Patient.objects.get(user_id=request.user.id)
    context = {'appointmentForm': appointmentForm, 'patient': patient}
    return render(request, 'patient_book_appointment.html', context)


def patient_doctor(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    return render(request, 'patient_doctor.html', {'patient': patient, 'doctors': doctors})


def search_doctor(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar

    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors = models.Doctor.objects.all().filter(status=True).filter(
        Q(department__icontains=query) | Q(user__first_name__icontains=query))
    return render(request, 'patient_doctor.html', {'patient': patient, 'doctors': doctors})


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_view_appointment(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.filter(status=True).order_by('-id')
    return render(request, 'patient_view_appointment.html', {'appointments': appointments, 'patient': patient})



@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_profile(request):
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.password = make_password(password)  # Hash the password
            user.save()
            return redirect('admin-dashboard')  # Redirect to a success page
    else:
        form = AdminProfileForm(instance=request.user)
    return render(request, 'admin_profile.html', {'form': form})



def aboutus(request):
    return render(request, 'aboutus.html')


def contactus(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form': sub})

@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_profile(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=doctor.user_id)
    userForm = forms.DoctorUserForm(instance=user)
    doctorForm = forms.DoctorForm(request.FILES, instance=doctor)
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST, instance=user)
        doctorForm = forms.DoctorForm(request.POST, request.FILES, instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.status = True
            doctor.save()
            return redirect('profile-doctor')
    return render(request, 'doctor_profile.html', context=mydict)
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_profile(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=patient.user_id)

    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, request.FILES, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('profile-patient')
    return render(request, 'patient_profile.html', context=mydict)




@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def add_doctor_schedule(request):
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            new_schedule = form.save(commit=False)
            new_schedule.doctor = request.user
            new_schedule.save()
            return redirect('doctor-dashboard')
    else:
        form = DoctorScheduleForm()

    return render(request, 'doctor_schedule_form.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms import formset_factory
from .forms import SurveyForm, QuestionForm, AnswerForm
from .models import Survey, Question


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def delete_my_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    doctor = models.Doctor.objects.get(user_id=appointment.doctorId)  # for profile picture of doctor in sidebar

    appointment.delete()
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        doctor = a.timeslots
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments, 'doctor': doctor})

@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})
@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def discharge_patient(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate)
    assignedDoctor=models.User.objects.all().filter()
    d=days.days
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'patient_final_bill.html',context=patientDict)
    return render(request,'patient_generate_bill.html',context=patientDict)
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_discharge(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient_discharge.html',context=patientDict)
@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def d_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'d_discharge_patient.html',{'patients':patients})




from django.shortcuts import render, redirect
from .models import Survey, Question, Answer
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_survey(request):
    answers = Answer.objects.all()
    return render(request, 'admin_view_answers.html', {'answers': answers})
@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_answers(request):
    answers = Answer.objects.all()
    return render(request, 'admin_view_answers.html', {'answers': answers})

















@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_survey(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        survey = Survey.objects.create(title=title, description=description)
        survey.save()
        return redirect('admin-add-questions', survey_id=survey.id)  # تحويل المستخدم إلى إضافة الأسئلة بعد إنشاء الاستبيان
    return render(request, 'admin_add_survey.html')

@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_questions(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        Question.objects.create(survey=survey, question_text=question_text)
        # يمكنك تحديد مكان التوجيه بناءً على ما تريده
        return redirect('admin-view-survey')  # يمكن أن يتم توجيه المستخدم إلى عرض الاستبيان أو أي مكان آخر بعد إضافة الأسئلة

    return render(request, 'admin_add_questions.html', {'survey': survey})

@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_survey(request):
    surveys = Survey.objects.all()
    return render(request, 'admin_view_survey.html', {'surveys': surveys})


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_answer_questions(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey=survey)

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            Answer.objects.create(question=question, answer_text=answer_text, answered_by=request.user)

        return redirect('patient-dashboard')

    return render(request, 'patient_answer_questions.html', {'survey': survey, 'questions': questions})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_answer_questions(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey=survey)

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            Answer.objects.create(question=question, answer_text=answer_text, answered_by=request.user)

        return redirect('doctor-dashboard')

    return render(request, 'doctor_answer_questions.html', {'survey': survey, 'questions': questions})

@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_view_survey(request):
    surveys = Survey.objects.all()
    survey_responses = []

    for survey in surveys:
        answers = Answer.objects.filter(question__survey=survey)
        survey_responses.append({'survey': survey, 'answers': answers})

    return render(request, 'patient_view_survey.html', {'survey_responses': survey_responses})

@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_view_survey(request):
    surveys = Survey.objects.all()
    survey_responses = []

    for survey in surveys:
        answers = Answer.objects.filter(question__survey=survey)
        survey_responses.append({'survey': survey, 'answers': answers})

    return render(request, 'doctor_view_survey.html', {'survey_responses': survey_responses})




@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_add_answers(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey=survey)

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')
            Answer.objects.create(question=question, answer_text=answer_text, answered_by=request.user)

        return redirect('doctor-dashboard')

    return render(request, 'doctor_add_answers.html', {'survey': survey, 'questions': questions})



@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_add_answers(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = Question.objects.filter(survey=survey)

    if request.method == 'POST':
        for question in questions:
            answer_text = request.POST.get(f'answer_{question.id}')  # Assuming input names are 'answer_<question_id>'
            Answer.objects.create(question=question, answer_text=answer_text, answered_by=request.user)

        return redirect('patient-dashboard')  # Redirect to patient dashboard or any other page

    return render(request, 'patient_add_answers.html', {'survey': survey, 'questions': questions})
