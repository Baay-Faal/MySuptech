from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ton_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mysuptech.db'

    db.init_app(app)
    login_manager.init_app(app)

    # Importer les modèles ici pour éviter le cercle
    from app import models

    # Routes
    from flask import render_template, redirect, url_for, request, flash
    from flask_login import login_user, logout_user, login_required, current_user

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = models.User.query.filter_by(email=email).first()
            if user and user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Email ou mot de passe incorrect", 'danger')
        return render_template('login&register.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            user = models.User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Compte créé avec succès", 'success')
            return redirect(url_for('login'))
        return render_template('login&register.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    return app