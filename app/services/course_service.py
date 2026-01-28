from app import db
from app.models import Cours, Classe, Matiere, User

class CourseService:
    """Service pour gérer les cours."""
    
    @staticmethod
    def create_course(jour, heure_debut, heure_fin, user_id, classe_id, matiere_id):
        """
        Crée un nouveau cours.
        
        Returns:
            tuple: (Cours object, message, success)
        """
        try:
            # Vérifier que l'utilisateur, la classe et la matière existent
            user = User.query.get(user_id)
            classe = Classe.query.get(classe_id)
            matiere = Matiere.query.get(matiere_id)
            
            if not user or not classe or not matiere:
                return None, "Professeur, classe ou matière introuvable", False
            
            course = Cours(
                jour=jour,
                heure_debut=heure_debut,
                heure_fin=heure_fin,
                user_id=user_id,
                classe_id=classe_id,
                matiere_id=matiere_id
            )
            db.session.add(course)
            db.session.commit()
            return course, "Cours créé avec succès", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def get_all_courses():
        """Récupère tous les cours."""
        return Cours.query.all()
    
    @staticmethod
    def get_courses_by_class(classe_id):
        """Récupère tous les cours d'une classe."""
        return Cours.query.filter_by(classe_id=classe_id).all()
    
    @staticmethod
    def get_courses_by_professor(user_id):
        """Récupère tous les cours d'un professeur."""
        return Cours.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_course_by_id(course_id):
        """Récupère un cours par son ID."""
        return Cours.query.get(course_id)
    
    @staticmethod
    def update_course(course_id, jour=None, heure_debut=None, heure_fin=None, 
                     user_id=None, classe_id=None, matiere_id=None):
        """
        Met à jour un cours.
        
        Returns:
            tuple: (Cours object, message, success)
        """
        try:
            course = Cours.query.get(course_id)
            if not course:
                return None, "Cours introuvable", False
            
            if jour:
                course.jour = jour
            if heure_debut:
                course.heure_debut = heure_debut
            if heure_fin:
                course.heure_fin = heure_fin
            if user_id:
                course.user_id = user_id
            if classe_id:
                course.classe_id = classe_id
            if matiere_id:
                course.matiere_id = matiere_id
            
            db.session.commit()
            return course, "Cours mis à jour", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def delete_course(course_id):
        """
        Supprime un cours.
        
        Returns:
            tuple: (message, success)
        """
        try:
            course = Cours.query.get(course_id)
            if not course:
                return "Cours introuvable", False
            
            db.session.delete(course)
            db.session.commit()
            return "Cours supprimé", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False
