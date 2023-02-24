from django.forms import ModelForm
from . import models
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

from .models import Doctor


class PatientForm(ModelForm):
    class Meta:
        model = models.PatientDetails
        fields = ['address', 'height', 'age', 'weight', 'blood_type', 'patient', 'mobile',
                  'symptoms']


class Register(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = ['email', 'password1', 'password2', 'firstname', 'lastname']


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class DoctorAppForm(ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['reason', 'date', 'start_time', 'end_time', 'patient', 'assigned_doctor', 'status']


class InvoiceForm(ModelForm):
    class Meta:
        model = models.Invoice
        fields = '__all__'


class StaffForm(ModelForm):
    class Meta:
        model = models.Staff
        fields = '__all__'


class DoctorForm(ModelForm):
    class Meta:
        model = models.Doctor
        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'


class AppointmentForm(ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['reason', 'date', 'start_time', 'end_time', 'assigned_doctor', 'patient']

    def save(self, commit=True):
        instance = super().save(commit=False)
        try:
            instance.save()
        except Exception as e:
            self.add_error(None, str(e))
            return None
        return instance


class AppointmentFilterForm(forms.Form):
    APPOINTMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('C', 'Completed'),
    ]
    date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    time = forms.TimeField(required=False, widget=forms.TextInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(required=False, widget=forms.TextInput(attrs={'type': 'time'}))
    status = forms.ChoiceField(required=False, choices=APPOINTMENT_STATUS_CHOICES)
    doctor = forms.ModelChoiceField(required=False, queryset=Doctor.objects.all())
    reason = forms.CharField(required=False)

