from django import forms
from .models import SessionCours

# Définition du formulaire de création de session
class CreerSessionForm(forms.ModelForm):
    class Meta:
        model = SessionCours  # Utilise le modèle SessionCours pour créer le formulaire
        fields = ['heure_ouverture', 'heure_fermeture', 'statut']  # Champs du formulaire à inclure

