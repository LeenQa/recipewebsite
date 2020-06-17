from django.conf.urls import url
from . import views

app_name='recipe'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)', views.DetailView.as_view(), name='details'),
    url(r'recipe/add/$', views.RecipeCreate.as_view(), name='recipe-add'),
    url(r'ingredient/add/$', views.IngredientCreate.as_view(), name='ingredient-add')
]