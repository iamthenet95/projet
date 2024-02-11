from django.contrib import admin
from django.urls import path
from .views import creer_session, sessions_ouvertes
from . import views

# Définition des URL patterns pour l'application
urlpatterns = [
    # URL pour accéder à l'interface d'administration Django
    path('admin/', admin.site.urls),
    # URL pour la création de session
    path('creer_session/', creer_session, name='creer_session'),
    # URL pour accéder à la liste des sessions ouvertes
    path('sessions_ouvertes/', sessions_ouvertes, name='sessions_ouvertes'),
    # URL pour afficher les moyennes par session
    path('moyennes_par_session/', views.moyennes_par_session, name='moyennes_par_session'),
]

