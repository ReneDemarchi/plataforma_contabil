from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from routes.modulos.requisito_login import login_requisito
from forms import LoginForm, CadastroUsuarioForm, precadastroo ,CadastroClienteAPI,visualizacao_dados_cliente , Editar_evento , Criar_evento
from api import consultar
from db import *
from cliente import Cliente
from calendario import Calendario
from datetime import datetime
cliente = Blueprint('cliente', __name__)

@cliente.route("/precadastro", methods=["GET", "POST"])
@login_requisito
def precadastro():
    form = precadastroo()
    if form.validate_on_submit():
        cnpj_sem_filtro = form.cnpj.data
        cnpj = cnpj_sem_filtro.replace('/','').replace('.','').replace('-','')
        hecliente = Cliente.buscar_por_cnpj(cnpj_sem_filtro)
        if hecliente is not None:
            return redirect(url_for("cliente.perfil_cliente", id_cliente=hecliente.id))
        if id_cliente_pelo_cnpj(cnpj_sem_filtro) is None:
            return redirect(url_for("cliente.cadastro", cnpj=cnpj))
    return render_template("cliente/precadastrocliente.html", form=form)

@cliente.route("/cadastro/<cnpj>", methods=["GET", "POST"])
@login_requisito
def cadastro(cnpj):
    dados = consultar(cnpj)
    if dados == 'Esperar 30 segundos':
        flash('Tente em 30 segundos')
        return redirect(url_for('cliente.precadastro'))
    elif dados['status'] == 'ERROR':
        flash('Cnpj invalido', 'danger')
        return redirect(url_for('cliente.precadastro'))
    form = CadastroClienteAPI()
    if form.validate_on_submit():
        nome =  form.nome.data
        nome_fantasia = form.nome_fantasia.data
        cnpj = form.cnpj.data
        data_entrada = form.data_entrada.data
        data_saida = form.data_saida.data
        novo_cliente = Cliente.registrar_salvar(nome,nome_fantasia,cnpj,data_entrada,data_saida)
        novo_cliente.cadastro_dados_adicional(dados)
        flash('Registro realizado com sucesso')
        return redirect(url_for("auth.home"))
    return render_template("cliente/cadastro.html",form=form,dados=dados)

@cliente.route("/cliente/<id_cliente>", methods=["GET", "POST"])
@login_requisito
def perfil_cliente(id_cliente):
    eventos = Calendario(id_cliente).query_cliente_informado()
    form = visualizacao_dados_cliente()
    p_cliente = Cliente.buscar_por_id(id_cliente)
    print(p_cliente)
    cnaes = p_cliente.Cnaes_do_cliente()
    endereço = p_cliente.Endrereco()
    contato = p_cliente.Contato()
    if request.method == 'POST' and form.submit.data:
        nome = form.nome.data
        nome_fantasia = form.nome_fantasia.data
        cnpj = form.cnpj.data
        data_entrada = form.data_entrada.data
        data_saida = form.data_saida.data
        telefone = form.telefone.data
        email = form.email.data
        cep = form.cep.data
        cidade = form.cidade.data
        estado = form.estado.data
        p_cliente.atualizar_pelo_formulario(nome,nome_fantasia,cnpj,data_entrada,data_saida,email,telefone,cep,cidade,estado)
        flash('Os dados do cliente foram editados','success')
        return redirect(url_for("cliente.lista_cliente", id_cliente=id_cliente))
    return render_template("cliente/perfil_cliente.html",form=form,dados_cliente=p_cliente,dados_cliente_endereco=endereço,dados_cliente_contato=contato,dados_cliente_cnaes=cnaes,eventos = eventos)


@cliente.route("/cliente/atualizar/<int:id_cliente>", methods=["GET"])
@login_requisito
def cliente_atualizar(id_cliente):
    p_cliente = Cliente.buscar_por_id(id_cliente)
    p_cliente.atualizar_dados_base()
    flash('Os dados do cliente foram atualizados com base na Api da receita','success')
    return redirect(url_for("cliente.lista_cliente", id_cliente=id_cliente))


@cliente.route("/deletar_cnae/<int:id_cnae>", methods=["GET"])
@login_requisito
def deletar_cnae(id_cnae):
    id_cliente = id_empresa_cnae(id_cnae)
    deletar_cnae_bd(id_cnae)
    return redirect(url_for("cliente.perfil_cliente", id_cliente=id_cliente))

@cliente.route("/clientes", methods=["GET", "POST"])
@login_requisito
def lista_cliente():
    dados = lista_cliente_db()
    return render_template("cliente/lista_cliente.html", dados=dados)

@cliente.route("/evento/<int:id_evento>", methods=["GET","POST"])
@login_requisito
def editar_evento(id_evento):
    calendario = Calendario().query_por_id_evento(id_evento)
    form = Editar_evento()
    if request.method == 'GET':
        form.status.data = str(calendario[0]['concluido'])
        form.data_entrega.data = datetime.strptime(calendario[0]['data_vencimento'], '%d/%m/%Y').date()
    if form.validate_on_submit():
        titulo = form.titulo.data
        descricao = form.descricao.data
        data_vencimento = form.data_entrega.data.strftime('%d/%m/%Y')
        status = form.status.data
        Calendario().editar_evento(titulo,descricao,data_vencimento,status,id_evento)
        return redirect(url_for("cliente.perfil_cliente", id_cliente=calendario[0]['id_cliente']))
    return render_template("cliente/perfil_evento.html", form=form ,dados=calendario)

@cliente.route("/deleta_evento/<int:id_evento>", methods=["POST"])
@login_requisito
def deleta_evento(id_evento):
    id_cliente = Calendario().query_por_id_evento(id_evento)[0]['id_cliente']
    deletar_evento(id_evento)
    return redirect(url_for("cliente.perfil_cliente", id_cliente=id_cliente))


@cliente.route("/cliente/<int:id_cliente>/criar_evento", methods=["GET", "POST"])
@login_requisito
def criar_evento(id_cliente):
    form = Criar_evento()
    if form.validate_on_submit():
        Calendario().adicionar_obrigações(
            form.titulo.data,
            form.descricao.data,
            form.data_entrega.data.strftime('%d/%m/%Y'),
            0,
            id_cliente
        )
        flash("Evento criado com sucesso!", "success")
        return redirect(url_for("cliente.perfil_cliente", id_cliente=id_cliente))
    return render_template("cliente/criar_evento.html",form=form,id_cliente=id_cliente)


@cliente.route("/calendario_consolidado", methods=["GET", "POST"])
@login_requisito
def calendario_consolidado():
    eventos = Calendario().query_todos_os_eventos()
    return render_template("cliente/calendario.html",eventos=eventos)


