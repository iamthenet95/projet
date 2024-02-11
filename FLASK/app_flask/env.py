# env.py

import bcrypt

# Configuration des clés secrètes
conf = {
    "secretLocal": "rgwrdgrdgrg",
    "secretJwt": "gregegrg",
    "dbPassword": "azerty123"
}

# Fonctions de hachage de mot de passe
def generate_hashed_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8'), salt.decode('utf-8')

def verify_password(plain_password, hashed_password, salt):
    hashed_attempt = bcrypt.hashpw(plain_password.encode('utf-8'), salt.encode('utf-8'))
    return hashed_attempt == hashed_password.encode('utf-8')
