from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Modèle principal Utilisateur
class Utilisateur(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    pseudo = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    matricule = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    empreinte_digitale = models.BinaryField(null=True, blank=True)

    type = models.CharField(max_length=20, choices=[
        ('admin', 'Administrateur'),
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
        ('responsable', 'Responsable Pédagogique'),
    ])
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'type']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"

# Sous-classe Etudiant
class Etudiant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    carte_etudiant = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f"Étudiant : {self.utilisateur.nom} {self.utilisateur.prenom}"

# Sous-classe Enseignant
class Enseignant(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=20)

    def __str__(self):
        return f"Enseignant : {self.utilisateur.nom} {self.utilisateur.prenom}"

# Sous-classe Administrateur
class Administrateur(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Administrateur : {self.utilisateur.nom} {self.utilisateur.prenom}"

# Sous-classe Responsable Pédagogique
class ResponsablePedagogique(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    def __str__(self):
        return f"Responsable Pédagogique : {self.utilisateur.nom} {self.utilisateur.prenom}"
