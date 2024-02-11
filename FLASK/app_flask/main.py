# Import des dépendances nécessaires à l'application Flask
from flask import Flask, render_template, redirect, url_for, make_response, request, abort, session

# Import pour la génération automatique des éléments de formulaire
from flask_wtf import FlaskForm

# Import des éléments nécessaires pour la validation des données des formulaires
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email

#utilisation a coté un fichier env.py non gitté pour mettre tout ce qui est conf
## Conseil : migrer toutes les données de conf dans le fichier et gérer un contexte dev et prod
import datetime, json, jwt, bcrypt, mysql.connector, env, requests

# Import de l'extension Flask CORS pour gérer les CORS
from flask_cors import CORS

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

#initialise mon app Flask
app.secret_key = env.conf["secretLocal"]
jwt_secret_key = env.conf["secretJwt"]
API_URL = 'http://127.0.0.1:8000/sessions_ouvertes/'

# Définition des classes de formulaires pour la connexion et l'inscription
class LoginForm(FlaskForm):
    # Définition des champs du formulaire de connexion
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Connexion')

class RegisterForm(FlaskForm):
    # Définition des champs du formulaire d'inscription
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Adresse Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

# Fonction de vérification du mot de passe
def verify_password(plain_password, hashed_password, stored_salt):
    #Prend en paramère le mdp en clair, le hash, le salt associé au hash
    if stored_salt:
        salt = stored_salt.encode('utf-8')
        #Version a tester checkpw(password, hashed_password) en bytestring
        hashed_attempt = bcrypt.hashpw(plain_password.encode('utf'), salt)
        hashed_password = hashed_password.encode('utf-8')
        #renvoi un bool ok pas ok
        return hashed_attempt == hashed_password
    else:
        return False

# Fonction de génération du token JWT
def generate_jwt(username):
    # Génère un token JWT avec une expiration de 30 minutes
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Définition du formulaire de connexion
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        #J'ai mes identifiants je vais aller cherche en DB ce qu'il me faut
        #pour comparer
        # Conf BDD
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="romain",
            password=env.conf["dbPassword"],
            database="session"
        )

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT password, salt FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        
        if user_data:
            stored_hashed_password = user_data['password']
            stored_salt = user_data.get('salt')
            if verify_password(password, stored_hashed_password, stored_salt):
                #Si mot de passe vérifié, alors je génère mon JWT
                jwt_token = generate_jwt(username)
                #Je prepare ma réponse avec une redirection
                response = make_response(redirect(url_for('protected')))
                #Dans ma réponse je mettrais a jour les cookis
                response.set_cookie('jwt', jwt_token)
                session['username'] = username
                return response
                #Je renvoi ma réponse

            else:
                return "Erreur: Nom d'utilisateur ou mot de passe incorrect."
        else:
            return "Erreur: Nom d'utilisateur ou mot de passe incorrect."
        conn.close()
    #Si la page n'a pas été appelée eb post et ou si le formulaire n'est pas valide
    return render_template('login.html', form=form)

# Route d'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Récupération des données du formulaire d'inscription
        username = form.username.data
        password = form.password.data
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        nom = form.nom.data
        prenom = form.prenom.data
        email = form.email.data
        
        # Connexion à la base de données pour enregistrer les informations de l'utilisateur
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="romain",
            password=env.conf["dbPassword"],
            database="session"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO users (username, password, salt, nom, prenom, email) VALUES (%s, %s, %s, %s, %s, %s)", (username, hashed_password.decode('utf-8'), salt.decode('utf-8'), nom, prenom, email))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Route de protection
@app.route('/protected')
def protected():
    # Récupération des données des sessions depuis l'API Django
    response = requests.get('http://127.0.0.1:8000/sessions_ouvertes/')
    if response.status_code == 200:
        sessions = response.json()  # Convertir la réponse en JSON
        return render_template('protected.html', sessions=sessions)
    else:
        return f'Erreur lors de la récupération des sessions : {response.status_code}'

# Route pour afficher le formulaire pour une session spécifique lié a son ID
@app.route("/formulaire/<int:session_id>")
def afficher_formulaire(session_id):
    if 'submitted_form_session_' + str(session_id) in session:
        return render_template("formulaire_deja_soumis.html")
    
    # Récupération des détails de la session avec l'ID spécifié depuis la réponse JSON
    response = requests.get('http://localhost:8000/sessions_ouvertes/')
    if response.status_code == 200:
        sessions_data = response.json().get('sessions_ouvertes')
        session_data = next((session for session in sessions_data if session['id'] == session_id), None)
        
        if not session_data:
            return abort(404)
        
        # Renvoi le template du formulaire en incluant les données de la session
        return render_template("formulaire.html", session=session_data)
    else:
        return f'Erreur lors de la récupération des sessions : {response.status_code}'

# Route pour soumettre le formulaire pour une session spécifique
@app.route("/formulaire/<int:session_id>/soumettre", methods=["POST"])
def soumettre_formulaire(session_id):
    # Récupération de l'username de l'utilisateur connecté
    username = session.get('username')

    # Vérification si l'utilisateur a déjà soumis le formulaire pour cette session
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="romain",
        password=env.conf["dbPassword"],
        database="session"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM formulaire_session WHERE session_id = %s AND username = %s", (session_id, username))
    existing_submission = cursor.fetchone()
    conn.close()

    if existing_submission:
        return render_template("formulaire_deja_soumis.html")

    # Si l'utilisateur n'a pas encore soumis le formulaire pour cette session, continuer le traitement
    avancement = request.form['avancement']
    difficulte = request.form['difficulte']
    progression = request.form['progression']
    
    # Insérer les données dans la base de données
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="romain",
        password=env.conf["dbPassword"],
        database="session"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("INSERT INTO formulaire_session (session_id, avancement, difficulte, progression, username) VALUES (%s, %s, %s, %s, %s)", (session_id, avancement, difficulte, progression, username))
    conn.commit()
    conn.close()

    # Marquer le formulaire comme soumis dans la session de l'utilisateur
    session['submitted_form_session_' + str(session_id)] = True

    # Redirection vers la page des sessions ouvertes
    return redirect("/protected")

# Exécution de l'application Flask en mode debug
if __name__ == "__main__":
    app.run(debug=True)

