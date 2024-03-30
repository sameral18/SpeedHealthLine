from audioop import reverse

from django.db import models
from django.contrib.auth.models import User



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=True)
    address = models.CharField(max_length=255, default="", blank=True)



    @classmethod
    def create_user(cls, username, password, assignedDoctorId, **extra_fields):
        user = User.objects.create_user(username=username, password=password, **extra_fields)
        patient = cls.objects.create(user=user, assignedDoctorId=assignedDoctorId, **extra_fields)
        return patient
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False, default='0123456789')
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=True)
    @classmethod
    def create_user(cls, username, password, department, **extra_fields):
        user = User.objects.create_user(username=username, password=password, **extra_fields)
        doctor = cls.objects.create(user=user, department=department, **extra_fields)
        return doctor
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Doctor: {self.doctor.username}, Date: {self.date}, Time: {self.time}"

class Appointment(models.Model):
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True)
    appointmentDate = models.DateField(null=True)
    appointmentTime = models.TimeField(null=True)
    timeslots = models.ManyToManyField(DoctorSchedule)  # تعديل هنا للارتباط بنموذج DoctorSchedule
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Appointment with {self.doctorName} on {self.appointmentDate} at {self.appointmentTime}"
