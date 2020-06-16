from django.db import models
from django.urls import reverse

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    ingredient_type = models.CharField(max_length=250)
    is_organic = models.BooleanField(False)

    def __str__(self):
        return f"{self.name}"


class Recipe(models.Model):
    DIFFICULTY = (
        ('Easy', 'E'),
        ('Medium', 'M'),
        ('Hard', 'H'),
    )
    name = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)
    ingredients = models.ManyToManyField(Ingredient)
    recipe_image = models.FileField()
    difficulty = models.CharField(max_length=50,choices=DIFFICULTY)

    def __str__(self):
        return f"recipe name: {self.name}, duration: {self.duration}"

    def get_absolute_url(self):
        return reverse('recipe:details', kwargs={'pk': self.pk})




