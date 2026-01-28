from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User

class AuthService:
    """Service pour gérer l'authentification des utilisateurs."""
    
    @staticmethod
    def register_user(username, email, password, role='user'):
        """
        Enregistre un nouvel utilisateur.
        
        Args:
            username (str): Nom d'utilisateur
            email (str): Email de l'utilisateur
            password (str): Mot de passe en clair
            role (str): Rôle de l'utilisateur ('user', 'prof', 'admin')
        
        Returns:
            tuple: (User object, error_message) ou (None, error_message) en cas d'erreur
        """
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            return None, "Nom d'utilisateur déjà existant!"
        
        if User.query.filter_by(email=email).first():
            return None, "Email déjà utilisé!"
        
        # Créer le nouvel utilisateur
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user, "Inscription réussie!"
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur lors de l'inscription: {str(e)}"
    
    @staticmethod
    def verify_credentials(username, password):
        """
        Vérifie les identifiants d'un utilisateur.
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe en clair
        
        Returns:
            User object si valide, None sinon
        """
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Récupère un utilisateur par son ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Récupère un utilisateur par son nom d'utilisateur."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Récupère un utilisateur par son email."""
        return User.query.filter_by(email=email).first()
