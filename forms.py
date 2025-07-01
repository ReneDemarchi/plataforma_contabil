from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField,DateField
from wtforms.validators import DataRequired, Length, InputRequired,  Optional

class CadastroUsuarioForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class Editar_usuario(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Editar')

class Trocar_senha_usuario(FlaskForm):
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Trocar Senha')

class Deletar_usuario_botao(FlaskForm):
    submit = SubmitField('Deletar Usuario')

class precadastroo(FlaskForm):
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(min=18, max=18)])
    submit = SubmitField('Buscar dados Api')

class Sair(FlaskForm):
    botao_sair = SubmitField('Sair')

class CadastroClienteAPI(FlaskForm):
    nome           = StringField('Nome',           validators=[DataRequired(), Length(min=3, max=150)])
    nome_fantasia  = StringField('Nome Fantasia',  validators=[DataRequired(), Length(min=3, max=150)])
    cnpj           = StringField('CNPJ',           validators=[DataRequired(), Length(min=14, max=18)])
    data_entrada   = DateField('Data de entrada',format='%Y-%m-%d',validators=[DataRequired()])
    data_saida     = DateField('Data de saída',format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class visualizacao_dados_cliente(FlaskForm):
    nome = StringField('Nome', validators=[Length(min=3, max=150)])
    nome_fantasia = StringField('Nome Fantasia')
    cnpj = StringField('CNPJ', validators=[Length(min=14, max=18)])
    data_entrada = DateField('Data de entrada', format='%Y-%m-%d', validators=[], default=None)
    data_saida = DateField('Data de saída', format='%Y-%m-%d', validators=[], default=None)
    telefone = StringField('Telefone', validators=[Length(min=3, max=150)])
    email = StringField('Email')
    cep = StringField('Cep', validators=[Length(min=3, max=25)])
    cidade = StringField('Cidade', validators=[Length(min=3, max=25)])
    estado = StringField('Estado', validators=[Length(min=3, max=25)])
    submit = SubmitField('Editar')


class Criar_evento(FlaskForm):
    titulo = StringField('titulo', validators=[Length(min=3, max=150)])
    descrição = StringField('descrição', validators=[Length(min=3, max=150)])
    data_entrega = DateField('Data de entrega', format='%d/%m/%Y', validators=[], default=None)
    id_cliente = StringField('Nome',validators=[Optional(),Length(max=9)])


class Editar_evento(FlaskForm):
    titulo = StringField('titulo', validators=[Length(min=3, max=150)])
    descricao = StringField('descrição', validators=[Length(min=3, max=150)])
    data_entrega = DateField('Data de Entrega', format='%Y-%m-%d')
    id_cliente = StringField('Nome', validators=[Optional(), Length(max=9)])
    status = SelectField(
        'Status da Entrega',
        choices=[('0', 'Não enviado'), ('1', 'Entregue')]
    )
    submit = SubmitField('Editar')
