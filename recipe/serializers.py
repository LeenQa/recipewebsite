from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

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
    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredient_list = serializers.ListField(write_only=True)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredient_list')
        # list = []
        # for ingredient in ingredients:
        #     list.append(Ingredient.objects.get(pk=ingredient))
        validated_data['ingredients'].add(ingredients)
        recipe = super(RecipeSerializer, self).create(validated_data)
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
