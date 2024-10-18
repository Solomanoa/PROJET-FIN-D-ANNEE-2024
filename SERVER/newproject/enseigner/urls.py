from django.urls import path
from .views import (
    get_enseignements,
    get_enseignement,
    create_enseignement,
    update_enseignement,
    delete_enseignement,
)

urlpatterns = [
    path('enseignements/', get_enseignements, name='get_enseignements'),  # Récupérer toutes les associations
    path('enseignements/<int:id>/', get_enseignement, name='get_enseignement'),  # Récupérer une association par ID
    path('enseignements/create/', create_enseignement, name='create_enseignement'),  # Créer une nouvelle association
    path('enseignements/update/<int:id>/', update_enseignement, name='update_enseignement'),  # Mettre à jour une association
    path('enseignements/delete/<int:id>/', delete_enseignement, name='delete_enseignement'),  # Supprimer une association
]
