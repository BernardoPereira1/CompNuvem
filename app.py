import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Chave secreta para gerenciar sessões
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

# Configuração do banco de dados
DB_USER = os.getenv('DB_USER', 'default_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'todo')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Modelo de Tarefa
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

# Página inicial com as tarefas do usuário logado
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('index.html', tasks=tasks)

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  # Aqui deve usar uma verificação segura de senha (hashing)
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect(url_for('index'))  # Redireciona para a página de index
        else:
            return "Email ou senha incorretos!", 403
    
    return render_template('login.html')

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verifica se o email já existe
        if User.query.filter_by(email=email).first():
            return "Email já cadastrado!", 400
        
        novo_usuario = User(email=email, password=password)
        db.session.add(novo_usuario)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Logoff
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

# Eliminar conta
@app.route('/delete_account', methods=['POST'])
def delete_account():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            # Remover todas as tasks associadas ao usuário
            Task.query.filter_by(user_id=user_id).delete()
            
            # Remover o usuário
            db.session.delete(user)
            db.session.commit()
            
            # Remover informações da sessão
            session.pop('user_id', None)
            session.pop('email', None)
            
            return redirect(url_for('login'))
    return redirect(url_for('index'))

# Adicionar tarefa
@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    descricao = request.form['descricao']
    user_id = session['user_id']
    nova_tarefa = Task(descricao=descricao, user_id=user_id)
    db.session.add(nova_tarefa)
    db.session.commit()

    return redirect(url_for('index'))

#Atualizar Tarefa
@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    tarefa = Task.query.get(id)
    if tarefa and tarefa.user_id == session['user_id']:
        nova_descricao = request.form['descricao']
        tarefa.descricao = nova_descricao
        tarefa.data_criacao = db.func.current_timestamp()  # Atualiza a data de criação
        db.session.commit()

    return redirect(url_for('index'))

# Deletar tarefa
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    tarefa = Task.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
