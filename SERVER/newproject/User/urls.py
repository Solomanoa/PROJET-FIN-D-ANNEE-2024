from django.urls import path
from django.conf import settings
from .views import get_users, create_user
from django.conf.urls.static import static

urlpatterns = [
    path('list/', get_users, name='get_users'),  # URL pour obtenir la liste des utilisateurs
    path('register/', create_user, name='create_user'),  # URL pour enregistrer un nouvel utilisateur
]

if settings.DEBUG:  # Serve les fichiers médias pendant le développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)