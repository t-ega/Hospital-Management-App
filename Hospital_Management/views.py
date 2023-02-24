from django.urls import reverse_lazy
from django.shortcuts import render
from . import models
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404
import datetime
from .forms import *
from django.http import JsonResponse, QueryDict
from django.views import generic, View
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def has_group(user, group_name):
    """ registers the filter ('has_group') inside the templates rendered
     so that we can check if the user belongs to a particular group"""
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

@login_required(login_url='accounts/login')
def home(request):
    if has_group(request.user, 'Doctors'):
        template_name = 'dashboards/doctorDashboard.html'
    elif has_group(request.user, 'Patients'):
        template_name = 'dashboards/PatientDashBoard.html'
    elif has_group(request.user, 'Admin'):
        template_name = 'dashboards/AdminDashBoard.html'
    elif has_group(request.user, 'Receptionist'):
        print('no')
        template_name = 'dashboards/ReceptionistDashBoard.html'
    return render(request, template_name)

class Register(generic.CreateView):

    form_class = Register
    models = models.User
    success_url = 'admin-dashboard'
    template_name = 'signup.html'
    context_object_name = 'form'

    def get(self, request):
        if self.request.user.is_authenticated:
            form = Register
            return render(request, self.template_name, context={'form': form})


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        user.groups.add('Patients')
        return super(Register, self).form_valid(form)

    def form_invalid(self, form):
        error = form.errors
        raise ValidationError(error)

class Login(View):
    form_class = LoginForm
    models = models.User
    template_name = 'signup.html'

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request,'username or password incorret')
                return render(request, self.template_name, context={'form': form})

        message = form.errors
        return render(request, self.template_name, context={'form': form})


    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name,)


class Logout(View):
    template_file_name = 'login.html'
    def get(self, request):
        logout(request)
        return redirect('login')


class AdminDashBoard(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Mangement.add_log', )
    def get_queryset(self):
        current_date = datetime.date.today()
        days = datetime.timedelta(days=7)
        begin = current_date - days
        total_doctors = models.Doctor.objects.all().count
        admitted_patients = models.AdmittedPatient.objects.select_related('patient')
        admitted_patients_details = admitted_patients.filter(admission_date__range=[begin, current_date])
        total_patients = models.PatientDetails.objects.all().count
        daily_appointments = models.Appointment.objects.filter(date=current_date)
        admitted_patients_count = admitted_patients.count()
        due_appointments = models.Appointment.objects.filter(status='P', date=current_date).count()
        total_beds = models.Bed.objects.all().count()
        total_beds_in_use = models.Bed.objects.filter(in_use=True).count()

        myset = {
            'admitted_patients': admitted_patients,
            'admitted_patients_details': admitted_patients_details,
            'total_doctors': total_doctors,
            'total_beds': total_beds,
            'total_beds_in_use': total_beds_in_use,
            'total_patients': total_patients,
            'admitted_patients_count': admitted_patients_count,
            'appointments': due_appointments,
            'daily_appointments': daily_appointments,
        }

        return myset

    template_name = 'dashboards/AdminDashBoard.html'
    context_object_name = 'data'


class ReceptionistDashBoard(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.add_appointment', 'Hospital_Management.view_doctor',
                           'Hospital_Management.view_appointment', 'Hospital_Management.add_patient', 'Hospital_Management.change_patient', 'Hospital_Management.view_patient')

    context_object_name = 'patients'
    queryset = models.Appointment.objects.all()
    model = models.Appointment
    template_name = 'dashboards/ReceptionistDashBoard.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ReceptionistDashBoard, self).get_context_data(*args, **kwargs)
        context['appointments'] = models.Appointment.objects.filter(date=datetime.date.today())
        context['upcoming_appointments'] = models.Appointment.objects.filter(date__gt=datetime.date.today())
        return context


class CreateAppointment(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView,):
    permission_required = ('Hospital_Management.add_appointment', 'Hospital_Management.change_appointment')
    form_class = AppointmentForm
    template_name = 'appointment_templates/AppointmentForm.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['doctors'] = models.Schedule.objects.filter(Q(staff__role__rank='Doctor') |
                                                            Q(staff__role__rank='Head Doctor'))\
            .filter(day_of_the_week=datetime.date.today().weekday())
        context['patient'] = models.PatientDetails.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        query_string = request.body.decode('utf-8')
        data = QueryDict(query_string)
        form = AppointmentForm(data)
        if form.is_valid():
            date = form.cleaned_data['date']
            time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            reason = form.cleaned_data['reason']
            doctor = form.cleaned_data['assigned_doctor']
            patient = form.cleaned_data['patient']
            appointment = models.Appointment.objects.create(date=date, start_time=time, end_time=end_time, reason=reason, assigned_doctor=doctor, patient=patient)
            appointment.save()
            return JsonResponse({'success': True})
        return JsonResponse({"success": False, 'errors': dict(form.errors.items())})


class ViewAppointments(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = 'Hospital_Management.view_appointment'
    queryset = models.Appointment.objects.all()
    template_name = 'appointment_templates/appointments.html'
    context_object_name = 'appointments'

    def get_context_data(self, *args, **kwargs):
        context = super(ViewAppointments, self).get_context_data(*args, **kwargs)
        context['appointments'] = models.Appointment.objects.filter(date__gte=datetime.date.today())
        return context


class AppointmentDetailView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('Hospital_Management.delete_appointment', 'Hospital_Management.view_appointment', 'Hospital_Management.change_appointment')
    model = models.Appointment
    form_class = AppointmentForm

    def get(self, request, appointment_id):
        appointment = get_object_or_404(models.Appointment, pk=appointment_id)
        data = {
            'date': appointment.date,
            'status': appointment.get_status_display(),
            'patientName': f'{str(appointment.patient)}',
            'patientId': appointment.patient_id,
            'time': appointment.start_time,
            'end_time': appointment.end_time,
            'doctor': f'{str(appointment.assigned_doctor)}',
            'doctor_id': appointment.assigned_doctor.pk,
            'reason': appointment.reason,
        }
        return JsonResponse(data)

    def delete(self, request, appointment_id):
        appointment = get_object_or_404(models.Appointment, pk=appointment_id)
        appointment.delete()
        return JsonResponse({'success': 'Deleted'})

    def put(self, request, appointment_id):
        appointment = get_object_or_404(models.Appointment, pk=appointment_id)
        query_string = request.body.decode('utf-8')
        data = QueryDict(query_string)
        if 'status' in data:
            form = DoctorAppForm(data, instance=appointment)
        else:
            form = AppointmentForm(data, instance=appointment)

        if form.is_valid():

            existing_appointments = models.Appointment.objects.filter(
                assigned_doctor=appointment.assigned_doctor,
                date=appointment.date
            ).exclude(pk=appointment.pk)
            print('here')

            for existing_appointment in existing_appointments:
                if appointment.start_time < existing_appointment.end_time and \
                        appointment.end_time > existing_appointment.start_time:
                    error_message = "The appointment conflicts with another appointment."
                    form.add_error('start_time', ValidationError(error_message))
                    return super().form_invalid(form)

            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({"success": False, 'errors': dict(form.errors.items())})

    def delete(self, *args, **kwargs):
        appointment = get_object_or_404(models.Appointment, pk=kwargs['appointment_id'])
        if appointment:
            appointment.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, 'errors': 'Appointment Doesnt Exist'})


class MyAppointments(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.view_appointment',)
    template_name = 'patient_templates/patientAppointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        qs = models.Appointment.objects.filter(patient__patient=self.request.user)
        return qs


    def delete(self, request, pk):
        appointment = get_object_or_404(models.Appointment, pk=pk)
        appointment.delete()
        return JsonResponse({'success': 'Deleted'})


class NewPatient(LoginRequiredMixin, PermissionRequiredMixin, generic.edit.CreateView):
    permission_required = ('Hospital_Management.add_patient', )
    model = models.PatientDetails
    template_name = 'patient_templates/new-patient-form.html'
    context_object_name = 'patients'
    form_class = PatientForm
    success_url = reverse_lazy('ReceptionistDashBoard')


    def form_valid(self, form):
        form.save(commit=False)
        # a simple constraint that checks if the person that created the PatientDetails object is a user
        # if the person is a patient then it must be the patient that created it
        if has_group(self.request.user, 'Patients'):
            self.model.patient = self.request.user
            form.save()
            return JsonResponse({'success':True})
        form.save()
        return JsonResponse({'success':True})



class Patients(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.view_patient', )
    model = models.PatientDetails
    template_name = 'patient_templates/patients.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Patients, self).get_context_data(*args, **kwargs)
        context['patients'] = self.model.objects.all()
        return context


class AvailableDoctors(LoginRequiredMixin, generic.ListView):
    model = models.Schedule

    def get(self, request, *args, **kwargs):
        if kwargs.get('date'):
            # -1 because the date in the database has been modeled as a python date
            # meaning that first day of the week is monday vs javascript firstday of the week is sunday
            doctors = models.Schedule.objects.filter(day_of_the_week=int(kwargs['date'])-1,
                                                     start_time__lte=kwargs['start_time'],
                                                 end_time__gt=kwargs['end_time'])
        context = {}
        if doctors:
            print(doctors)
            for doctor in doctors:
                context[doctor.staff.staff.id] = str(doctor.staff)
            return JsonResponse(context)
        return JsonResponse({'error': 'No such doctor'})


class PatientDetail(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView, generic.DetailView, generic.UpdateView):
    permission_required = ('Hospital_Management.add_patient', 'Hospital_Management.view_patient', 'Hospital_Management.change_patient')
    model = models.PatientDetails
    form_class = PatientForm
    template_name = 'patient_templates/new-patient-form.html'

    def get(self, request, *args, **kwargs):
        patient = models.PatientDetails.objects.get(patient_id=kwargs['pk'])
        appointment = models.Appointment.objects.filter(patient_id=kwargs['pk'])
        context = {
            'id': patient.patient.id,
            'bloodType': patient.blood_type,
            'name': f'{patient.patient.firstname} {patient.patient.lastname}',
            'symptoms': patient.symptoms,
            'weight': patient.weight,
            'height': patient.height,
            'age': patient.age,
            'firstname': patient.patient.firstname,
            'lastname': patient.patient.lastname,
            'mobile': patient.mobile,
            'blood_type': patient.blood_type,
            'address': patient.address,
        }

        for i in appointment:
            context['start_time'] = i.start_time
            context['end_time'] = i.end_time
            context['reason'] = i.reason
            context['status'] = i.get_status_display()
            context['doctor'] = f'{i.assigned_doctor.name.staff.firstname} {i.assigned_doctor.name.staff.lastname}'

        return JsonResponse(context)

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success':True})

    def form_invalid(self, form):
        return JsonResponse({"success":False, "errors" : dict(form.errors)})


class AppointmentHistory(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.view_appointment', )
    template_name = 'appointment_templates/appointmentHistory.html'
    context_object_name = 'appointment_history'

    def get_queryset(self):
        qs = models.Appointment.objects.filter(patient_id=self.kwargs['pk'])
        return qs

class UpcomingAppointments(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.view_appointment', )
    template_name = 'appointment_templates/upcomingAppointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = self.request.user
        qs = models.Appointment.objects.filter(Q(patient__patient=user) | Q(assigned_doctor__name__staff=user))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpcomingAppointments, self).get_context_data(**kwargs)
        context['date'] = datetime.date.today()
        return context



class DoctorDashBoard(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.add_admitted_patient', )
    model = models.Doctor
    context_object_name = 'doctor'
    template_name = 'dashboards/DoctorDashBoard.html'


class DoctorAppointments(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('Hospital_Management.add_admitted_patient', )
    model = models.Appointment
    context_object_name = 'appointments'
    template_name = 'doctor_templates/doctorAppointments.html'

    def get_queryset(self):
        qs = models.Appointment.objects.filter(assigned_doctor=self.request.user.id)
        return qs



class DoctorPatients(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    permission_required = ('')
    context_object_name = 'patients'
    template_name = 'doctor_templates/doctorPatients.html'

    def get_queryset(self):
        qs = models.AdmittedPatient.objects.filter(assigned_doctor__name__staff=self.request.user)
        return qs



class PatientDashboard(generic.ListView):
    context_object_name = 'patient'
    template_name = 'dashboards/PatientDashBoard.html'
    model = models.PatientDetails


def appointment_filter(request):
    appointments = Appointment.objects.all()
    filter_form = AppointmentFilterForm(request.GET or None)

    if filter_form.is_valid():
        date = filter_form.cleaned_data['date']
        time = filter_form.cleaned_data['time']
        end_time = filter_form.cleaned_data['end_time']
        status = filter_form.cleaned_data['status']
        doctor = filter_form.cleaned_data['doctor']
        reason = filter_form.cleaned_data['reason']

        # Filter appointments based on form inputs
        if date:
            appointments = appointments.filter(date=date)
        if time:
            appointments = appointments.filter(start_time__gte=time)
        if end_time:
            appointments = appointments.filter(end_time__lte=end_time)
        if status:
            appointments = appointments.filter(status=status)
        if doctor:
            appointments = appointments.filter(doctor=doctor)
        if reason:
            appointments = appointments.filter(Q(reason__icontains=reason) | Q(diagnosis__icontains=reason))

    context = {
        'appointments': appointments,
        'filter_form': filter_form
    }

    return render(request, 'appointments/appointmentHistory.html', context)


class MyAppointmentRecord(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    context_object_name = 'patient'
    template_name = 'patient_templates/myrecord.html'
    context_object_name = 'appointment_history'

    def test_func(self):
        if models.PatientDetails.objects.filter(patient=self.request.user):
            return True
        return False

    def get_queryset(self):
        qs = models.Appointment.objects.filter(patient__patient=self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MyAppointmentRecord, self).get_context_data(**kwargs)
        context['filter_form'] = AppointmentFilterForm
        return context


class PatientRecord(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    context_object_name = 'patient'
    template_name = 'patient_templates/patientRecord.html'

    def test_func(self):
        if models.PatientDetails.objects.filter(patient=self.request.user):
            return True
        return False

    def get_queryset(self):
        qs = models.PatientDetails.objects.get(patient=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super(PatientRecord, self).get_context_data(**kwargs)
        # fetch the appointment history of a the user requesting details
        context['history'] = models.Appointment.objects.filter(patient__patient=self.request.user)
        return context

