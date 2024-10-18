from django.db import models
from gestion_utilisateur.models import Etudiant, Enseignant

class Evaluation(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    date_evaluation = models.DateField(auto_now_add=True)
    heure_evaluation = models.TimeField(auto_now_add=True)
    maitrise_sujet=  models.IntegerField(default=0) 
    clarte_explicative= models.IntegerField(default=0)
    interaction_apprenant= models.IntegerField(default=0)
    qualite_support= models.IntegerField(default=0)
    gestion_temps= models.IntegerField(default=0)
    note = models.IntegerField()  # Note entière
    commentaire = models.TextField(null=True, blank=True)  # Commentaire optionnel

    def __str__(self):
        return f"Évaluation de {self.etudiant} par {self.enseignant} le {self.date_evaluation.strftime('%Y-%m-%d %H:%M:%S')}"
