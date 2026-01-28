from app import db
from app.models import Classe

class ClassService:
    """Service pour gérer les classes."""
    
    @staticmethod
    def create_class(nom):
        """
        Crée une nouvelle classe.
        
        Returns:
            tuple: (Classe object, message, success)
        """
        try:
            # Vérifier si la classe existe déjà
            if Classe.query.filter_by(nom=nom).first():
                return None, "Cette classe existe déjà", False
            
            classe = Classe(nom=nom)
            db.session.add(classe)
            db.session.commit()
            return classe, "Classe créée avec succès", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def get_all_classes():
        """Récupère toutes les classes."""
        return Classe.query.all()
    
    @staticmethod
    def get_class_by_id(classe_id):
        """Récupère une classe par son ID."""
        return Classe.query.get(classe_id)
    
    @staticmethod
    def get_class_by_name(nom):
        """Récupère une classe par son nom."""
        return Classe.query.filter_by(nom=nom).first()
    
    @staticmethod
    def update_class(classe_id, nom):
        """
        Met à jour une classe.
        
        Returns:
            tuple: (Classe object, message, success)
        """
        try:
            classe = Classe.query.get(classe_id)
            if not classe:
                return None, "Classe introuvable", False
            
            # Vérifier que le nouveau nom n'existe pas
            if nom != classe.nom and Classe.query.filter_by(nom=nom).first():
                return None, "Ce nom de classe existe déjà", False
            
            classe.nom = nom
            db.session.commit()
            return classe, "Classe mise à jour", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def delete_class(classe_id):
        """
        Supprime une classe.
        
        Returns:
            tuple: (message, success)
        """
        try:
            classe = Classe.query.get(classe_id)
            if not classe:
                return "Classe introuvable", False
            
            db.session.delete(classe)
            db.session.commit()
            return "Classe supprimée", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False
