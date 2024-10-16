from django.db import models
from gestion_utilisateur.models import Etudiant, Enseignant

class Evaluation(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    date_evaluation = models.DateTimeField(auto_now_add=True)
    heure_evaluation = models.TimeField(auto_now_add=True)  # Heure de l'évaluation
    note = models.IntegerField()  # Note entière
    commentaire = models.TextField(null=True, blank=True)  # Commentaire optionnel

    def __str__(self):
        return f"Évaluation de {self.etudiant} par {self.enseignant} le {self.date_evaluation.strftime('%Y-%m-%d %H:%M:%S')}"
