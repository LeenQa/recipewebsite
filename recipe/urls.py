from django.conf.urls import url
from rest_framework.generics import ListCreateAPIView
from rest_framework.routers import DefaultRouter
from django.urls import include

from . import views
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'recipe'

router = DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)', views.DetailView.as_view(), name='details'),
    url(r'login/$', obtain_auth_token, name="login"),
    url('', include(router.urls)),
]
