from datetime import datetime
from app import db
from app.models import SessionCours, Cours

def _parse_date(value):
    """Convertit une chaîne ISO ou datetime en datetime. Retourne datetime.utcnow() si invalide/None."""
    if value is None:
        return datetime.utcnow()
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return datetime.utcnow()
    return datetime.utcnow()

class SessionService:
    """Service pour gérer les sessions (cahier de texte)."""

    @staticmethod
    def create_session(cours_id, date=None, contenu=None, devoirs=None, point_arret=None, est_valide=False):
        try:
            cours = Cours.query.get(cours_id)
            if not cours:
                return None, "Cours introuvable", False
            date_val = _parse_date(date)
            session = SessionCours(
                cours_id=cours_id,
                date=date_val,
                contenu=contenu,
                devoirs=devoirs,
                point_arret=point_arret,
                est_valide=est_valide
            )
            db.session.add(session)
            db.session.commit()
            return session, "Session créée", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False

    @staticmethod
    def get_sessions_by_course(cours_id):
        return SessionCours.query.filter_by(cours_id=cours_id).all()

    @staticmethod
    def get_session_by_id(session_id):
        return SessionCours.query.get(session_id)

    @staticmethod
    def update_session(session_id, date=None, contenu=None, devoirs=None, point_arret=None, est_valide=None):
        try:
            session = SessionCours.query.get(session_id)
            if not session:
                return None, "Session introuvable", False
            if date is not None:
                session.date = _parse_date(date)
            if contenu is not None:
                session.contenu = contenu
            if devoirs is not None:
                session.devoirs = devoirs
            if point_arret is not None:
                session.point_arret = point_arret
            if est_valide is not None:
                session.est_valide = est_valide
            db.session.commit()
            return session, "Session mise à jour", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False

    @staticmethod
    def validate_session(session_id):
        try:
            session = SessionCours.query.get(session_id)
            if not session:
                return None, "Session introuvable", False
            session.est_valide = True
            db.session.commit()
            return session, "Session validée", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False

    @staticmethod
    def delete_session(session_id):
        try:
            session = SessionCours.query.get(session_id)
            if not session:
                return "Session introuvable", False
            db.session.delete(session)
            db.session.commit()
            return "Session supprimée", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False