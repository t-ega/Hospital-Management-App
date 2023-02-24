from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('accounts/signup/', Register.as_view(), name='signup'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/logout/', Logout.as_view(), name='logout'),
    path('receptionist/', ReceptionistDashBoard.as_view(), name='ReceptionistDashBoard'),
    path('create-appointment/', CreateAppointment.as_view(), name='create-appointment'),
    path('patients/', Patients.as_view(), name='patients'),
    path('doctor/', DoctorDashBoard.as_view(), name='DoctorDashBoard'),
    path('patient-dashboard/', PatientDashboard.as_view(), name='patientDashboard'),
    path('my-records/', MyAppointmentRecord.as_view(), name='my-records'),
    path('filter-appointments/', appointment_filter, name='appointment_filter'),
    path('my-appointments/', MyAppointments.as_view(), name='my-appointments'),
    path('my-upcoming-appointments/', UpcomingAppointments.as_view(), name='upcoming-appointments'),
    path('my-appointments/delete/<int:pk>/', MyAppointments.as_view(), name='my-appointments'),
    path('patient/<int:pk>/', PatientDetail.as_view(), name='patient-detail'),
    path('new-patient/', NewPatient.as_view(), name='new-patient'),
    path('appointment-history/<int:pk>/', AppointmentHistory.as_view(), name='appointment-history'),
    path('appointments/', ViewAppointments.as_view(), name='view-appointments'),
    path('appointment/<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment_detail'),
    path('available-doctors/', AvailableDoctors.as_view(), name='available-doctors'),
    path('doctor/appointments/', DoctorAppointments.as_view(), name='doctor-appointments'),
    path('doctor/appointments/<int:pk>/', DoctorAppointments.as_view(), name='doctor-appointments'),
    path('doctor/patients/', DoctorPatients.as_view(), name='doctor-patients'),
    path('available-doctors/<str:date>/<str:start_time>/<str:end_time>/',  AvailableDoctors.as_view(), name='available-doctors')

]
