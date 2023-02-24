from django.contrib.auth.models import Group


def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def base_template(request):
    user = request.user
    templates = {}

    if user.is_authenticated:
        """ a context_processor that can determine the type of user
            so that we can render a different templates based on different users"""
        if has_group(user, 'Admin'):
            templates['base'] = 'base/base.html'
            templates['home'] = 'doctordashboard.html'
        elif has_group(user, 'Receptionist'):
            templates['base'] = 'base/receptionistbase.html'
            templates['home'] = 'receptionistDashBoard.html'
        elif has_group(user, 'Patients'):
            templates['base'] = 'base/patientdashbase.html'
            templates['home'] = 'receptionistDashBoard.html'
        elif has_group(user, 'Doctors'):
            templates['base'] = 'base/doctordashbase.html'
            templates['home'] = 'receptionistDashBoard.html'

    # Return a default base template if the user type cannot be determined
    return {'templates': templates}
