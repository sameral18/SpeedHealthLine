from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']



class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):

    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['address','mobile','status','profile_pic']



class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
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
    return render(request, 'doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_view_patient(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_view_patient.html', {'patients': patients, 'doctor': doctor})@login_required(login_url='Userlogin')
@user_passes_test(is_doctor)
def doctor_appointment(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'doctor_appointment.html', {'doctor': doctor})@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_appointment(request):
    return render(request, 'admin_appointment.html')@login_required(login_url='Userlogin')
@user_passes_test(is_admin)
def admin_view_appointment(request):
    appointments = models.Appointment.objects.all().filter(status=True)
    return render(request, 'admin_view_appointment.html', {'appointments': appointments})@login_required(login_url='Userlogin')
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
    return render(request, 'doctor_approve_appointment.html', {'appointments': appointments})@login_required(login_url='Userlogin')
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
    return redirect('doctor-approve-appointment')@login_required(login_url='Userlogin')
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
@login_required(login_url='Userlogin')
@user_passes_test(is_patient)
def patient_view_appointment(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'patient_view_appointment.html', {'appointments': appointments, 'patient': patient})


