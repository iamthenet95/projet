Dans notre projet, Flask gère les pages web qui seront accessibles pour utilisateurs, comme la page de création de compte, la page de login et les formulaires qui seront associé a chaque session et remplie par les etudiants . Les données seront enregistrer dans la base de donnée.
De plus, Flask gère l'authentification des utilisateurs en vérifiant leurs informations d'identification lors de la connexion et en leur attribuant des jetons JWT (JSON Web Tokens) valide 30 minutes , qui sont utilisés pour sécuriser les communications entre l'application Flask et l'application Django.
En plus de ca il fait appel a l'API django pour recuperer les informations concernant les sessions ouvertes pour que l'etudiant voit sur son pannel a quoi il a accès.


Creation du base en SQL session;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    salt VARCHAR(255),
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE formulaire_session (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    avancement VARCHAR(255) NOT NULL,
    difficulte VARCHAR(255) NOT NULL,
    progression VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (username) REFERENCES users(username)
);