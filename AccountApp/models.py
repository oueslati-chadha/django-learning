import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class user(AbstractUser):
   pass

class doctor(user):
    phone=models.CharField(max_length=8)
    licence_number=models.CharField(max_length=6,unique=True)
    specialities= models.ManyToManyField('Speciality', related_name='doctors',null=True,blank=True)

def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )

class patient(user):
    phone=models.CharField(max_length=8,validators=[RegexValidator(r'^\d{8}$',message="Le téléphone doit contenir exactement 8 chiffres.")]
    )

    #birth_date=models.DateField(validators=[validate_past_date])
    
    #Methode 2:
    birth_date = models.DateField()

    national_id=models.CharField(max_length=8,unique=True, 
    validators=[
        RegexValidator(r'^\d{8}$',message="La CIN doit contenir exactement 8 chiffres.")
    ]
    )

    def clean(self):
        super().clean()
        
        if self.birth_date and self.birth_date >= timezone.localdate():
            raise ValidationError({
            'birth_date': "La date de naissance doit être antérieure à aujourd'hui."
        })


class Speciality(models.Model):
    name = models.CharField(max_length=100)
