from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.class_service import ClassService
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.services.matiere_service import MatiereService
from app.services.session_service import SessionService
from app.decorators import role_required

# Route index
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        # Utiliser le service d'authentification
        new_user, message = AuthService.register_user(username, email, password, role)
        
        if new_user:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')
    
    return render_template('register.html')

# Route Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Utiliser le service d'authentification
        user = AuthService.verify_credentials(username, password)
        
        if user:
            login_user(user)
            flash(f'Bienvenue {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect!', 'danger')
    
    return render_template('login.html')

# Route Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))

# Route Dashboard - Redirige selon le rôle
@app.route('/dashboard')
@login_required
def dashboard():
    """Redirige vers le dashboard approprié selon le rôle."""
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'prof':
        return redirect(url_for('prof_dashboard'))
    else:
        flash('Rôle non reconnu', 'danger')
        return redirect(url_for('logout'))

# Dashboard Admin
@app.route('/dashboard/admin')
@login_required
@role_required('admin')
def admin_dashboard():
    """Dashboard pour les administrateurs."""
    total_profs = len(User.query.filter_by(role='prof').all())
    total_classes = len(ClassService.get_all_classes())
    total_students = len(StudentService.get_all_students())
    
    return render_template('admin/dashboard.html', 
                          total_profs=total_profs,
                          total_classes=total_classes,
                          total_students=total_students,
                          user=current_user)

# Dashboard Professeur
@app.route('/dashboard/prof')
@login_required
@role_required('prof')
def prof_dashboard():
    """Dashboard pour les professeurs."""
    courses = CourseService.get_courses_by_professor(current_user.id)
    
    return render_template('prof/dashboard.html',
                          courses=courses,
                          user=current_user)

# ========== PAGES ADMIN (templates) ==========

@app.route('/admin/classes')
@login_required
@role_required('admin')
def admin_classes_page():
    """Page gestion des classes."""
    classes = ClassService.get_all_classes()
    return render_template('admin/classes.html', classes=classes, user=current_user)

@app.route('/admin/students')
@login_required
@role_required('admin')
def admin_students_page():
    """Page gestion des étudiants."""
    students = StudentService.get_all_students()
    classes = ClassService.get_all_classes()
    return render_template('admin/students.html', students=students, classes=classes, user=current_user)

# ========== PAGES PROF (templates) ==========

@app.route('/prof/courses')
@login_required
@role_required('prof')
def prof_courses_page():
    """Page gestion des cours (prof)."""
    courses = CourseService.get_courses_by_professor(current_user.id)
    classes = ClassService.get_all_classes()
    matieres = MatiereService.get_all_matieres()
    return render_template('prof/courses.html', courses=courses, classes=classes, matieres=matieres, user=current_user)

@app.route('/prof/attendance')
@login_required
@role_required('prof')
def prof_attendance_page():
    """Page marquer les présences."""
    courses = CourseService.get_courses_by_professor(current_user.id)
    return render_template('prof/attendance.html', courses=courses, user=current_user)

# ========== COURSES ROUTES ==========

@app.route('/courses', methods=['GET'])
@login_required
def get_courses():
    """Récupère tous les cours."""
    courses = CourseService.get_all_courses()
    return jsonify([{
        'id': c.id,
        'jour': c.jour,
        'heure_debut': c.heure_debut,
        'heure_fin': c.heure_fin,
        'professeur': c.professeur.username,
        'classe': c.classe.nom,
        'matiere': c.matiere.nom
    } for c in courses])

@app.route('/courses/create', methods=['POST'])
@login_required
@role_required('prof', 'admin')
def create_course():
    """Crée un nouveau cours. user_id est pris depuis current_user pour des raisons de sécurité."""
    data = request.get_json() or {}
    # Validation minimale
    if not data.get('jour') or not data.get('heure_debut') or not data.get('heure_fin') or not data.get('classe_id') or not data.get('matiere_id'):
        return jsonify({'success': False, 'message': 'Champs requis manquants'}), 400

    course, message, success = CourseService.create_course(
        jour=data.get('jour'),
        heure_debut=data.get('heure_debut'),
        heure_fin=data.get('heure_fin'),
        user_id=current_user.id,
        classe_id=data.get('classe_id'),
        matiere_id=data.get('matiere_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message, 'course_id': course.id}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/courses/<int:course_id>', methods=['GET'])
@login_required
def get_course(course_id):
    """Récupère un cours par son ID."""
    course = CourseService.get_course_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': 'Cours introuvable'}), 404
    
    return jsonify({
        'id': course.id,
        'jour': course.jour,
        'heure_debut': course.heure_debut,
        'heure_fin': course.heure_fin,
        'professeur': course.professeur.username,
        'classe': course.classe.nom,
        'matiere': course.matiere.nom
    })

@app.route('/courses/<int:course_id>', methods=['PUT'])
@login_required
@role_required('prof', 'admin')
def update_course(course_id):
    """Met à jour un cours. Seul l'admin ou le professeur propriétaire peuvent modifier."""
    data = request.get_json() or {}
    course = CourseService.get_course_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': 'Cours introuvable'}), 404
    # Permission check
    if current_user.role != 'admin' and course.user_id != current_user.id:
        return jsonify({'success': False, 'message': "Accès refusé"}), 403

    course, message, success = CourseService.update_course(
        course_id=course_id,
        jour=data.get('jour'),
        heure_debut=data.get('heure_debut'),
        heure_fin=data.get('heure_fin'),
        user_id=current_user.id if data.get('user_id') is None else data.get('user_id'),
        classe_id=data.get('classe_id'),
        matiere_id=data.get('matiere_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/courses/<int:course_id>', methods=['DELETE'])
@login_required
@role_required('prof', 'admin')
def delete_course(course_id):
    """Supprime un cours. Seul l'admin ou le professeur propriétaire peuvent supprimer."""
    course = CourseService.get_course_by_id(course_id)
    if not course:
        return jsonify({'success': False, 'message': 'Cours introuvable'}), 404
    if current_user.role != 'admin' and course.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Accès refusé'}), 403

    message, success = CourseService.delete_course(course_id)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

# ========== CLASSES ROUTES ==========

@app.route('/classes', methods=['GET'])
@login_required
def get_classes():
    """Récupère toutes les classes."""
    classes = ClassService.get_all_classes()
    return jsonify([{'id': c.id, 'nom': c.nom} for c in classes])

# ========== MATIERES ROUTES ==========

@app.route('/matieres', methods=['GET'])
@login_required
def get_matieres():
    """Récupère toutes les matières."""
    matieres = MatiereService.get_all_matieres()
    return jsonify([{'id': m.id, 'nom': m.nom} for m in matieres])

@app.route('/matieres/create', methods=['POST'])
@login_required
@role_required('admin')
def create_matiere():
    data = request.get_json() or {}
    if not data.get('nom'):
        return jsonify({'success': False, 'message': 'Nom requis'}), 400
    matiere, message, success = MatiereService.create_matiere(nom=data.get('nom'))
    if success:
        return jsonify({'success': True, 'message': message, 'mat_id': matiere.id}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/matieres/<int:mat_id>', methods=['GET'])
@login_required
def get_matiere(mat_id):
    matiere = MatiereService.get_matiere_by_id(mat_id)
    if not matiere:
        return jsonify({'success': False, 'message': 'Matière introuvable'}), 404
    return jsonify({'id': matiere.id, 'nom': matiere.nom})

@app.route('/matieres/<int:mat_id>', methods=['PUT'])
@login_required
@role_required('admin')
def update_matiere(mat_id):
    data = request.get_json() or {}
    matiere, message, success = MatiereService.update_matiere(mat_id, nom=data.get('nom'))
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/matieres/<int:mat_id>', methods=['DELETE'])
@login_required
@role_required('admin')
def delete_matiere(mat_id):
    message, success = MatiereService.delete_matiere(mat_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

# ========== SESSIONS (CAHIER DE TEXTE) ROUTES ==========

@app.route('/sessions/create', methods=['POST'])
@login_required
@role_required('prof', 'admin')
def create_session():
    data = request.get_json() or {}
    if not data.get('cours_id'):
        return jsonify({'success': False, 'message': 'cours_id requis'}), 400
    session, message, success = SessionService.create_session(
        cours_id=data.get('cours_id'),
        date=data.get('date'),
        contenu=data.get('contenu'),
        devoirs=data.get('devoirs'),
        point_arret=data.get('point_arret'),
        est_valide=data.get('est_valide', False)
    )
    if success:
        return jsonify({'success': True, 'message': message, 'session_id': session.id}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/courses/<int:course_id>/sessions', methods=['GET'])
@login_required
def get_course_sessions(course_id):
    sessions = SessionService.get_sessions_by_course(course_id)
    return jsonify([{
        'id': s.id,
        'date': s.date.isoformat() if s.date else None,
        'contenu': s.contenu,
        'devoirs': s.devoirs,
        'point_arret': s.point_arret,
        'est_valide': s.est_valide
    } for s in sessions])

@app.route('/sessions/<int:session_id>', methods=['GET'])
@login_required
def get_session(session_id):
    session = SessionService.get_session_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'message': 'Session introuvable'}), 404
    return jsonify({
        'id': session.id,
        'cours_id': session.cours_id,
        'date': session.date.isoformat() if session.date else None,
        'contenu': session.contenu,
        'devoirs': session.devoirs,
        'point_arret': session.point_arret,
        'est_valide': session.est_valide
    })

@app.route('/sessions/<int:session_id>', methods=['PUT'])
@login_required
@role_required('prof', 'admin')
def update_session(session_id):
    data = request.get_json() or {}
    session, message, success = SessionService.update_session(
        session_id=session_id,
        date=data.get('date'),
        contenu=data.get('contenu'),
        devoirs=data.get('devoirs'),
        point_arret=data.get('point_arret'),
        est_valide=data.get('est_valide')
    )
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/sessions/<int:session_id>/validate', methods=['PUT'])
@login_required
@role_required('prof', 'admin')
def validate_session(session_id):
    session, message, success = SessionService.validate_session(session_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/sessions/<int:session_id>', methods=['DELETE'])
@login_required
@role_required('prof', 'admin')
def delete_session(session_id):
    message, success = SessionService.delete_session(session_id)
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/classes/create', methods=['POST'])
@login_required
def create_class():
    """Crée une nouvelle classe."""
    data = request.get_json() or {}
    if not data.get('nom'):
        return jsonify({'success': False, 'message': 'Nom requis'}), 400
    classe, message, success = ClassService.create_class(nom=data.get('nom'))
    
    if success:
        return jsonify({'success': True, 'message': message, 'class_id': classe.id}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/classes/<int:class_id>', methods=['GET'])
@login_required
def get_class(class_id):
    """Récupère une classe par son ID."""
    classe = ClassService.get_class_by_id(class_id)
    if not classe:
        return jsonify({'success': False, 'message': 'Classe introuvable'}), 404
    
    return jsonify({'id': classe.id, 'nom': classe.nom})

@app.route('/classes/<int:class_id>', methods=['PUT'])
@login_required
def update_class(class_id):
    """Met à jour une classe."""
    data = request.get_json() or {}
    if not data.get('nom'):
        return jsonify({'success': False, 'message': 'Nom requis'}), 400
    classe, message, success = ClassService.update_class(class_id=class_id, nom=data.get('nom'))
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/classes/<int:class_id>', methods=['DELETE'])
@login_required
def delete_class(class_id):
    """Supprime une classe."""
    message, success = ClassService.delete_class(class_id)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

# ========== STUDENTS ROUTES ==========

@app.route('/students', methods=['GET'])
@login_required
def get_students():
    """Récupère tous les étudiants."""
    students = StudentService.get_all_students()
    return jsonify([{
        'id': s.id,
        'nom': s.nom_E,
        'prenom': s.prenom_E,
        'classe': s.classe.nom
    } for s in students])

@app.route('/students/create', methods=['POST'])
@login_required
def create_student():
    """Crée un nouvel étudiant."""
    data = request.get_json() or {}
    if not data.get('nom') or not data.get('prenom') or not data.get('classe_id'):
        return jsonify({'success': False, 'message': 'Nom, prénom et classe requis'}), 400
    student, message, success = StudentService.create_student(
        nom_E=data.get('nom'),
        prenom_E=data.get('prenom'),
        classe_id=data.get('classe_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message, 'student_id': student.id}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/students/<int:student_id>', methods=['GET'])
@login_required
def get_student(student_id):
    """Récupère un étudiant par son ID."""
    student = StudentService.get_student_by_id(student_id)
    if not student:
        return jsonify({'success': False, 'message': 'Étudiant introuvable'}), 404
    
    return jsonify({
        'id': student.id,
        'nom': student.nom_E,
        'prenom': student.prenom_E,
        'classe': student.classe.nom
    })

@app.route('/students/<int:student_id>', methods=['PUT'])
@login_required
def update_student(student_id):
    """Met à jour un étudiant."""
    data = request.get_json() or {}
    student, message, success = StudentService.update_student(
        student_id=student_id,
        nom_E=data.get('nom'),
        prenom_E=data.get('prenom'),
        classe_id=data.get('classe_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/students/<int:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    """Supprime un étudiant."""
    message, success = StudentService.delete_student(student_id)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

# ========== ATTENDANCE ROUTES ==========

@app.route('/attendance/<int:session_id>', methods=['GET'])
@login_required
def get_session_attendance(session_id):
    """Récupère toutes les présences d'une session."""
    attendances = AttendanceService.get_attendance_by_session(session_id)
    return jsonify([{
        'id': a.id,
        'etudiant': a.etudiant.nom_E + ' ' + a.etudiant.prenom_E,
        'est_absent': a.est_absent
    } for a in attendances])

@app.route('/attendance/mark', methods=['POST'])
@login_required
@role_required('prof', 'admin')
def mark_attendance():
    """Marque la présence/absence d'un étudiant."""
    data = request.get_json() or {}
    # accept both 'student_id' and 'etudiant_id' for compatibility
    etudiant_id = data.get('etudiant_id') or data.get('student_id')
    if not data.get('session_id') or not etudiant_id:
        return jsonify({'success': False, 'message': 'Champs requis manquants'}), 400

    presence, message, success = AttendanceService.mark_attendance(
        session_id=data.get('session_id'),
        etudiant_id=etudiant_id,
        est_absent=data.get('est_absent', False)
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 201
    return jsonify({'success': False, 'message': message}), 400

@app.route('/attendance/student/<int:student_id>', methods=['GET'])
@login_required
def get_student_attendance(student_id):
    """Récupère les statistiques de présence d'un étudiant."""
    stats = AttendanceService.get_student_attendance_stats(student_id)
    return jsonify(stats)

@app.route('/attendance/<int:attendance_id>', methods=['DELETE'])
@login_required
def delete_attendance(attendance_id):
    """Supprime une présence."""
    message, success = AttendanceService.delete_attendance(attendance_id)
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400