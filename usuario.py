from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id, usuario, email, tipo):
        self.id = id
        self.usuario = usuario
        self.email = email
        self.tipo = tipo

    @classmethod
    def buscar_por_id(cls, id_usuario):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,)).fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["usuario"], row["email"], row["tipo"])
        return None

    @classmethod
    def buscar_por_nome(cls, usuario):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,)).fetchone()
        conn.close()
        if row:
            return cls(row["id"], row["usuario"], row["email"], row["tipo"]), row["senha"]
        return None, None

    @classmethod
    def criar(cls, usuario, senha, email, tipo):
        senha_hash = generate_password_hash(senha)
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO usuarios (usuario, senha, email, tipo) VALUES (?, ?, ?, ?)',
                (usuario, senha_hash, email, tipo)
            )
            conn.commit()
            novo_id = cursor.lastrowid
            return cls(novo_id, usuario, email, tipo)
        except Exception as e:
            print("Erro ao criar usuário:", e)
            return None
        finally:
            conn.close()

    def atualizar(self, novo_usuario, novo_email):
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE usuarios
            SET usuario = ?, email = ?
            WHERE id = ?;
            """,
            (novo_usuario, novo_email, self.id)
        )
        conn.commit()
        conn.close()

    def trocar_senha(self,senha):
        senha_hash = generate_password_hash(senha)
        conn = get_db_connection()
        conn.execute(
            """
            UPDATE usuarios
            SET senha = ?
            WHERE id = ?;
            """,
            (senha_hash, self.id)
        )
        conn.commit()
        conn.close()

    def deletar(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM usuarios WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
