from django.urls import path
from .views import (
    get_recommendations,
    get_recommendation,
    create_recommendation,
    update_recommendation,
    delete_recommendation,
)

urlpatterns = [
    path('recommendations/', get_recommendations, name='get_recommendations'),  # Récupérer toutes les recommandations
    path('recommendations/<int:id>/', get_recommendation, name='get_recommendation'),  # Récupérer une recommandation par ID
    path('recommendations/create/', create_recommendation, name='create_recommendation'),  # Créer une nouvelle recommandation
    path('recommendations/update/<int:id>/', update_recommendation, name='update_recommendation'),  # Mettre à jour une recommandation par ID
    path('recommendations/delete/<int:id>/', delete_recommendation, name='delete_recommendation'),  # Supprimer une recommandation par ID
]
