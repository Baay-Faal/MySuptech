from app import db
from app.models import Etudiant, Classe

class StudentService:
    """Service pour gérer les étudiants."""
    
    @staticmethod
    def create_student(nom_E, prenom_E, classe_id):
        """
        Crée un nouvel étudiant.
        
        Returns:
            tuple: (Etudiant object, message, success)
        """
        try:
            # Vérifier que la classe existe
            classe = Classe.query.get(classe_id)
            if not classe:
                return None, "Classe introuvable", False
            
            student = Etudiant(
                nom_E=nom_E,
                prenom_E=prenom_E,
                classe_id=classe_id
            )
            db.session.add(student)
            db.session.commit()
            return student, "Étudiant créé avec succès", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def get_all_students():
        """Récupère tous les étudiants."""
        return Etudiant.query.all()
    
    @staticmethod
    def get_students_by_class(classe_id):
        """Récupère tous les étudiants d'une classe."""
        return Etudiant.query.filter_by(classe_id=classe_id).all()
    
    @staticmethod
    def get_student_by_id(student_id):
        """Récupère un étudiant par son ID."""
        return Etudiant.query.get(student_id)
    
    @staticmethod
    def update_student(student_id, nom_E=None, prenom_E=None, classe_id=None):
        """
        Met à jour un étudiant.
        
        Returns:
            tuple: (Etudiant object, message, success)
        """
        try:
            student = Etudiant.query.get(student_id)
            if not student:
                return None, "Étudiant introuvable", False
            
            if nom_E:
                student.nom_E = nom_E
            if prenom_E:
                student.prenom_E = prenom_E
            if classe_id:
                classe = Classe.query.get(classe_id)
                if not classe:
                    return None, "Classe introuvable", False
                student.classe_id = classe_id
            
            db.session.commit()
            return student, "Étudiant mis à jour", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def delete_student(student_id):
        """
        Supprime un étudiant.
        
        Returns:
            tuple: (message, success)
        """
        try:
            student = Etudiant.query.get(student_id)
            if not student:
                return "Étudiant introuvable", False
            
            db.session.delete(student)
            db.session.commit()
            return "Étudiant supprimé", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False
