from django.db import models
from django.contrib.auth.models import User

# Modèle de la session de cours
class SessionCours(models.Model):
    heure_ouverture = models.DateTimeField()  # Champ pour stocker l'heure d'ouverture de la session
    heure_fermeture = models.DateTimeField()  # Champ pour stocker l'heure de fermeture de la session
    statut = models.CharField(max_length=255)  # Champ pour stocker le statut de la session
    formateur = models.ForeignKey(User, on_delete=models.CASCADE)  
    formulaire_url = models.URLField()  # Champ pour stocker l'URL du formulaire associé à la session

# Modèle pour enregistrer les réponses aux formulaires pour chaque session
class FormulaireSession(models.Model):
    session_id = models.IntegerField()  # Champ pour stocker l'ID de la session associée
    avancement = models.IntegerField()  # Champ pour stocker l'avancement de la session
    difficulte = models.CharField(max_length=50)  # Champ pour stocker le niveau de difficulté de la session
    progression = models.CharField(max_length=50)  # Champ pour stocker la progression de la session
    moyenne = models.CharField(max_length=50)  # Champ pour stocker la moyenne
    username = models.CharField(max_length=50)  # Champ pour stocker le nom d'utilisateur associé

    class Meta:
        managed = False  # Indique à Django de ne pas gérer cette table car elle existe déjà 
        db_table = 'formulaire_session'  # Spécifie le nom de la table existante 

