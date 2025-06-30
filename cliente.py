from db import get_db_connection
from api import consultar


class Cliente:
    def __init__(self, id_cliente, nome, nome_fantasia, cnpj, data_entrada, data_saida):
        self.id = id_cliente
        self.nome = nome
        self.nome_fantasia = nome_fantasia
        self.cnpj = cnpj
        self.data_entrada = data_entrada
        self.data_saida = data_saida

    @classmethod
    def buscar_por_cnpj(cls, cnpj):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM clientes WHERE cnpj = ?;", (cnpj,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(**row)
        return None

    @classmethod
    def buscar_por_id(cls, id_cliente):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM clientes WHERE id_cliente = ?;", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(**row)
        return None

    @classmethod
    def listar_todos(cls):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM clientes;")
        rows = cursor.fetchall()
        conn.close()
        return [cls(**row) for row in rows]

    @classmethod
    def registrar_salvar(cls,nome,nome_fantasia,cnpj,data_entrada,data_saida):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO clientes (nome, nome_fantasia, cnpj, data_entrada, data_saida) VALUES (?, ?, ?, ?, ?)',
                (nome, nome_fantasia, cnpj, data_entrada, data_saida)
            )
            conn.commit()
            novo_id = cursor.lastrowid
            return cls.buscar_por_id(novo_id)
            return True
        except Exception as e:
            print(f"Erro ao salvar cliente: {e}")
            return False
        finally:
            conn.close()

    def Cnaes_do_cliente(self):
        conn = get_db_connection()
        cursor = conn.execute(
            "SELECT * FROM cnaes WHERE id_cliente = ?;",
            (self.id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def Endrereco(self):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM enderecos WHERE id_cliente = ?;", (self.id,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row

    def Contato(self):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM contatos WHERE id_cliente = ?;", (self.id,))
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return row

    def cadastro_dados_adicional(self,json_api):
        self.cadastrar_cnae_cliente(json_api)
        self.cadastrar_contato(json_api)
        self.cadastrar_endereco(json_api)



    def atualizar_dados_adicional(self,dados):
        self.deletar_contatos()
        self.deletar_cnaes()
        self.cadastro_dados_adicional(dados)

    def atualizar_dados_base(self):
        dados = consultar(self.cnpj.replace('.', '').replace('/', '').replace('-', ''))
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE clientes
            SET nome = ?, nome_fantasia = ?,cnpj = ?
            WHERE id_cliente = ?;
            """,
            (dados['nome'], dados['fantasia'],dados['cnpj'], self.id)
        )
        conn.commit()
        conn.close()
        self.atualizar_dados_adicional(dados)

    def deletar_cnaes(self):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM cnaes WHERE id_cliente = ?;",
            (self.id,)
        )
        conn.commit()
        conn.close()

    def cadastrar_cnae_cliente(self,json_api):
        conn = get_db_connection()
        cnaes_primario = json_api['atividade_principal']
        cnaes_secundario = json_api['atividades_secundarias']
        for cnae in cnaes_primario:
            tipo = 'Primario'
            codico = cnae['code']
            descri = cnae['text']
            conn.execute(
                'INSERT INTO cnaes (tipo_cnae, codigo_cnae, descricao, id_cliente) VALUES (?, ?, ?, ?)',
                (tipo, codico, descri, self.id)
            )
            conn.commit()
        for cnae in cnaes_secundario:
            tipo = 'Secundario'
            codico = cnae['code']
            descri = cnae['text']
            conn.execute(
                'INSERT INTO cnaes (tipo_cnae, codigo_cnae, descricao, id_cliente) VALUES (?, ?, ?, ?)',
                (tipo, codico, descri, self.id)
            )
            conn.commit()
        conn.close()

    def cadastrar_endereco(self,json_api):
        conn = get_db_connection()
        cep = json_api['cep']
        estado = json_api['uf']
        cidade = json_api['municipio']
        conn.execute(
            'INSERT INTO enderecos (cep, cidade, estado, id_cliente) VALUES (?, ?, ?, ?)',
            (cep, cidade, estado, self.id)
        )
        conn.commit()
        conn.close()

    def deletar_endereco(self):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM enderecos WHERE id_cliente = ?;",
            (self.id,)
        )
        conn.commit()
        conn.close()

    def cadastrar_contato(self,json_api):
        conn = get_db_connection()
        email = json_api['email']
        telefone = json_api['telefone']
        conn.execute(
            'INSERT INTO contatos (email, telefone, id_cliente) VALUES (?, ?, ?)',
            (email, telefone, self.id)
        )
        conn.commit()
        conn.close()

    def deletar_contatos(self):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM contatos WHERE id_cliente = ?;",
            (self.id,)
        )
        conn.commit()
        conn.close()

    def deletar_cliente(self):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM clientes WHERE id_cliente = ?;",
            (self.id,)
        )
        conn.commit()
        conn.close()

    def atualizar_pelo_formulario(self,nome,nome_fantasia,cnpj,data_entrada,data_saida,email,telefone,cep,cidade,estado):
        self.__at_dados_base_formulario(nome,nome_fantasia,cnpj,data_entrada,data_saida)
        self.__at_dados_contato_formulario(email,telefone)
        self.__at_dados_endereco_formulario(cep,cidade,estado)

    def __at_dados_base_formulario(self,nome,nome_fantasia,cnpj,data_entrada,data_saida):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE clientes
            SET nome = ?, nome_fantasia = ?,cnpj = ?,data_entrada = ?,data_saida = ?
            WHERE id_cliente = ?;
            """,
            (nome, nome_fantasia, cnpj, data_entrada, data_saida, self.id)
        )
        conn.commit()
        conn.close()

    def __at_dados_contato_formulario(self,email,telefone):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE contatos
            SET email = ?, telefone = ?
            WHERE id_cliente = ?;
            """,
            (email, telefone, self.id)
        )
        conn.commit()
        conn.close()


    def __at_dados_endereco_formulario(self,cep,cidade,estado):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE enderecos
            SET cep = ?, cidade = ?, estado = ?
            WHERE id_cliente = ?;
            """,
            (cep,cidade,estado, self.id)
        )
        conn.commit()
        conn.close()


if __name__ == '__main__':
    a = Cliente.buscar_por_id(7)
    a.atualizar_pelo_formulario("nome","nome_fantasia",'456123789','12/12/2021','12/05/2024','rene@hotmail','48 998329244','88080401','floripa','sc')
