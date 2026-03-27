from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    CAR_TYPES = [('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Wagon', 'Wagon')]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='Sedan')
    year = models.IntegerField(default=2023, validators=[MaxValueValidator(2023), MinValueValidator(2015)])
    def __str__(self):
        return self.car_make.name + " " + self.name
