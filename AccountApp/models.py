from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    pass


class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Doctor(User):
    licence_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            MinLengthValidator(6),
            MaxLengthValidator(6)
        ]
    )

    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    specialities = models.ManyToManyField(
        Speciality,
        related_name="doctors"
    )

    def __str__(self):
        return self.username


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le numéro national ne respecte pas le pattern : 8 chiffres."
            )
        ]
    )

    phone = models.CharField(max_length=8)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.birth_date and self.birth_date > timezone.localdate():
            raise ValidationError({
                'birth_date': "La date de naissance ne peut pas être dans le futur."
            })

    def __str__(self):
        return self.username


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    appointment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'patient', 'appointment_date'],
                name='unique_patient_doctor_date',
                violation_error_message="Ce docteur possède déjà un rendez-vous avec ce patient à cette date."
            )
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"