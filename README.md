# Hospital-Management-App


Hospital Management App is a Django web application that allows users to schedule appointments with doctors online. It provides a platform for both doctors and patients to manage their appointments, medical records, and prescriptions.
# Introduction:

Welcome to our Django-based healthcare management system. This system aims to simplify the process of managing patients, appointments, and medical records for healthcare providers. It provides a user-friendly interface for patients and healthcare providers to communicate and manage their healthcare needs.

 # Features:

- User registration and authentication: Patients can register and create their profiles, and healthcare providers can register and create their profiles. The system automatically assigns patients to the patient group.
- Chat feature for doctors and patients.
- Appointment scheduling: Patients can schedule appointments with healthcare providers, and healthcare providers can manage their schedules and appointments.
- Medical records management: Healthcare providers can manage medical records for their patients, including prescriptions, test results, and treatment plans.
- Admin panel: Admins can manage the system's settings, create and manage users, and view system logs.
- Doctor management and schedule management.
- Data seeding: The system comes with pre-defined data, including groups and default users, to simplify the setup process.
# Getting started:

To use this system, you will need to have Python and Django installed on your machine. Once you have installed Django, clone the repository to your local machine and navigate to the project directory. Next, create a virtual environment, activate it, and install the project's requirements using pip.


Prescription management.

# Getting Started
- Clone the repository: git clone https://github.com/t-ega/Hospital-Management-App.git- 
- Install dependencies: pip install -r requirements.txt
- Run migrations: python manage.py migrate
- Create a superuser: python manage.py createsuperuser
- Load default data: python manage.py loaddata initial
- Start the server: daphne Hospital_Management_App.asgi:application * For the chattting feature to work
# Usage
Logging In
- To log in as a patient, go to /accounts/login/ and enter your credentials.
- Staff members can only be created by the admin
# Scheduling an Appointment
- After logging in, select the Appointments tab.
- Click on New Appointment.
- Fill in the details for the appointment and click Save.
# Note: This process assumes that you are a patient.
# Viewing Appointments
- After logging in, select the Appointments tab.
- View your upcoming appointments or past appointments.
# Managing Patients
- After logging in as a doctor, select the Patients tab.
- View all patients and their medical records.
- Add new patients and update existing ones.
# Chatting
- After logging in as a doctor or patient, select the Chat tab.
- Select a user to chat with by clicking on the '+' icon located at the top right corner and start chatting.
![Doctor Patient Chat](Screenshots/hospital%20management%20chat%20video.gif)

- 

# Screenshots
- Patient Home Screen
![Patients Home](Screenshots/patients%20home.png)
- Patient Records Screen
![Patients Records](Screenshots/patients%20records.png)
- Patient Can Create An Appointment With A Doctor Based On Their Availability
![Patients Appointments](Screenshots/patients%20appointments.png)
- Patient Can Add Their Medical Details
![Patients Add Details](Screenshots/patients%20add%20details.png)
- Patient trying to create an appointment without registering their medical condition
![Patients Create Apppointment Warning](Screenshots/patients%20create%20apppointment%20warning.png)
- Patient appointment before filling appointment details
![Patients Create Apppointment Before](Screenshots/patients%20create%20apppointment%20before.png)
- Patient Appointment after filling appointment details
![Patients Create Apppointment After](Screenshots/patients%20create%20apppointment%20after.png)
- Appointment successfully created
![Patients Create Apppointment Completed](Screenshots/patients%20create%20apppointment%20completed.png)
- Patient can edit their appointment time and date after they have created it 
![Patients Edit Appointment](Screenshots/patients%20edit%20appointment.png)
- Patient After Appointment has been approved
![Patients Approved Apointment](Screenshots/patients%20approved%20apointment.png)
- Doctor home screen
![Doctor Home Page](Screenshots/doctor%20home.png)
- Doctor can approve/reject/confrim appointment for patients
![Doctor Approve Appointment](Screenshots/doctor%20approve%20appointment.png)
- Doctor chat with Patient
![Doctor Chat With Patient](Screenshots/doctor%20chat%20with%20patient.png)
 - Patient can chat with their doctor they have been assigned to for appointmne
![Patient Chat With Doctor](Screenshots/patient%20chat%20with%20doctor.png)


# Contributing
If you'd like to contribute to Hospital Management App, please fork the repository.
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
# Authors
Akpojiyovwi Tega

License
This project is licensed under the MIT License - see the LICENSE.md file for details.
