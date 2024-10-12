from django.urls import path
from .views import (
    get_utilisateurs,
    create_utilisateur,
    get_utilisateur,
    update_utilisateur,
    delete_utilisateur,
    authenticate_face,
)

urlpatterns = [
    path('utilisateurs/', get_utilisateurs, name='get_utilisateurs'),  # Récupérer tous les utilisateurs
    path('utilisateurs/<int:id>/', get_utilisateur, name='get_utilisateur'),  # Récupérer un utilisateur par ID
    path('utilisateurs/create/', create_utilisateur, name='create_utilisateur'),  # Créer un nouvel utilisateur
    path('utilisateurs/update/<int:id>/', update_utilisateur, name='update_utilisateur'),  # Mettre à jour un utilisateur
    path('utilisateurs/delete/<int:id>/', delete_utilisateur, name='delete_utilisateur'),  # Supprimer un utilisateur
    path('authenticate-face/', authenticate_face, name='authenticate_face'),  # Route d'authentification faciale
]
