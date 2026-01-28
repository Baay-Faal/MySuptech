from app import db
from app.models import Presence, SessionCours, Etudiant

class AttendanceService:
    """Service pour gérer les présences."""
    
    @staticmethod
    def mark_attendance(session_id, etudiant_id, est_absent=False):
        """
        Marque la présence/absence d'un étudiant.
        
        Returns:
            tuple: (Presence object, message, success)
        """
        try:
            # Vérifier que la session et l'étudiant existent
            session = SessionCours.query.get(session_id)
            student = Etudiant.query.get(etudiant_id)
            
            if not session or not student:
                return None, "Session ou étudiant introuvable", False
            
            # Vérifier si cette présence existe déjà
            existing = Presence.query.filter_by(
                session_id=session_id,
                etudiant_id=etudiant_id
            ).first()
            
            if existing:
                # Mettre à jour
                existing.est_absent = est_absent
                db.session.commit()
                return existing, "Présence mise à jour", True
            else:
                # Créer nouvelle présence
                presence = Presence(
                    session_id=session_id,
                    etudiant_id=etudiant_id,
                    est_absent=est_absent
                )
                db.session.add(presence)
                db.session.commit()
                return presence, "Présence enregistrée", True
        except Exception as e:
            db.session.rollback()
            return None, f"Erreur: {str(e)}", False
    
    @staticmethod
    def get_attendance_by_session(session_id):
        """Récupère toutes les présences d'une session."""
        return Presence.query.filter_by(session_id=session_id).all()
    
    @staticmethod
    def get_attendance_by_student(etudiant_id):
        """Récupère toutes les présences d'un étudiant."""
        return Presence.query.filter_by(etudiant_id=etudiant_id).all()
    
    @staticmethod
    def get_attendance_by_id(attendance_id):
        """Récupère une présence par son ID."""
        return Presence.query.get(attendance_id)
    
    @staticmethod
    def get_student_attendance_stats(etudiant_id):
        """
        Récupère les statistiques de présence d'un étudiant.
        
        Returns:
            dict: {'total': int, 'absences': int, 'attendances': int, 'rate': float}
        """
        presences = Presence.query.filter_by(etudiant_id=etudiant_id).all()
        
        total = len(presences)
        absences = sum(1 for p in presences if p.est_absent)
        attendances = total - absences
        
        rate = (attendances / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'absences': absences,
            'attendances': attendances,
            'rate': round(rate, 2)
        }
    
    @staticmethod
    def delete_attendance(attendance_id):
        """
        Supprime une présence.
        
        Returns:
            tuple: (message, success)
        """
        try:
            attendance = Presence.query.get(attendance_id)
            if not attendance:
                return "Présence introuvable", False
            
            db.session.delete(attendance)
            db.session.commit()
            return "Présence supprimée", True
        except Exception as e:
            db.session.rollback()
            return f"Erreur: {str(e)}", False
