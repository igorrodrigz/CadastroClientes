import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout
from PyQt5.QtCore import Qt
from lojaDB import init_db, cadastrar_cliente, editar_cliente, excluir_cliente, buscar_clientes, buscar_cliente_por_id
from client_window import ClientWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Controle de Clientes')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Barra de busca
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar Cliente")
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar_cliente)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Lista de clientes
        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(6)
        self.table_clientes.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone", "Endereço", "CEP"])
        self.table_clientes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_clientes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_clientes.doubleClicked.connect(self.abrir_cliente)

        # Botões
        button_layout = QHBoxLayout()
        self.button_add_cliente = QPushButton("Adicionar Cliente")
        self.button_edit_cliente = QPushButton("Editar Cliente")
        self.button_delete_cliente = QPushButton("Excluir Cliente")
        self.button_acessar_cliente = QPushButton("Acessar Cliente")

        self.button_add_cliente.clicked.connect(self.adicionar_cliente)
        self.button_edit_cliente.clicked.connect(self.editar_cliente)
        self.button_delete_cliente.clicked.connect(self.excluir_cliente)
        self.button_acessar_cliente.clicked.connect(self.abrir_cliente)

        button_layout.addWidget(self.button_add_cliente)
        button_layout.addWidget(self.button_edit_cliente)
        button_layout.addWidget(self.button_delete_cliente)
        button_layout.addWidget(self.button_acessar_cliente)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table_clientes)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_clientes()

    def load_clientes(self):
        clientes = buscar_clientes()
        self.table_clientes.setRowCount(len(clientes))
        for row_idx, cliente in enumerate(clientes):
            for col_idx, value in enumerate(cliente):
                item = QTableWidgetItem(str(value))
                self.table_clientes.setItem(row_idx, col_idx, item)

    def buscar_cliente(self):
        search_term = self.search_input.text()
        clientes = buscar_clientes(search_term)
        self.table_clientes.setRowCount(len(clientes))
        for row_idx, cliente in enumerate(clientes):
            for col_idx, value in enumerate(cliente):
                item = QTableWidgetItem(str(value))
                self.table_clientes.setItem(row_idx, col_idx, item)

    def adicionar_cliente(self):
        dialog = ClientDialog(self)
        if dialog.exec_():
            self.load_clientes()

    def editar_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            client_id = self.table_clientes.item(selected_row, 0).text()
            client_data = buscar_cliente_por_id(client_id)
            dialog = ClientDialog(self, client_data)
            if dialog.exec_():
                self.load_clientes()

    def excluir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            client_id = self.table_clientes.item(selected_row, 0).text()
            excluir_cliente(client_id)
            self.load_clientes()

    def abrir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            client_id = self.table_clientes.item(selected_row, 0).text()
            self.client_window = ClientWindow(client_id)
            self.client_window.show()

class ClientDialog(QDialog):
    def __init__(self, parent=None, client_data=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Cliente" if client_data is None else "Editar Cliente")
        self.client_data = client_data
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.input_nome = QLineEdit()
        self.input_cpf = QLineEdit()
        self.input_telefone = QLineEdit()
        self.input_endereco = QLineEdit()
        self.input_cep = QLineEdit()

        if self.client_data:
            self.input_nome.setText(self.client_data[1])
            self.input_cpf.setText(self.client_data[2])
            self.input_telefone.setText(self.client_data[3])
            self.input_endereco.setText(self.client_data[4])
            self.input_cep.setText(self.client_data[5])

        layout.addRow("Nome:", self.input_nome)
        layout.addRow("CPF:", self.input_cpf)
        layout.addRow("Telefone:", self.input_telefone)
        layout.addRow("Endereço:", self.input_endereco)
        layout.addRow("CEP:", self.input_cep)

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save_client)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def save_client(self):
        nome = self.input_nome.text()
        cpf = self.input_cpf.text()
        telefone = self.input_telefone.text()
        endereco = self.input_endereco.text()
        cep = self.input_cep.text()

        if self.client_data:
            editar_cliente(self.client_data[0], nome, cpf, telefone, endereco, cep)
        else:
            cadastrar_cliente(nome, cpf, telefone, endereco, cep)

        self.accept()

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
