from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


phone_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le numéro de téléphone doit contenir exactement 8 chiffres."
)


def validate_past_date(value):
    """La date doit être strictement antérieure à aujourd'hui."""
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à la date du jour.")


class User(AbstractUser):
    pass


class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )
    phone = models.CharField(max_length=8, validators=[phone_validator])
    specialties = models.ManyToManyField(
        Specialty,
        related_name="doctors",
        blank=True
    )

    class Meta:
        verbose_name = "Médecin"
        verbose_name_plural = "Médecins"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}".strip()


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le numéro de CIN doit contenir exactement 8 chiffres."
            )
        ]
    )
    phone = models.CharField(max_length=8, validators=[phone_validator])
    birth_date = models.DateField(validators=[validate_past_date])

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()
