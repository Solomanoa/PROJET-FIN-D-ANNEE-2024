from django.db import models
from django.utils import timezone
from gestion_utilisateur.models import ResponsablePedagogique, Enseignant

class Recommendation(models.Model):
    responsable = models.ForeignKey(ResponsablePedagogique, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    recommandation = models.TextField()  # Champ pour la recommandation
    date_recommendation = models.DateTimeField(default=timezone.now)  # Date de création

    def __str__(self):
        return f"Recommandation de {self.responsable} pour {self.enseignant}"
