from django.db import models
from gestion_utilisateur.models import Etudiant, Enseignant

class Enseigner(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    niveau = models.CharField(
        max_length=20,
        choices=[
            ('L1', 'L1'),
            ('L2', 'L2'),
            ('L3', 'L3'),
            ('M1', 'M1'),
            ('M2', 'M2'),
        ]
    )

    def __str__(self):
        return f"{self.enseignant.utilisateur.nom} enseigne au niveau {self.niveau}"