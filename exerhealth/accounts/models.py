from django.contrib.auth.models import User
from django.db import models


class FitnessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    goal = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def calculate_bmi(self):
        return self.weight / (self.height * self.height)



