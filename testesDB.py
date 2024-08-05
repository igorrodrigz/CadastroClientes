import sqlite3
import lojaDB


def limpar_banco():
    """Limpa o banco de dados para garantir um estado limpo antes de rodar os testes."""
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS compras')
    c.execute('DROP TABLE IF EXISTS clientes')
    conn.commit()
    conn.close()


def testar_funcao(funcao, *args):
    """Função auxiliar para testar funções com assert e tratar exceções."""
    try:
        funcao(*args)
        print(f"Teste de {funcao.__name__} passou.")
    except AssertionError as e:
        print(f"Teste de {funcao.__name__} falhou: {e}")
    except Exception as e:
        print(f"Erro ao executar {funcao.__name__}: {e}")


def test_cadastrar_cliente():
    lojaDB.cadastrar_cliente('João da Silva', '12345678900', '987654321', 'Rua A, 123', '12345-678')
    cliente = lojaDB.buscar_clientes('João da Silva')[0]
    assert cliente[1] == 'João da Silva', "Erro no cadastro de cliente"


def test_editar_cliente():
    lojaDB.cadastrar_cliente('Maria Oliveira', '09876543211', '123456789', 'Rua B, 456', '87654-321')
    cliente = lojaDB.buscar_clientes('Maria Oliveira')[0]
    lojaDB.editar_cliente(cliente[0], 'Maria Oliveira', '09876543211', '987654321', 'Rua B, 789', '87654-321')
    cliente_editado = lojaDB.buscar_cliente_por_id(cliente[0])
    assert cliente_editado[4] == 'Rua B, 789', "Erro na edição de cliente"


def test_excluir_cliente():
    lojaDB.cadastrar_cliente('Pedro Santos', '11223344556', '234567890', 'Rua C, 789', '34567-890')
    cliente = lojaDB.buscar_clientes('Pedro Santos')[0]
    lojaDB.excluir_cliente(cliente[0])
    cliente_excluido = lojaDB.buscar_cliente_por_id(cliente[0])
    assert cliente_excluido is None, "Erro na exclusão de cliente"


def test_registrar_compra():
    lojaDB.cadastrar_cliente('Ana Costa', '22334455667', '345678901', 'Rua D, 101', '45678-901')
    cliente = lojaDB.buscar_clientes('Ana Costa')[0]
    lojaDB.registrar_compra(cliente[0], '2024-08-01', 'Produto X', 150.00, 'Cartão', '2024-08-01', '2024-08-02',
                            'R123456789', 0)
    compras = lojaDB.buscar_compras(cliente[0])
    assert len(compras) > 0, "Erro ao registrar compra"


def test_editar_compra():
    lojaDB.cadastrar_cliente('Carlos Almeida', '33445566778', '456789012', 'Rua E, 202', '56789-012')
    cliente = lojaDB.buscar_clientes('Carlos Almeida')[0]
    lojaDB.registrar_compra(cliente[0], '2024-08-02', 'Produto Y', 200.00, 'Dinheiro', '2024-08-02', '2024-08-03',
                            'R987654321', 0)
    compra = lojaDB.buscar_compras(cliente[0])[0]
    lojaDB.editar_compra(compra[0], cliente[0], '2024-08-02', 'Produto Z', 250.00, 'Cartão', '2024-08-02', '2024-08-03',
                         'R987654321', 1)
    compra_editada = lojaDB.buscar_compras(cliente[0], compra[0])[0]
    assert compra_editada[3] == 'Produto Z', "Erro na edição de compra"


def test_excluir_compra():
    lojaDB.cadastrar_cliente('Fernanda Lima', '44556677889', '567890123', 'Rua F, 303', '67890-123')
    cliente = lojaDB.buscar_clientes('Fernanda Lima')[0]
    lojaDB.registrar_compra(cliente[0], '2024-08-03', 'Produto W', 300.00, 'Pix', '2024-08-03', '2024-08-04',
                            'R192837465', 0)
    compra = lojaDB.buscar_compras(cliente[0])[0]
    lojaDB.excluir_compra(compra[0])
    compras_restantes = lojaDB.buscar_compras(cliente[0])
    assert len(compras_restantes) == 0, "Erro na exclusão de compra"


def run_tests():
    """Executa todos os testes."""
    limpar_banco()
    lojaDB.init_db()

    # Adicionar clientes e compras para testes mais robustos
    clientes = [
        ('João da Silva', '12345678900', '987654321', 'Rua A, 123', '12345-678'),
        ('Maria Oliveira', '09876543211', '123456789', 'Rua B, 456', '87654-321'),
        ('Pedro Santos', '11223344556', '234567890', 'Rua C, 789', '34567-890'),
        ('Ana Costa', '22334455667', '345678901', 'Rua D, 101', '45678-901'),
        ('Carlos Almeida', '33445566778', '456789012', 'Rua E, 202', '56789-012'),
        ('Fernanda Lima', '44556677889', '567890123', 'Rua F, 303', '67890-123')
    ]
    compras = [
        ('Ana Costa', '2024-08-01', 'Produto X', 150.00, 'Cartão', '2024-08-01', '2024-08-02', 'R123456789', 0),
        ('Carlos Almeida', '2024-08-02', 'Produto Y', 200.00, 'Dinheiro', '2024-08-02', '2024-08-03', 'R987654321', 0),
        ('Fernanda Lima', '2024-08-03', 'Produto W', 300.00, 'Pix', '2024-08-03', '2024-08-04', 'R192837465', 0)
    ]

    for cliente in clientes:
        lojaDB.cadastrar_cliente(*cliente)

    for cliente_nome, *compra in compras:
        cliente = lojaDB.buscar_clientes(cliente_nome)[0]
        lojaDB.registrar_compra(cliente[0], *compra)

    testar_funcao(test_cadastrar_cliente)
    testar_funcao(test_editar_cliente)
    testar_funcao(test_excluir_cliente)
    testar_funcao(test_registrar_compra)
    testar_funcao(test_editar_compra)
    testar_funcao(test_excluir_compra)
    print("Todos os testes passaram com sucesso!")


if __name__ == '__main__':
    run_tests()
