import sqlalchemy as sa
from datetime import datetime, timezone
from app import app, db
from app.models import User
from app.forms import LoginForms, RegistrationForm, EditProfileForm
from urllib.parse import urlsplit
from flask_login import (current_user, 
                         login_user, 
                         logout_user,
                         login_required)
from flask import (render_template, #Módulo necessário para renderizar arquivos HTML através do python.
                   flash,           #Função que retorna uma mensagem ao usuário em caso de sucesso ou erro.
                   redirect,        #Redireciona para outra página
                   url_for,         #Redireciona para outra página, porem ser a sintaxe de '\'. Já leva direto ao endpoint
                   request)         

#Os geradores estão sendo usados como todas as possíveis rotas que a web page venha a ter.
@app.route('/')
@app.route('/index')
@login_required      #Página protegida contra usuários não logados.
def index():
    posts = [
        {
         'author': {'username': 'Raquel Rodrigues'},
         'post': 'Eu amo muito meu namorado ! <3'
        },
        {
         'author': {'username': 'Carlota'},
         'post': 'Lota, Lota, Lota !!!!!!'
        }
    ]
    return render_template('index.html', title='Página Inicial', posts=posts)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
                {'author': user, 'body': 'Postagem de texto #1'},
                {'author': user, 'body': 'Postagem de texto #2'}
            ]
    
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Suas alterações foram realizadas com sucesso!')
        return redirect(url_for('edit_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Editar Perfil', form=form)

@app.before_request   #É feito sempre antes de qualquer requisição
def before_request():
    if current_user.is_authenticated:  
        current_user.last_seen = datetime.now(timezone.utc)  #Atualiza a coluna de visto por ultimo no banco de dados do usuário
        db.session.commit()             #Commitando as mudanças

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   #Verifica se o usuário ja está logado
        return redirect(url_for('index'))
    
    form = LoginForms()

    if form.validate_on_submit():       #Se os dados estiverem preenchidos no formulário
        user = db.session.scalar(       #Pegar o usuario no bando de dados
            sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):  #Verifica se o usuário está no banco de dados ou se caso ele esteja, sua senha está correta.
            flash('Usuário ou Senha Inválido!')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)  #Login do usuário
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)                 #Redireciona para a página com o user logado. 

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  #Adicionando os dados na classe Usuário
        user.set_password(form.password.data)                            #Setando sua senha codificada
        db.session.add(user)                                             #Adicionando ao banco de dados
        db.session.commit()                                              #Commitando o novo usuário
        flash(f'Parabéns {user}, você agora é um usuário registrado :) !!!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)
