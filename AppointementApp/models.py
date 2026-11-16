from django.db import models


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "En Attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    reason = models.TextField()

    prescription = models.FileField(
        blank=True,
        upload_to="prescription/"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    appointment_date = models.DateField()

    doctor = models.ForeignKey(
        "accountapp.Doctor",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    patient = models.ForeignKey(
        "accountapp.Patient",
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"