# MySuptech - Système de Gestion de Présences

## 📋 Table des matières
- [Description du projet](#description-du-projet)
- [Architecture](#architecture)
- [Phases de développement](#phases-de-développement)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Collaboration Git](#collaboration-git)
- [Notes importantes](#notes-importantes)

---

## 🎯 Description du projet

**MySuptech** est une application web de gestion de présences pour une institution éducative. Elle permet aux professeurs de :
- Se connecter et gérer leurs cours
- Marquer les présences/absences des étudiants
- Gérer les classes et les étudiants
- Consulter les statistiques de présence

Les administrateurs peuvent :
- Voir le tableau de bord global
- Gérer les professeurs
- Gérer les classes
- Gérer les étudiants
- Accéder à tous les rapports de présences

---

## 👥 Système de rôles

| Rôle | Accès | Dashboard |
|------|-------|-----------|
| **Admin** | Tout le système | `/dashboard/admin` |
| **Prof** | Ses cours & présences | `/dashboard/prof` |

**Gestion des admins:**
- Les admins sont créés **directement en base de données** via le script `add_admin.py`
- Pour ajouter un admin, modifier `add_admin.py` et exécuter : `python add_admin.py`
- Pour la sécurité, les admins ne peuvent PAS être créés via la page d'inscription

---

## 🏗️ Architecture

```
MySuptech/
├── app/
│   ├── __init__.py              # Configuration Flask
│   ├── models.py                # Modèles SQLAlchemy
│   ├── routes.py                # Routes API & Auth
│   ├── services/
│   │   ├── auth_service.py      # Authentification
│   │   ├── course_service.py    # CRUD Cours
│   │   ├── class_service.py     # CRUD Classes
│   │   ├── student_service.py   # CRUD Étudiants
│   │   └── attendance_service.py # Gestion présences
│   ├── static/                  # CSS, JS
│   ├── templates/               # HTML templates
│   └── __pycache__/
├── instance/
│   └── site.db                  # Base de données SQLite
├── run.py                       # Point d'entrée
├── create_db.py                 # Script de création DB
└── requirements.txt             # Dépendances
```

### Modèles de données
- **User** : Utilisateurs (professeurs, admins)
- **Classe** : Classes/groupes d'étudiants
- **Matiere** : Matières enseignées
- **Cours** : Planification des cours
- **Etudiant** : Informations étudiants
- **SessionCours** : Sessions réalisées
- **Presence** : Enregistrement des présences

---

## 🚀 Phases de développement

### ✅ Phase 1 : Authentification - COMPLÉTÉE
**Status:** ✅ DONE  
**Développeur:** Backend (Toi)  

- [x] Route `/login` - Connexion utilisateur
- [x] Route `/register` - Inscription nouvel utilisateur
- [x] Route `/logout` - Déconnexion
- [x] Service d'authentification (`auth_service.py`)
- [x] Protection des routes avec `@login_required`
- [x] Gestion des mots de passe (hachage)

**Templates en attente:** 
- [ ] `login.html`
- [ ] `register.html`

---

### ✅ Phase 2 : CRUD Entités - COMPLÉTÉE
**Status:** ✅ DONE  
**Développeur:** Backend (Toi)  

#### Courses
- [x] Service `course_service.py`
- [x] Route GET `/courses` - Lister tous les cours
- [x] Route POST `/courses/create` - Créer un cours
- [x] Route GET `/courses/<id>` - Détail d'un cours
- [x] Route PUT `/courses/<id>` - Modifier un cours
- [x] Route DELETE `/courses/<id>` - Supprimer un cours

#### Classes
- [x] Service `class_service.py`
- [x] Route GET `/classes` - Lister toutes les classes
- [x] Route POST `/classes/create` - Créer une classe
- [x] Route GET `/classes/<id>` - Détail d'une classe
- [x] Route PUT `/classes/<id>` - Modifier une classe
- [x] Route DELETE `/classes/<id>` - Supprimer une classe

#### Étudiants
- [x] Service `student_service.py`
- [x] Route GET `/students` - Lister tous les étudiants
- [x] Route POST `/students/create` - Créer un étudiant
- [x] Route GET `/students/<id>` - Détail d'un étudiant
- [x] Route PUT `/students/<id>` - Modifier un étudiant
- [x] Route DELETE `/students/<id>` - Supprimer un étudiant

#### Présences
- [x] Service `attendance_service.py`
- [x] Route GET `/attendance/<session_id>` - Présences par session
- [x] Route POST `/attendance/mark` - Marquer présence/absence
- [x] Route GET `/attendance/student/<id>` - Stats étudiant
- [x] Route DELETE `/attendance/<id>` - Supprimer présence

**Templates en attente:**
- [ ] `dashboard.html`
- [ ] `courses.html`
- [ ] `classes.html`
- [ ] `students.html`
- [ ] `attendance.html`

---

### ⏳ Phase 3 : Frontend (Templates) - EN ATTENTE
**Status:** ⏳ NOT STARTED  
**Développeur:** Frontend (Ton ami)  

- [ ] Base template (`base.html`) - Navigation, styles globaux
- [ ] Page Login (`login.html`)
- [ ] Page Register (`register.html`)
- [ ] Dashboard (`dashboard.html`)
- [ ] Gestion Courses (`courses.html`)
- [ ] Gestion Classes (`classes.html`)
- [ ] Gestion Students (`students.html`)
- [ ] Gestion Attendance (`attendance.html`)
- [ ] Styling CSS (`style.css`)
- [ ] Scripts JS (optionnel)

---

### ⏳ Phase 4 : Fonctionnalités avancées - EN ATTENTE
**Status:** ⏳ NOT STARTED  

- [ ] Oublié mot de passe (`forgot_password.html`, `reset_password.html`)
- [ ] Génération rapports PDF
- [ ] Export données Excel
- [ ] Notifications email
- [ ] Dashboard avec graphiques
- [ ] Rôles et permissions (admin, prof, étudiant)
- [ ] Tests unitaires
- [ ] Déploiement production

---

## 📦 Installation

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner le repo**
```bash
git clone https://github.com/ton_username/MySuptech.git
cd MySuptech
```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Créer la base de données**
```bash
python create_db.py
```

5. **Ajouter les admins (IMPORTANT)**
```bash
python add_admin.py
```
Cela crée un compte admin par défaut:
- Username: `admin`
- Email: `admin@mysuptech.com`
- Password: `admin123` (À CHANGER en production!)

6. **Lancer l'application**
```bash
python run.py
```

L'app sera disponible sur : `http://127.0.0.1:5000/`

---

## 📂 Structure du projet détaillée

```
MySuptech/
├── app/
│   ├── __init__.py
│   │   └── Configuration Flask, SQLAlchemy, LoginManager
│   │
│   ├── models.py
│   │   ├── User (username, email, password, role)
│   │   ├── Classe (nom)
│   │   ├── Matiere (nom)
│   │   ├── Cours (jour, heure_debut, heure_fin, FK: user, classe, matiere)
│   │   ├── Etudiant (nom_E, prenom_E, FK: classe)
│   │   ├── SessionCours (date, contenu, devoirs, est_valide, FK: cours)
│   │   └── Presence (est_absent, FK: session, etudiant)
│   │
│   ├── routes.py
│   │   ├── Auth routes (login, register, logout)
│   │   ├── Course routes (CRUD)
│   │   ├── Class routes (CRUD)
│   │   ├── Student routes (CRUD)
│   │   └── Attendance routes
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   │   ├── register_user()
│   │   │   ├── verify_credentials()
│   │   │   └── get_user_*()
│   │   │
│   │   ├── course_service.py
│   │   │   ├── create_course()
│   │   │   ├── get_all_courses()
│   │   │   ├── update_course()
│   │   │   └── delete_course()
│   │   │
│   │   ├── class_service.py (même structure)
│   │   ├── student_service.py (même structure)
│   │   │
│   │   └── attendance_service.py
│   │       ├── mark_attendance()
│   │       ├── get_attendance_by_session()
│   │       ├── get_student_attendance_stats()
│   │       └── delete_attendance()
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css (TODO)
│   │   └── js/
│   │       └── script.js (TODO)
│   │
│   └── templates/
│       ├── base.html (TODO)
│       ├── login.html (TODO)
│       ├── register.html (TODO)
│       ├── dashboard.html (TODO)
│       ├── courses.html (TODO)
│       ├── classes.html (TODO)
│       ├── students.html (TODO)
│       └── attendance.html (TODO)
│
├── instance/
│   └── site.db (Base de données auto-créée)
│
├── run.py (Point d'entrée - python run.py)
├── create_db.py (Création DB - python create_db.py)
├── requirements.txt (Dépendances)
└── README.md (Cette documentation)
```

---

## 🔌 API Endpoints

### Authentification
| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/` | Redirige vers login | Non |
| POST | `/login` | Se connecter | Non |
| POST | `/register` | S'inscrire | Non |
| GET | `/logout` | Se déconnecter | Oui |
| GET | `/dashboard` | Tableau de bord | Oui |

### Courses
| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/courses` | Lister tous les cours | Oui |
| POST | `/courses/create` | Créer un cours | Oui |
| GET | `/courses/<id>` | Détail d'un cours | Oui |
| PUT | `/courses/<id>` | Modifier un cours | Oui |
| DELETE | `/courses/<id>` | Supprimer un cours | Oui |

### Classes
| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/classes` | Lister toutes les classes | Oui |
| POST | `/classes/create` | Créer une classe | Oui |
| GET | `/classes/<id>` | Détail d'une classe | Oui |
| PUT | `/classes/<id>` | Modifier une classe | Oui |
| DELETE | `/classes/<id>` | Supprimer une classe | Oui |

### Étudiants
| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/students` | Lister tous les étudiants | Oui |
| POST | `/students/create` | Créer un étudiant | Oui |
| GET | `/students/<id>` | Détail d'un étudiant | Oui |
| PUT | `/students/<id>` | Modifier un étudiant | Oui |
| DELETE | `/students/<id>` | Supprimer un étudiant | Oui |

### Présences
| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/attendance/<session_id>` | Présences d'une session | Oui |
| POST | `/attendance/mark` | Marquer présence/absence | Oui |
| GET | `/attendance/student/<id>` | Stats étudiant | Oui |
| DELETE | `/attendance/<id>` | Supprimer présence | Oui |

---

## 🌳 Collaboration Git

### Branches
- `main` - Branche de production (stable)
- `gueye` - Branche toi (Backend/APIs)
- `kane` - Branche ton ami (Templates/UI)

### Workflow
1. Chacun travaille sur sa branche
2. Commit régulièrement : `git commit -m "message descriptif"`
3. Push : `git push origin nom-branche`
4. Créer des Pull Requests pour merger
5. Rebase avant de merger : `git rebase main`

### Commandes utiles
```bash
# Créer une branche
git checkout -b feature/backend

# Voir les branches
git branch -a

# Changer de branche
git checkout feature/backend

# Pusher les changements
git push origin feature/backend

# Rebase
git rebase main
```

---

## 📝 Notes importantes

### Sécurité
- ✅ Mots de passe hachés avec Werkzeug
- ✅ Sessions Flask-Login
- ⏳ À ajouter : Rate limiting, CSRF protection, validation inputs

### Conventions de code
- Noms de fonctions en `snake_case`
- Noms de classes en `PascalCase`
- Docstrings pour tous les services
- Retours standardisés : `(objet, message, success)` ou `(message, success)`

### Dépendances
```
Flask
Flask-SQLAlchemy
Flask-Login
Werkzeug
```

À ajouter quand nécessaire :
- `Flask-Mail` (emails)
- `python-dotenv` (variables d'env)
- `Flask-Cors` (API calls cross-origin)
- `PyPDF2` ou `reportlab` (PDF)
- `openpyxl` (Excel)

### Problèmes connus
- Aucun pour le moment

### Prochaines étapes immédiates
1. ✅ Backend : Routes CRUD créées
2. ⏳ Frontend : Créer les templates HTML
3. ⏳ Tester les endpoints avec Postman
4. ⏳ Merger les branches vers main

---

## 📞 Contact & Support

**Équipe:**
- Backend (Toi) : `gueye`
- Frontend (Ton ami) : `kane`

**Dernier update:** 28 Janvier 2026

---

**Bon développement ! 🚀**
