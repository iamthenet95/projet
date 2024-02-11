from django.contrib import admin
from .models import SessionCours

# Définition d'une classe d'administration pour le modèle SessionCours
class SessionCoursAdmin(admin.ModelAdmin):
    # Champ de la liste d'affichage dans l'interface d'administration
    list_display = ('formateur', 'heure_ouverture', 'heure_fermeture', 'statut')
    # Filtres pour la liste d'affichage dans l'interface d'administration
    list_filter = ('statut',)

# Enregistrement du modèle SessionCours avec sa classe d'administration personnalisée
admin.site.register(SessionCours, SessionCoursAdmin)

