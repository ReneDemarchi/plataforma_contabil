import sqlite3

def criar_banco():
    with sqlite3.connect("usuarios.db") as conexao:
        cursor = conexao.cursor()

        cursor.executescript("""
        PRAGMA foreign_keys = ON;

        /* ---------- Tabela de usuários ---------- */
        CREATE TABLE IF NOT EXISTS usuarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario     TEXT    NOT NULL UNIQUE,
            senha       TEXT    NOT NULL,
            email       TEXT,
            tipo        TEXT
        );

        /* ---------- Tabela de clientes ---------- */
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente    INTEGER PRIMARY KEY AUTOINCREMENT,
            nome          TEXT    NOT NULL UNIQUE,
            nome_fantasia TEXT    NOT NULL UNIQUE,
            cnpj          TEXT    UNIQUE,
            data_entrada  TEXT,
            data_saida    TEXT
        );

        /* ---------- CNAEs ---------- */
        CREATE TABLE IF NOT EXISTS cnaes (
            id_cnae     INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_cnae   TEXT    NOT NULL,
            codigo_cnae TEXT    NOT NULL,
            descricao   TEXT,
            id_cliente  INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );

        /* ---------- Contatos ---------- */
        CREATE TABLE IF NOT EXISTS contatos (
            id_contato  INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT,
            telefone    TEXT,
            id_cliente  INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );

        /* ---------- Endereços ---------- */
        CREATE TABLE IF NOT EXISTS enderecos (
            id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
            cep         TEXT,
            cidade      TEXT,
            estado      TEXT,
            id_cliente  INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );

        /* ---------- Obrigações por cliente ---------- */
        CREATE TABLE IF NOT EXISTS obrigacoes_clientes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo          TEXT    NOT NULL,
            descricao       TEXT,
            data_vencimento TEXT    NOT NULL,
            concluido       INTEGER DEFAULT 0,
            id_cliente      INTEGER NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        );
        """)

if __name__ == "__main__":
    criar_banco()
