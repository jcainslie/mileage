from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask import redirect, render_template, request, flash, session
import os

login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def init_login(app):
    login_manager.init_app(app)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if request.form['username'] == os.getenv("APP_USERNAME") and request.form['password'] == os.getenv("APP_PASSWORD"):
                user = User(id=1)
                login_user(user)
                return redirect('/')
            else:
                flash("Invalid credentials", "danger")
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/login')
