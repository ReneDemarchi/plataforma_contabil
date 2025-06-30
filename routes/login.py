from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, CadastroUsuarioForm
from db import get_db_connection, criar_usuario
from usuario import Usuario
auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    if 'usuario_logado' in session:
        return render_template('Registro/home.html')
    else:
        return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'usuario_logado' in session:
        return redirect(url_for('auth.home'))
    if form.validate_on_submit():
        usuario = form.usuario.data
        senha = form.senha.data
        user, senha_hash = Usuario.buscar_por_nome(usuario)
        if user and check_password_hash(senha_hash, senha):
            session['usuario_logado'] = {'id': user.id, 'nome': user.usuario, 'email': user.email}
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('auth.home'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
    return render_template('Registro/login.html', form=form)

@auth.route('/logout/')
def logout():
    session.pop('usuario_logado', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if 'usuario_logado' in session:
        return redirect(url_for('auth.home'))
    form = CadastroUsuarioForm()
    if form.validate_on_submit():
        usuario = form.usuario.data
        email = form.email.data
        senha = form.senha.data
        tipo = 'xxx'
        try:
            Usuario.criar(usuario,senha,email,tipo)
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Erro ao registrar usuário.', 'danger')
    return render_template('Registro/register.html', form=form)
