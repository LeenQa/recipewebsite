from django.conf.urls import url
from . import views
from .views import IngredientsView

app_name='recipe'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)', views.DetailView.as_view(), name='details'),
    url(r'recipe/add/$', views.RecipeCreate.as_view(), name='recipe-add'),
    url(r'ingredient/add/$', views.IngredientCreate.as_view(), name='ingredient-add'),
    url(r'ingredients/(?P<pk>[0-9]+)/', views.ingredient_detail),
    url(r'ingredients/$', IngredientsView.as_view()),

]