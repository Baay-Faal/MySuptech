"""
Script pour ajouter des admins à la base de données.
Utilisation: python add_admin.py
"""

from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

def add_admin(username, email, password):
    """Ajoute un admin à la base de données."""
    
    with app.app_context():
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            print(f"❌ Admin '{username}' existe déjà!")
            return False
        
        if User.query.filter_by(email=email).first():
            print(f"❌ Email '{email}' est déjà utilisé!")
            return False
        
        # Créer le nouvel admin
        admin = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role='admin'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print(f"✅ Admin '{username}' créé avec succès!")
        print(f"   Email: {email}")
        print(f"   Rôle: admin")
        return True

if __name__ == '__main__':
    # Exemple : Créer l'admin principal
    print("=" * 50)
    print("CRÉATION D'ADMINS MYSUPTECH")
    print("=" * 50)
    
    # Admin 1
    add_admin(
        username='admin',
        email='admin@mysuptech.com',
        password='admin123'  # À CHANGER en production!
    )
    
    # Tu peux ajouter d'autres admins ici
    # add_admin(
    #     username='directeur',
    #     email='directeur@mysuptech.com',
    #     password='directeur123'
    # )
    
    print("=" * 50)
    print("✅ Configuration des admins terminée!")
    print("=" * 50)
