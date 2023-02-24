from django import template
from Hospital_Management.models import PatientDetails

register = template.Library()

# registers the filter ('has_group') inside the templates rendered
# so that we can check if the user belongs to a particular group


@register.filter(name='get_patient')
def get_patient(user,):
    if PatientDetails.objects.filter(patient=user).exists():
        return True
    return False
