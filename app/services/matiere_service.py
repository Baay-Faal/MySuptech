from app import db
from app.models import Matiere

class MatiereService:
    """Service pour gérer les matières."""

    @staticmethod
    def create_matiere(nom):
        try:
            if Matiere.query.filter_by(nom=nom).first():
                return None, "Matière déjà existante", False
            matiere = Matiere(nom=nom)
            db.session.add(matiere)
            db.session.commit()
            return matiere, "Matière créée", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False

    @staticmethod
    def get_all_matieres():
        return Matiere.query.all()

    @staticmethod
    def get_matiere_by_id(matiere_id):
        return Matiere.query.get(matiere_id)

    @staticmethod
    def update_matiere(matiere_id, nom):
        try:
            matiere = Matiere.query.get(matiere_id)
            if not matiere:
                return None, "Matière introuvable", False
            if nom != matiere.nom and Matiere.query.filter_by(nom=nom).first():
                return None, "Ce nom de matière existe déjà", False
            matiere.nom = nom
            db.session.commit()
            return matiere, "Matière mise à jour", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False

    @staticmethod
    def delete_matiere(matiere_id):
        try:
            matiere = Matiere.query.get(matiere_id)
            if not matiere:
                return "Matière introuvable", False
            db.session.delete(matiere)
            db.session.commit()
            return "Matière supprimée", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False