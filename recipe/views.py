from recipe.models import Recipe, Ingredient
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import View


class IndexView(generic.ListView):
    template_name = 'recipe/index.html'

    def get_queryset(self):
        return Recipe.objects.all()


class DetailView(generic.DetailView):
    model = Recipe
    template_name = 'recipe/details.html'


class RecipeCreate(CreateView):
    model = Recipe
    fields = ['name', 'duration', 'ingredients', 'recipe_image', 'difficulty']


class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['name', 'ingredient_type', 'is_organic']
