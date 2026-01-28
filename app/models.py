from datetime import datetime
from app import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(20), nullable=False, default='user')

    cours=db.relationship('Cours', backref='professeur', lazy=True)
    def __repr__(self):
        return f"User('{self.username}',  '{self.role}')"

class Classe(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50), unique=True, nullable=False)

    etudiants=db.relationship('Etudiant', backref='classe', lazy=True)
    cours=db.relationship('Cours', backref='classe', lazy=True)
    def __repr__(self):
        return f"Classe('{self.nom}')"

class Matiere(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nom=db.Column(db.String(50), unique=True, nullable=False)

    cours=db.relationship('Cours', backref='matiere', lazy=True)
    def __repr__(self):
        return f"Matiere('{self.nom}')"

class Etudiant(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nom_E=db.Column(db.String(50), nullable=False)
    prenom_E=db.Column(db.String(50), nullable=False)

    classe_id=db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)

    presences=db.relationship('Presence', backref='etudiant', lazy=True)
    def __repr__(self):
        return f"Etudiant('{self.nom_E}', '{self.prenom_E}')"

class Cours(db.Model): 
    id=db.Column(db.Integer, primary_key=True)
    jour=db.Column(db.String(20), nullable=False)
    heure_debut=db.Column(db.String(10), nullable=False)
    heure_fin=db.Column(db.String(10), nullable=False)

    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    classe_id=db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)
    matiere_id=db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)

    sessions=db.relationship('SessionCours', backref='cours_planifie', lazy=True)

class SessionCours(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenu=db.Column(db.Text, nullable=True)
    devoirs=db.Column(db.Text, nullable=True)
    point_arret=db.Column(db.String(255), nullable=True)
    est_valide=db.Column(db.Boolean, default=False)

    cours_id=db.Column(db.Integer, db.ForeignKey('cours.id'), nullable=False)
    presences=db.relationship('Presence', backref='session', lazy=True)

class Presence(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    est_absent=db.Column(db.Boolean, default=False)
    session_id=db.Column(db.Integer, db.ForeignKey('session_cours.id'), nullable=False)
    etudiant_id=db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    def __repr__(self):
        return f"Presence(session_id={self.session_id}, etudiant_id={self.etudiant_id})"
    