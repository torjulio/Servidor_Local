from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Configuração inicial
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

db = SQLAlchemy(app)

# Modelo do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='files', lazy=True)

# Função auxiliar para obter o usuário atual
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

# Rota inicial
@app.route('/')
def index():
    current_user = get_current_user()
    if current_user:
        if current_user.is_admin:
            # Inclui o proprietário em cada arquivo
            all_files = File.query.join(User, File.user_id == User.id).add_columns(File.id, File.filename, User.username.label('owner_name')).all()
            return render_template('index.html', files=all_files, current_user=current_user, is_admin=True)
        else:
            # Inclui o proprietário nos arquivos do usuário
            user_files = File.query.filter_by(user_id=current_user.id).join(User, File.user_id == User.id).add_columns(File.id, File.filename, User.username.label('owner_name')).all()
            return render_template('index.html', files=user_files, current_user=current_user, is_admin=False)
    return redirect(url_for('login'))



# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe!')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro realizado com sucesso! Faça login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login realizado com sucesso!')
            return redirect(url_for('index'))
        flash('Credenciais inválidas!')
    return render_template('login.html')

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Você saiu da sua conta.')
    return redirect(url_for('login'))

# Rota para upload de arquivos
@app.route('/upload', methods=['POST'])
def upload():
    current_user = get_current_user()
    if not current_user:
        flash('Faça login para enviar arquivos!')
        return redirect(url_for('login'))

    file = request.files.get('file')
    if not file or file.filename == '':
        flash('Nenhum arquivo selecionado!')
        return redirect(url_for('index'))

    filename = secure_filename(file.filename)
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
    os.makedirs(user_folder, exist_ok=True)
    file.save(os.path.join(user_folder, filename))

    new_file = File(filename=filename, user_id=current_user.id)
    db.session.add(new_file)
    db.session.commit()

    flash('Arquivo enviado com sucesso!')
    return redirect(url_for('index'))

# Rota para deletar arquivos
@app.route('/delete', methods=['POST'])
def delete():
    current_user = get_current_user()
    if not current_user:
        flash('Faça login para continuar!')
        return redirect(url_for('login'))

    file_id = request.form.get('file_id')
    file = File.query.get(file_id)
    if file:
        # Permitir que o administrador ou o dono do arquivo exclua
        if current_user.is_admin or file.user_id == current_user.id:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(file.user_id), file.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            db.session.delete(file)
            db.session.commit()
            flash('Arquivo deletado com sucesso!')
            return redirect(url_for('index'))
    flash('Arquivo não encontrado ou acesso negado!')
    return redirect(url_for('index'))

# Rota para download de arquivos
@app.route('/download/<int:file_id>')
def download(file_id):
    current_user = get_current_user()
    if not current_user:
        flash('Faça login para continuar!')
        return redirect(url_for('login'))

    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user.id))
        return send_from_directory(file_path, file.filename, as_attachment=True)
    flash('Arquivo não encontrado ou acesso negado!')
    return redirect(url_for('index'))

# Configuração inicial do banco de dados
with app.app_context():
    db.create_all()
    # Criar um administrador padrão, se não existir
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'), is_admin=True)
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
