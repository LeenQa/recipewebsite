from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from django.views import generic
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .permissions import IsLoggedUser
import django_filters.rest_framework


class IndexView(generic.ListView):  # a view for the index page
    template_name = 'recipe/index.html'

    def get_queryset(self):
        return Recipe.objects.all()


class DetailView(generic.DetailView):  # a view for the details of a recipe
    model = Recipe
    template_name = 'recipe/details.html'


"""
class RecipeCreate(CreateView):  # a view for creating a new recipe
    model = Recipe
    fields = ['name', 'duration', 'ingredients', 'recipe_image', 'difficulty']

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['ingredient_list'] = Ingredient.objects.all()
        return context
"""


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsLoggedUser)
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name',
                        'ingredient_type',
                        'is_organic']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsLoggedUser)
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name',
                        'duration',
                        'ingredients',
                        'recipe_image',
                        'difficulty',
                        'ingredient_list']
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'recipe': self.object}, template_name='index.html')