from django.db import models
from owners.models import Owner , PetType



class Visit(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    sex = models.CharField(max_length=10)
    age = models.FloatField()
    weight_in_kg = models.FloatField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    visit_date = models.DateField()
    next_check_date = models.DateField()

    def __str__(self):
        return f"{self.owner.name} - {self.visit_date}"
