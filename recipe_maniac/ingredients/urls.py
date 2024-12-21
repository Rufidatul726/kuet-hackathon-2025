from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("ingredients", views.IngredientViewSet)
router.register("recipe", views.RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
