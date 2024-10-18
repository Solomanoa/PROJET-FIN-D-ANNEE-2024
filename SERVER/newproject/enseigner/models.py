from django.db import models
from gestion_utilisateur.models import Etudiant, Enseignant

class Enseigner(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    etudiants = models.ManyToManyField(Etudiant)

    def __str__(self):
        niveaux_list = ', '.join(set([etudiant.niveau for etudiant in self.etudiants.all()]))
        return f"{self.enseignant.nom} enseigne aux niveaux : {niveaux_list}"
