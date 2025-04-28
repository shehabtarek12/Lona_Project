from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'your_secret_key'  # This is necessary for session management

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Make sure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# User class
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role  # 'admin' or 'user'

# Mocked user database
users = {
    'admin': {'password': 'adminpassword', 'role': 'admin'},
    'user1': {'password': 'userpassword', 'role': 'user'}
}

# Mocking login function
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        return User(user_id, user_id, user_data['role'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]['password'] == password:
            user = User(username, username, users[username]['role'])
            login_user(user)
            return redirect(url_for('user_dashboard' if user.role == 'user' else 'admin'))

        return 'Invalid credentials, please try again.'

    return render_template('login.html')


@app.route('/admin')
@login_required
def admin():
    # Ensure that only admin can access this page
    if current_user.role != 'admin':
        return redirect(url_for('login'))  # Redirect non-admin users to login page

    # Load tickets
    tickets = []
    if os.path.exists('tickets.json'):
        with open('tickets.json', 'r', encoding='utf-8') as f:
            try:
                tickets = json.load(f)
            except json.JSONDecodeError:
                tickets = []

    return render_template('admin.html', tickets=tickets)


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/ticket_success')
def thank_you():
    return render_template('ticket_success.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        branch = request.form.get('branch')
        pcname = request.form.get('pcname')
        depname = request.form.get('depname')
        category = request.form.get('category')
        description = request.form.get('description')
        solution = request.form.get('solution')
        image = request.files.get('image')

        # Check if image is provided and is valid
        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_url = f'/uploads/{filename}'

        # Create ticket data
        ticket = {
            'name': name,
            'email': email,
            'branch': branch,
            'pcname': pcname,
            'depname': depname,
            'category': category,
            'description': description,
            'solution': solution,
            'image': image_url
        }

        # Save ticket in the JSON file
        tickets = []
        if os.path.exists('tickets.json'):
            with open('tickets.json', 'r', encoding='utf-8') as f:
                try:
                    tickets = json.load(f)
                except json.JSONDecodeError:
                    tickets = []

        tickets.append(ticket)
        with open('tickets.json', 'w', encoding='utf-8') as f:
            json.dump(tickets, f, ensure_ascii=False, indent=4)

        return redirect(url_for('thank_you'))
    except Exception as e:
        print("Error:", e)
        return jsonify({'message': 'Error occurred while submitting the ticket!'}), 500


# Function to check if the file is allowed (image only)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




