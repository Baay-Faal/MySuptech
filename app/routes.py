from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.services.auth_service import AuthService
from app.services.course_service import CourseService
from app.services.class_service import ClassService
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService

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

# Route Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

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
def create_course():
    """Crée un nouveau cours."""
    data = request.get_json()
    course, message, success = CourseService.create_course(
        jour=data.get('jour'),
        heure_debut=data.get('heure_debut'),
        heure_fin=data.get('heure_fin'),
        user_id=data.get('user_id'),
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
def update_course(course_id):
    """Met à jour un cours."""
    data = request.get_json()
    course, message, success = CourseService.update_course(
        course_id=course_id,
        jour=data.get('jour'),
        heure_debut=data.get('heure_debut'),
        heure_fin=data.get('heure_fin'),
        user_id=data.get('user_id'),
        classe_id=data.get('classe_id'),
        matiere_id=data.get('matiere_id')
    )
    
    if success:
        return jsonify({'success': True, 'message': message}), 200
    return jsonify({'success': False, 'message': message}), 400

@app.route('/courses/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    """Supprime un cours."""
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

@app.route('/classes/create', methods=['POST'])
@login_required
def create_class():
    """Crée une nouvelle classe."""
    data = request.get_json()
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
    data = request.get_json()
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
    data = request.get_json()
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
    data = request.get_json()
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
def mark_attendance():
    """Marque la présence/absence d'un étudiant."""
    data = request.get_json()
    presence, message, success = AttendanceService.mark_attendance(
        session_id=data.get('session_id'),
        etudiant_id=data.get('student_id'),
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