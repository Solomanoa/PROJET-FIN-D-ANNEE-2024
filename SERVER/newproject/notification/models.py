from django.db import models
from gestion_utilisateur.models import Utilisateur

class Notification(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)  # Indique si la notification a été lue ou non

    def __str__(self):
        return f"Notification pour {self.utilisateur.username}: {self.message[:20]}..."
