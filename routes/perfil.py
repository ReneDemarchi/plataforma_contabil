from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from routes.modulos.requisito_login import login_requisito
from forms import LoginForm, Editar_usuario, Deletar_usuario_botao, Trocar_senha_usuario
from db import editar_usuario,dados_usuario_id, deletar_usuario as _deletar_usuario
from usuario import Usuario
perfil = Blueprint('perfil', __name__)

@perfil.route('/meu_perfil', methods=['GET', 'POST'])
@login_requisito
def meu_perfil():
    usuario = Usuario.buscar_por_id(session['usuario_logado']['id'])
    form = Editar_usuario()
    formDel = Deletar_usuario_botao()
    if form.validate_on_submit():
        usuario_nome = form.usuario.data
        email = form.email.data
        flash('Dados do perfil editados com sucesso', 'success')
        usuario.atualizar(usuario_nome, email)
        return redirect(url_for('auth.home'))
    if formDel.validate_on_submit():
        return redirect(url_for('auth.login'))
    return render_template('perfil/meu_perfil.html' ,usuario=usuario, form=form)



@perfil.route('/trocar_senha', methods=['GET', 'POST'])
@login_requisito
def trocar_senha():
    usuario_obj = Usuario.buscar_por_id(session['usuario_logado']['id'])
    formsenha = Trocar_senha_usuario()
    if formsenha.validate_on_submit():
        senha = formsenha.senha.data
        usuario_obj.trocar_senha(senha)
        flash('Senha trocada com sucesso!','success')
        return redirect(url_for('auth.login'))
    return render_template('perfil/trocar_senha.html' , form=formsenha)




@perfil.route('/deletar_usuario', methods=['GET', 'POST'])
@login_requisito
def deletar_usuario():
    usuario_obj = Usuario.buscar_por_id(session['usuario_logado']['id'])
    usuario_obj.deletar()
    return redirect('logout')


