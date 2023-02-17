from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class FoodList(models.Model):
    category = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Food Lists'

    def get_absolute_url(self):
        return reverse('calorie_tracker:show_food_lists', args=[self.slug])

    def __str__(self):
        return self.category


class FoodItem(models.Model):
    type_item = models.ForeignKey(FoodList, related_name='food_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    calories = models.IntegerField()
    proteins = models.FloatField()
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    serving_size = models.FloatField()
    serving_unit = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'FoodItems'

    def get_absolute_url(self):
        return reverse('calorie_tracker:food_item_detail')

    def __str__(self):
        return self.name
