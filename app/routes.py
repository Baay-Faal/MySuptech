from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.services.auth_service import AuthService

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