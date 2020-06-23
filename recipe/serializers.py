from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Recipe, Ingredient
import re


class IngredientSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_name(self, value):
        r = re.compile('^[a-zA-Z ]*$')
        if not (r.match(value) is not None):
            raise serializers.ValidationError("ingredient name can only contain alphabets")
        return value

    class Meta:
        model = Ingredient
        fields = ['name',
                  'ingredient_type',
                  'is_organic',
                  'user']


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    name = serializers.CharField(
        max_length=250,
        validators=[
            RegexValidator(
                regex='^[a-zA-Z ]*$',
                message='recipe name can only contain alphabets',
                code='invalid_username'
            ),
        ]
    )
    duration = serializers.CharField(
        max_length=250,
        validators=[
            RegexValidator(
                regex='\\b(minute|hour|day)',
                message='You must specify duration in minutes/hours/days',
                code='invalid_duration'
            ),
        ]
    )

    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_list = serializers.ListField(write_only=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient_list')
        recipe = super(RecipeSerializer, self).create(validated_data)
        recipe.ingredients.set(ingredients)
        return recipe

    class Meta:
        model = Recipe
        fields = ['name',
                  'duration',
                  'ingredients',
                  'recipe_image',
                  'difficulty',
                  'ingredient_list',
                  'user']


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password',
                  'confirm_password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def save(self):

        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        if password != confirm_password:
            print("passwords don't match.")
            raise serializers.ValidationError({"password": "passwords must match."})
        else:
            user = User(
                email=self.validated_data['email'],
                username=self.validated_data['username'],
            )
            user.set_password(password)
            user.save()
            return user
