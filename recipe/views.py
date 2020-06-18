from rest_framework.views import APIView

from recipe.models import Recipe, Ingredient
from django.views import generic
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import IngredientSerializer
from rest_framework.response import Response


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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['ingredient_list'] = Ingredient.objects.all()
        return context


class IngredientCreate(CreateView):
    model = Ingredient
    fields = ['name', 'ingredient_type', 'is_organic']


@csrf_exempt
def ingredient_list(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def ingredient_detail(request, pk):
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = IngredientSerializer(ingredient)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = IngredientSerializer(ingredient, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        ingredient.delete()
        return HttpResponse(status=204)


class IngredientsView(APIView):
    def get(self, request):
        ingredients =Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response({"ingredients": serializer.data})

    def post(self, request):
        ingredient = request.data.get('ingredient')

        serializer = IngredientSerializer(data=ingredient)
        if serializer.is_valid(raise_exception=True):
            save_ingredient = serializer.save()

        return Response({"success":f"ingrediet '{ ingredient.name}' created successfuly"})