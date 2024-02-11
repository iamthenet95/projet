# Import des modules nécessaires depuis Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count

# Import des modèles et du formulaire depuis le même package
from .models import SessionCours, FormulaireSession
from .forms import CreerSessionForm

# Définition de la vue pour créer une nouvelle session
@login_required
def creer_session(request):
    if request.method == 'POST':
        # Si la méthode de requête est POST, crée un formulaire avec les données de la requête
        form = CreerSessionForm(request.POST)
        if form.is_valid():
            # Si le formulaire est valide, crée une nouvelle session
            session = form.save(commit=False)
            session.formateur = request.user  # Assigne l'utilisateur actuel comme formateur de la session
            session.save()
            return redirect('sessions_ouvertes')  # Redirige vers la vue de liste des sessions
    else:
        # Si la méthode de requête n'est pas POST, crée un formulaire vide
        form = CreerSessionForm()
    return render(request, 'creer_session.html', {'form': form})

# Définition de la vue pour afficher les sessions ouvertes au format JSON
def sessions_ouvertes(request):
    # Récupère toutes les sessions ouvertes depuis la base de données
    sessions_ouvertes = SessionCours.objects.filter(statut='ouvert')

    # Formate les données des sessions dans un format JSON
    sessions_data = []
    for session in sessions_ouvertes:
        session_data = {
            'id': session.id,
            'heure_ouverture': session.heure_ouverture.isoformat(),
            'heure_fermeture': session.heure_fermeture.isoformat(),
            # Ajoute d'autres champs de session au besoin
        }
        sessions_data.append(session_data)

    # Renvoie les données au format JSON
    return JsonResponse({'sessions_ouvertes': sessions_data})

# Définition de la vue pour afficher les moyennes des résultats par session
def moyennes_par_session(request):
    # Récupère les dix derniers résultats de formulaire
    derniers_resultats = FormulaireSession.objects.order_by('-id')[:10]
    # Calcule la moyenne des avancements
    moyenne_avancement = sum(resultat.avancement for resultat in derniers_resultats) / len(derniers_resultats)
    
    # Crée un contexte avec les données à afficher dans le template
    context = {
        'derniers_resultats': derniers_resultats,
        'moyenne_avancement': moyenne_avancement,
    }
    return render(request, 'moyennes_par_session.html', context)

