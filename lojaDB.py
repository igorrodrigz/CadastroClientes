import sqlite3

def init_db():
    """Inicializa o banco de dados e cria as tabelas, se ainda não existirem."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        # Criação ou atualização da tabela clientes
        c.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                proprietario TEXT NOT NULL,
                raca TEXT NOT NULL,
                endereco TEXT NOT NULL,
                Telefone TEXT NOT NULL
            )
        ''')
        # Criação da tabela compras
        c.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data_venda TEXT NOT NULL,
                produto TEXT NOT NULL,
                valor_venda REAL NOT NULL,
                notas TEXT,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id)
            )
        ''')
        conn.commit()
        print("Banco de dados e tabelas criados com sucesso.")
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conn.close()

def cadastrar_cliente(nome, proprietario, raca, endereco, telefone):
    """Cadastra um novo cliente no banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO clientes (nome, proprietario, raca, endereco, telefone) VALUES (?, ?, ?, ?, ?)
        ''', (nome, proprietario, raca, endereco, telefone))
        conn.commit()
        print("Cliente cadastrado com sucesso.")
    except Exception as e:
        print(f"Erro ao cadastrar cliente: {e}")
    finally:
        conn.close()

def editar_cliente(client_id, nome, proprietario, raca, endereco, telefone):
    """Edita os dados de um cliente existente no banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''
            UPDATE clientes SET nome = ?, proprietario = ?, raca = ?, endereco = ?, telefone = ? WHERE id = ?
        ''', (nome, proprietario, raca, endereco, telefone, client_id))
        conn.commit()
        print("Cliente editado com sucesso.")
    except Exception as e:
        print(f"Erro ao editar cliente: {e}")
    finally:
        conn.close()

def excluir_cliente(client_id):
    """Exclui um cliente e suas compras associadas do banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('DELETE FROM compras WHERE cliente_id = ?', (client_id,))
        c.execute('DELETE FROM clientes WHERE id = ?', (client_id,))
        conn.commit()
        print("Cliente e suas compras excluídos com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")
    finally:
        conn.close()

def buscar_clientes(search_term=None):
    """Busca clientes no banco de dados com base no termo de pesquisa fornecido."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        if search_term:
            c.execute('''
                SELECT * FROM clientes WHERE nome LIKE ? OR proprietario LIKE ? OR telefone LIKE ?
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        else:
            c.execute('SELECT * FROM clientes')
        clientes = c.fetchall()
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        clientes = []
    finally:
        conn.close()
    return clientes

def buscar_cliente_por_id(client_id):
    """Busca um cliente pelo ID no banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM clientes WHERE id = ?', (client_id,))
        cliente = c.fetchone()
    except Exception as e:
        print(f"Erro ao buscar cliente por ID: {e}")
        cliente = None
    finally:
        conn.close()
    return cliente

def buscar_clientes_com_itens_nao_enviados():
    """Busca clientes que possuem itens (ou compras) não enviados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''
            SELECT DISTINCT cl.id, cl.nome, cl.proprietario, cl.raca, cl.endereco, cl.telefone
            FROM clientes cl
            JOIN compras co ON cl.id = co.cliente_id
            WHERE co.enviado = 0
        ''')
        clientes = c.fetchall()
    except Exception as e:
        print(f"Erro ao buscar clientes com itens não enviados: {e}")
        clientes = []
    finally:
        conn.close()
    return clientes


def registrar_compra(cliente_id, data_venda, produto, valor_venda, notas=None):
    """Registra uma nova compra no banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()

        # Verifique os dados que estão sendo inseridos
        print(f"Registrando nova compra para cliente_id {cliente_id}:")
        print(f"data_venda: {data_venda}, produto: {produto}, valor_venda: {valor_venda}, notas: {notas}")

        # Comando SQL para inserir a compra
        c.execute('''
            INSERT INTO compras (cliente_id, data_venda, produto, valor_venda, notas)
            VALUES (?, ?, ?, ?, ?)
        ''', (cliente_id, data_venda, produto, valor_venda, notas))

        # Commitar a transação para salvar no banco
        conn.commit()
        print("Compra registrada com sucesso.")
    except Exception as e:
        print(f"Erro ao registrar compra: {e}")
    finally:
        conn.close()


def editar_compra(compra_id, data_venda, produto, valor_venda, notas=None):
    """Edita uma compra existente no banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''
            UPDATE compras
            SET data_venda = ?, produto = ?, valor_venda = ?, notas = ?
            WHERE id = ?
        ''', (data_venda, produto, valor_venda, notas, compra_id))
        conn.commit()
        print("Compra editada com sucesso.")
    except Exception as e:
        print(f"Erro ao editar compra: {e}")
    finally:
        conn.close()

def excluir_compra(compra_id):
    """Exclui uma compra do banco de dados."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('DELETE FROM compras WHERE id = ?', (compra_id,))
        conn.commit()
        print(f"Compra com ID {compra_id} excluída com sucesso.")
    except Exception as e:
        print(f"Erro ao excluir compra: {e}")
    finally:
        conn.close()

def buscar_compras(cliente_id, compra_id=None):
    """Busca compras para um cliente com base no ID da compra opcional."""
    try:
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        if compra_id:
            c.execute('SELECT * FROM compras WHERE cliente_id = ? AND id = ?', (cliente_id, compra_id))
        else:
            c.execute('SELECT * FROM compras WHERE cliente_id = ?', (cliente_id,))
        compras = c.fetchall()
    except Exception as e:
        print(f"Erro ao buscar compras: {e}")
        compras = []
    finally:
        conn.close()
    return compras

if __name__ == '__main__':
    init_db()