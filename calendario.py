from db import get_db_connection

class Calendario:
    def __init__(self,id_cliente = None):
        self.id_cliente = id_cliente
        self.lista = []
    def query_cliente_informado(self):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM obrigacoes_clientes WHERE id_cliente = ?;", (self.id_cliente,))
        colunas = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        lista_dicionarios = []
        for row in rows:
            lista_dicionarios.append(dict(zip(colunas, row)))
        conn.close()
        if lista_dicionarios:
            self.lista = lista_dicionarios
            return lista_dicionarios
        return []
    def query_todos_os_eventos(self):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM obrigacoes_clientes;")  # Remover o filtro WHERE id_cliente = ?
        colunas = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        lista_dicionarios = []
        for row in rows:
            lista_dicionarios.append(dict(zip(colunas, row)))
        conn.close()
        if lista_dicionarios:
            self.lista = lista_dicionarios
            return lista_dicionarios
        return None

    def query_por_id_evento(self,id_evento):
        conn = get_db_connection()
        cursor = conn.execute("SELECT * FROM obrigacoes_clientes WHERE id = ?;", (id_evento,))
        colunas = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        lista_dicionarios = []
        for row in rows:
            lista_dicionarios.append(dict(zip(colunas, row)))
        conn.close()
        if lista_dicionarios:
            self.lista = lista_dicionarios
            return lista_dicionarios
        return None

    def adicionar_obrigações(self,titulo,descrição,data_vencimento,concluido,id_cliente):
        conn = get_db_connection()
        print('refsdfsdfsd')
        cursor = conn.execute("SELECT COUNT(*) FROM clientes WHERE id_cliente = ?", (id_cliente,))
        cliente_existe = cursor.fetchone()[0] > 0
        if not cliente_existe:
            print(f"Erro: Cliente com ID {id_cliente} não encontrado!")
            conn.close()
            return 'Erro'
        conn.execute(
            'INSERT INTO obrigacoes_clientes (titulo, descricao, data_vencimento, concluido, id_cliente) VALUES (?, ?, ?, ?, ?)',
            (titulo,descrição,data_vencimento,concluido,id_cliente)
        )
        conn.commit()
    def editar_evento(self,titulo, descricao, data_vencimento, concluido,id):
        conn = get_db_connection()
        print(data_vencimento)
        conn.execute("""
            UPDATE obrigacoes_clientes
            SET titulo = ?, descricao = ?, data_vencimento = ?, concluido = ?
            WHERE id = ?;
        """, (titulo, descricao, data_vencimento, concluido, id))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    query = Calendario(1).adicionar_obrigações('CND','rene','02/07/2025',1,1)
    print(query)