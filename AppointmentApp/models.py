from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    reason = models.TextField()
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    doctor = models.ForeignKey(
        "AccountApp.Doctor",
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    patient = models.ForeignKey(
        "AccountApp.Patient",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="Ce médecin a déjà un rendez-vous à cette date et heure."
            )
        ]

    def clean(self):
        super().clean()
        if not self.appointment_date:
            return
        # La règle s'applique à la création ou si la date a été modifiée :
        # un rendez-vous passé reste modifiable (ex. ajout de l'ordonnance).
        date_changed = self._state.adding or not Appointment.objects.filter(
            pk=self.pk, appointment_date=self.appointment_date
        ).exists()
        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError({
                "appointment_date": "La date du rendez-vous doit être postérieure à maintenant."
            })

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date:%d/%m/%Y %H:%M}"
