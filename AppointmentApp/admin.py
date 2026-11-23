from django.contrib import admin
from .models import Appointment


@admin.action(description="Make them confirmed")
def confirm_appointments(modeladmin, request, queryset):
    updated = queryset.update(status=Appointment.Status.CONFIRMED)
    modeladmin.message_user(request, f"{updated} rendez-vous confirmé(s).")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    actions = [confirm_appointments]
    list_display = ("appointment_date", "doctor", "patient", "status", "duration_minutes")
    list_filter = ("status", "doctor")
    search_fields = ("reason", "patient__last_name", "doctor__last_name")
    date_hierarchy = "appointment_date"
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informations du rendez-vous", {
            "fields": ("reason", "status"),
        }),
        ("Date et durée", {
            "fields": ("appointment_date", "duration_minutes"),
        }),
        ("Patient et médecin", {
            "fields": ("patient", "doctor"),
        }),
        ("Ordonnance", {
            "fields": ("prescription",),
        }),
        ("Planification", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
