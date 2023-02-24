import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db.models import Q
from .managers import MyUserManager
from django.db.models.signals import post_delete
from django.dispatch import receiver


class StaffRank(models.Model):
    rank = models.CharField(max_length=30)

    def __str__(self):
        return self.rank


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, db_index=True, verbose_name='email address', max_length=255)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    is_superuser = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_name(self):
        return self.email


class Staff(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='owner')
    mobile = models.IntegerField()
    role = models.ForeignKey(StaffRank, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.staff)


class Specialization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    week_days = (
        ('6', 'Sunday'),
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE,)
    day_of_the_week = models.CharField(max_length=10, choices=week_days)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.staff)


class Doctor(models.Model):
    name = models.OneToOneField(Staff, on_delete=models.CASCADE, primary_key=True)
    # a doctor can have many specialties
    specialization = models.ManyToManyField('Specialization')

    def clean(self, *args, **kwargs):
        if self.name.role.rank != 'Head Doctor' and self.name.role.rank != 'Doctor':
            raise ValidationError({'name': 'This staff is not a Head Doctor or a Doctor'})
        super(Doctor, self).clean(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    def get_availability(self, time, date, end_time):
        not_available = Appointment.objects.filter(assigned_doctor=self, date=date,
                                                   start_time__range=[time, end_time]).exists()

        return False if not_available else True


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class BillItem(models.Model):
    bill_type = [
        ('S', 'Service Fee'),
    ]
    billType = models.CharField(max_length=10, choices=bill_type)
    name = models.CharField(max_length=50)
    item_price = models.PositiveIntegerField()


class Invoice(models.Model):
    patient_name = models.ForeignKey('PatientDetails', on_delete=models.CASCADE)
    doctor_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    release_date = models.DateField(default=None)
    bill = models.ManyToManyField(BillItem)
    days_spent = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name


class Bed(models.Model):
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class AdmittedPatient(models.Model):
    patient = models.OneToOneField('PatientDetails', on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True)
    assigned_doctor = models.ManyToManyField(Doctor, verbose_name='doctor')
    bed = models.OneToOneField(Bed, on_delete=models.RESTRICT)

    def save(self, *args, **kwargs):
        if self.bed.in_use is True:
            raise ValidationError({'bed': 'Bed has already been taken please choose another one or create one instead!'})
        patient = PatientDetails.objects.get(patient=self.patient)
        patient.admitted = True
        patient.save()
        bed = Bed.objects.get(id=self.bed.id)
        bed.in_use = True
        bed.save()
        super(AdmittedPatient, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.patient)


@receiver(post_delete, sender=AdmittedPatient)
def model_delete(sender, instance, **kwargs):
    bed = Bed.objects.get(id=instance.bed.id)
    bed.in_use = False
    bed.save()


class Appointment(models.Model):
    next_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    stats = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('C', 'Completed')
    ]
    reason = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default=next_hour.time())
    patient = models.ForeignKey('PatientDetails', on_delete=models.CASCADE)
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=stats, default='P')

    def clean(self):
        if self.date < datetime.date.today():
            raise ValidationError({"date": "Date must not be less than today's date"})
        if self.start_time > self.end_time and self.date >= datetime.date.today():
            raise ValidationError({'start_time': 'Start time exceeds endtime'})

        # Check for overlapping appointments for the same patient or assigned doctor
        conflicting_appointments = Appointment.objects.filter(
            Q(patient=self.patient) | Q(assigned_doctor=self.assigned_doctor),
            status__in=['P', 'A'],  # Only check pending or approved appointments
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)  # Exclude self if updating an existing appointment

        if conflicting_appointments.exists():
            raise ValidationError({'start_time': 'Doctor has an appointment'})


    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return str(self.patient)


class PatientDetails(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobile = models.IntegerField()
    age = models.IntegerField()
    weight = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=4)
    address = models.CharField(max_length=50)
    symptoms = models.CharField(max_length=30)
    entry = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.patient.get_name()

