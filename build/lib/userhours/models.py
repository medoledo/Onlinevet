from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class UserHours(models.Model):
    # Reference the UserProfile model
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    arrival_time = models.DateTimeField()
    left_time = models.DateTimeField()
    total_hours = models.FloatField()  # Make it editable

    def __str__(self):
        return f"{self.user.name} - {self.total_hours} hrs"
