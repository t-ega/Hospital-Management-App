from django.contrib import admin
from .models import Staff, Doctor, StaffRank, Specialization, PatientDetails, AdmittedPatient, Bed, Appointment, Schedule
from django import forms

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin',)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email',  'is_admin', 'is_staff', 'firstname', 'lastname')
    list_filter = ('is_admin', 'groups',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'firstname',
                                    'lastname', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


# Now register the new UserAdmin...


class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff',)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name',)


class RankAdmin(admin.ModelAdmin):
    list_display = ('rank',)


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', )


class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient',)


class AdmittedPatientAdmin(admin.ModelAdmin):
    list_display = ('patient', 'admission_date', 'bed')


class BedAdmin(admin.ModelAdmin):
    list_display = ('in_use', )


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'status')


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff', 'day_of_the_week', 'start_time', 'end_time')


admin.site.register(User, UserAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Bed, BedAdmin)
admin.site.register(AdmittedPatient, AdmittedPatientAdmin)
admin.site.register(PatientDetails, PatientAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(StaffRank, RankAdmin)
admin.site.register(Specialization, SpecializationAdmin)
