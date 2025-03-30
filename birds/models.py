from django.db import models

class Birddailyprice(models.Model):
    bird_type = models.CharField(max_length=50, unique=True)
    bird_price = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update all birds that have this bird type
        for bird in Bird.objects.filter(bird_type=self):
            bird.price = self.bird_price
            bird.total = bird.quantity * bird.price
            bird.remaining_to_pay = bird.total - bird.payed_money
            bird.save()

class Bird(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    
    bird_type = models.ForeignKey(Birddailyprice, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    payed_money = models.FloatField()
    total = models.FloatField()
    remaining_to_pay = models.FloatField()
    date_of_payment = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Fetch price from Birddailyprice and update calculations
        self.price = self.bird_type.bird_price
        self.total = self.quantity * self.price
        self.remaining_to_pay = self.total - self.payed_money
        super().save(*args, **kwargs)
        
        
class DoneBird(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    bird_type = models.ForeignKey(Birddailyprice, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    payed_money = models.FloatField()
    total = models.FloatField()
    remaining_to_pay = models.FloatField()
    date_of_payment = models.DateField(auto_now_add=True)
    done_date = models.DateField(auto_now_add=True)  # This automatically sets the date when the bird is marked as done

    def save(self, *args, **kwargs):
        # Calculate total and remaining to pay before saving
        self.total = self.quantity * self.price
        self.remaining_to_pay = self.total - self.payed_money
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.bird_type.bird_type}"