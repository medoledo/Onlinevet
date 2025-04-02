from django.db import models

class PetType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Owner(models.Model):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Not clear', 'Not clear'),
    ]

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    pet_name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)  # Change to CASCADE
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    
    def __str__(self):
        return f"{self.name} - {self.pet_name}"
