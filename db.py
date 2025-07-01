import sqlite3



def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_usuario(usuario, senha_hash, email, tipo):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO usuarios (usuario, senha, email, tipo) VALUES (?, ?, ?, ?)',
        (usuario, senha_hash, email, tipo)
    )
    conn.commit()
    conn.close()

def dados_usuario_id(id_usuario):
    """Dados do usuário pelo ID."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT FROM usuarios WHERE id = ?;",
        (id_usuario,)
    )
    conn.commit()
    conn.close()
    return user

def editar_usuario(id_usuario, nome_usuario, senha_hash, email):
    """Atualiza nome, e-mail, senha e tipo de um usuário existente."""
    conn = get_db_connection()
    conn.execute(
        """
        UPDATE usuarios
        SET usuario = ?, senha = ?, email = ?
        WHERE id = ?;
        """,
        (nome_usuario, senha_hash, email, id_usuario)
    )
    conn.commit()
    conn.close()

def deletar_usuario(id_usuario):
    """Remove definitivamente um usuário pelo ID."""
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM usuarios WHERE id = ?;",
        (id_usuario,)
    )
    conn.commit()
    conn.close()

def registrar_cliente(nome,nome_fantasia,cnpj,data_entrada,data_saida):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO clientes (nome, nome_fantasia, cnpj, data_entrada, data_saida) VALUES ( ?, ?, ?, ?, ?)',
            (nome,nome_fantasia,cnpj,data_entrada,data_saida)
        )
        conn.commit()
        conn.close()
        return True
    except:
        return False

def id_cliente_pelo_cnpj(cnpj):
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT id_cliente FROM clientes WHERE cnpj = ?;", (cnpj,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row['id_cliente']
    except sqlite3.Error as e:
        print(e)
        return None


def cadastrar_cnae_cliente(json_api,id_cliente):
    conn = get_db_connection()
    cnaes_primario = json_api['atividade_principal']
    cnaes_secundario = json_api['atividades_secundarias']
    for cnae in cnaes_primario:
        tipo = 'Primario'
        codico = cnae['code']
        descri = cnae['text']
        conn.execute(
            'INSERT INTO cnaes (tipo_cnae, codigo_cnae, descricao, id_cliente) VALUES (?, ?, ?, ?)',
            (tipo,codico,descri, id_cliente)
        )
        conn.commit()
    for cnae in cnaes_secundario:
        tipo = 'Secundario'
        codico = cnae['code']
        descri = cnae['text']
        conn.execute(
            'INSERT INTO cnaes (tipo_cnae, codigo_cnae, descricao, id_cliente) VALUES (?, ?, ?, ?)',
            (tipo, codico, descri, id_cliente)
        )
        conn.commit()
    conn.close()

def cadastrar_contato_cliente(json_api,id_cliente):
    conn = get_db_connection()
    email = json_api['email']
    telefone = json_api['telefone']
    conn.execute(
        'INSERT INTO contatos (email, telefone, id_cliente) VALUES (?, ?, ?)',
        (email, telefone, id_cliente)
    )
    conn.commit()
    conn.close()

def cadastrar_endereco_cliente(json_api,id_cliente):
    conn = get_db_connection()
    cep = json_api['cep']
    estado = json_api['uf']
    cidade = json_api['municipio']
    conn.execute(
        'INSERT INTO enderecos (cep, cidade, estado, id_cliente) VALUES (?, ?, ?, ?)',
        (cep,cidade,estado, id_cliente)
    )
    conn.commit()
    conn.close()


def dados_base_cliente_pelo_id(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM clientes WHERE id_cliente = ?;", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row
    except sqlite3.Error as e:
        print(e)
        return None

def dados_endereco_cliente_pelo_id(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM enderecos WHERE id_cliente = ?;", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row
    except sqlite3.Error as e:
        print(e)
        return None

def dados_contatos_cliente_pelo_id(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM contatos WHERE id_cliente = ?;", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row
    except sqlite3.Error as e:
        print(e)
        return None

def dados_cnaes_cliente_pelo_id(id_cliente):
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT * FROM cnaes WHERE id_cliente = ?;",
            (id_cliente,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(e)
        return None

def id_empresa_cnae(id_cnae):
    conn = get_db_connection()
    cursor = conn.execute("SELECT id_cliente FROM cnaes WHERE id_cnae = ?;", (id_cnae,))
    row = cursor.fetchone()
    conn.close()
    return row['id_cliente']

def deletar_cnae_bd(id_cnae):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM cnaes WHERE id_cnae = ?;",
        (id_cnae,)
    )
    conn.commit()
    conn.close()

def lista_cliente_db():
    try:
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT * FROM clientes ;",
            ()
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(e)
        return None

def deletar_evento(id_evento):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM obrigacoes_clientes WHERE id = ?;",
        (id_evento,)
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    pass