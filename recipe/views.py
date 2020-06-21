from rest_framework import status
from rest_framework.views import APIView
from django.views import generic
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


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


@permission_classes((IsAuthenticated), )
class IngredientsView(APIView):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response({"ingredients": serializer.data})

    def post(self, request):
        ingredient = request.data.get('ingredient')
        serializer = IngredientSerializer(data=ingredient)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": f"ingredient '{ingredient['name']}' created successfully"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetail(APIView):
    def get_object(self, pk):
        try:
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    def put(self, request, pk):
        ingredient = self.get_object(pk)
        serializer = IngredientSerializer(ingredient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ingredient = self.get_object(pk)
        ingredient.delete()
        return Response({"success": f"ingredient Deleted successfully"})


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # if User.objects.filter(username=request.data['username']).exists():
        #    raise serializers.ValidationError({"username": "username already exists."})
        if serializer.is_valid():
            user = serializer.save()
            data = {}
            data['response'] = f"User {user.username} created successfully"
            data['username'] = user.username
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
