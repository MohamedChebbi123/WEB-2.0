from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import identify_hasher
from AppointmentApp.models import Appointment
from .models import User, Specialty, Doctor, Patient


class AppointmentInline(admin.StackedInline):
    """Appointments shown inside the Doctor page (Appointment has a FK to Doctor)."""
    model = Appointment
    extra = 0
    fields = ("patient", "appointment_date", "duration_minutes", "status", "reason")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class BaseProfileAdmin(admin.ModelAdmin):
    """Hashes the password when it is set from the admin form."""
    identifier_field = None

    def get_readonly_fields(self, request, obj=None):
        # Business identifiers cannot be modified after creation
        readonly = list(super().get_readonly_fields(request, obj))
        if obj is not None:
            readonly.append(self.identifier_field)
        return readonly

    def save_model(self, request, obj, form, change):
        raw = form.cleaned_data.get("password")
        if raw:
            try:
                identify_hasher(raw)  # already hashed -> leave as is
            except ValueError:
                obj.set_password(raw)
        super().save_model(request, obj, form, change)


@admin.register(Doctor)
class DoctorPerso(BaseProfileAdmin):
    identifier_field = "license_number"
    fields = ("username", "password", "first_name", "last_name", "email",
              "license_number", "phone", "specialties")
    list_display = ("username", "first_name", "last_name", "license_number", "phone")
    search_fields = ("username", "last_name", "license_number")
    filter_horizontal = ("specialties",)
    inlines = [AppointmentInline]


@admin.register(Patient)
class PatientAdmin(BaseProfileAdmin):
    identifier_field = "national_id"
    fields = ("username", "password", "first_name", "last_name", "email",
              "national_id", "phone", "birth_date")
    list_display = ("username", "first_name", "last_name", "national_id", "birth_date")
    search_fields = ("username", "last_name", "national_id")
