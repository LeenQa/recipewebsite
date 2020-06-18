from rest_framework import serializers
from .models import Recipe, Ingredient, DIFFICULTY, TYPE


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'ingredient_type', 'is_organic']
