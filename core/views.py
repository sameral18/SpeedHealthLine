from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import  date
from django.conf import settings
from django.db.models import Q

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


def patient_signup(request):
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
        return HttpResponseRedirect('Userlogin')
    return render(request, 'patientsignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT

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
def delete_patient_from_hospital(request, pk):
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
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'admin_view_appointment.html', {'appointments': appointments})


@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_add_appointment(request):
    appointmentForm = forms.AppointmentForm()
    mydict = {'appointmentForm': appointmentForm, }
    if request.method == 'POST':
        appointmentForm = forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.POST.get('patientId')
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request, 'admin_add_appointment.html', context=mydict)


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_approve_appointment(request):
    # those whose approval are needed
    appointments = models.Appointment.objects.all().filter(status=False)
    return render(request, 'doctor_approve_appointment.html', {'appointments': appointments})


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def approve_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.status = True
    appointment.save()
    return redirect(reverse('doctor-approve-appointment'))


@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def reject_appointment(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor-approve-appointment')


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
def doctor_view_appointment(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
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
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'patient_dashboard.html', context=mydict)


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_appointment(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    return render(request, 'patient_appointment.html', {'patient': patient})


@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_book_appointment(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    message = None
    mydict = {'appointmentForm': appointmentForm, 'patient': patient, 'message': message}
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc = request.POST.get('description')

            doctor = models.Doctor.objects.get(user_id=request.POST.get('doctorId'))

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.user.id  # ----user can choose any patient but only their info will be stored
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = request.user.first_name  # ----user can choose any patient but only their info will be stored
            appointment.status = False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request, 'patient_book_appointment.html', context=mydict)


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
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments, 'patient': patient})




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

