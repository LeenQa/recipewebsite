from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    TYPE = (
        ('Vegetables', 'veg'),
        ('Fruits', 'fruit'),
        ('Grains, Beans and Nuts', 'grain'),
        ('Meat and Poultry', 'meat'),
        ('Fish and Seafood', 'seafood'),
        ('Dairy Foods', 'dairy'),
    )
    name = models.CharField(max_length=250)
    ingredient_type = models.CharField(max_length=50, choices=TYPE)
    is_organic = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('recipe:index')


class Recipe(models.Model):
    DIFFICULTY = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    name = models.CharField(max_length=250)
    duration = models.CharField(max_length=250)
    ingredients = models.ManyToManyField(Ingredient)
    recipe_image = models.FileField()
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY)

    def __str__(self):
        return f"recipe name: {self.name}, duration: {self.duration}"

    def get_absolute_url(self):
        return reverse('recipe:details', kwargs={'pk': self.pk})
