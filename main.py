import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QTabWidget, QFrame)
from PyQt5.QtCore import Qt
from lojaDB import init_db
from lojaDB import (cadastrar_cliente, editar_cliente, excluir_cliente, buscar_clientes,
                    buscar_cliente_por_id, buscar_clientes_com_itens_nao_enviados)
from client_window import ClientWindow
import random

def carregar_estilos(app, caminho_qss):
    """Carrega os estilos do arquivo QSS no aplicativo."""
    try:
        with open(caminho_qss, "r") as arquivo_estilos:
            app.setStyleSheet(arquivo_estilos.read())
    except FileNotFoundError:
        QMessageBox.warning(None, "Aviso", f"Arquivo de estilos não encontrado: {caminho_qss}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema de Controle de Clientes - Bem Banhado Pet Shop')
        self.setGeometry(100, 100, 900, 600)
        self.initUI()

        self.showMaximized()
    def initUI(self):
        main_layout = QVBoxLayout()
        init_db()

        #ali

        # Adicionar uma aba para clientes
        self.tabs = QTabWidget()
        self.tab_clientes = QWidget()
        self.tabs.addTab(self.tab_clientes, "Clientes")

        # Configurar a aba de clientes
        self.tab_clientes_layout = QVBoxLayout()

        # Busca de clientes
        self.search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar Cliente")
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar_cliente)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.tab_clientes_layout.addLayout(self.search_layout)

        # Tabela de clientes
        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(6)
        self.table_clientes.setHorizontalHeaderLabels(
            ["ID", "Nome", "Proprietario", "Raça", "Endereço", "Telefone"]
        )
        self.table_clientes.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_clientes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_clientes.doubleClicked.connect(self.abrir_cliente)
        self.tab_clientes_layout.addWidget(self.table_clientes)

        # Botões CRUD
        self.button_layout = QHBoxLayout()
        self.btn_adicionar = QPushButton("Adicionar Cliente")
        self.btn_editar = QPushButton("Editar Cliente")
        self.btn_excluir = QPushButton("Excluir Cliente")
        self.btn_acessar = QPushButton("Acessar Cliente")

        self.btn_adicionar.clicked.connect(self.adicionar_cliente)
        self.btn_editar.clicked.connect(self.editar_cliente)
        self.btn_excluir.clicked.connect(self.excluir_cliente)
        self.btn_acessar.clicked.connect(self.abrir_cliente)

        self.button_layout.addWidget(self.btn_adicionar)
        self.button_layout.addWidget(self.btn_editar)
        self.button_layout.addWidget(self.btn_excluir)
        self.button_layout.addWidget(self.btn_acessar)

        self.tab_clientes_layout.addLayout(self.button_layout)

        # Definir layout da aba de clientes
        self.tab_clientes.setLayout(self.tab_clientes_layout)

        # Adicionar abas ao layout principal
        main_layout.addWidget(self.tabs)

        # Frase motivacional e rodapé
        self.footer_frame = QFrame()
        self.footer_frame.setFrameShape(QFrame.StyledPanel)
        self.footer_layout = QVBoxLayout()

        #aqui
        self.horizontal_layout = QHBoxLayout()
        # logo
        logo_label = QLabel(self)
        pixmap = QPixmap("LogoBBx.png")
        pixmap = pixmap.scaled(142, 63)
        logo_label.setPixmap(pixmap)  # Define a image no QLabel
        logo_label.setFixedSize(142, 63)
        self.footer_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        self.motivational_phrases = [
            "A perseverança é a chave para o sucesso.",
            "Transforme seus desafios em oportunidades.",
            "Acreditar em si mesmo é o primeiro passo para o sucesso.",
            "Cada dia é uma nova chance para brilhar.",
            "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
            "A diferença entre um sonho e um objetivo é uma data.",
        ]
        self.motivational_label = QLabel(self.get_random_phrase())
        self.horizontal_layout.addWidget(self.motivational_label, alignment=Qt.AlignCenter)

        self.footer_layout.addLayout(self.horizontal_layout) #Adiciona o layout horizontal ao rodapé

        self.footer_signature = QLabel(
            "Software Exclusivo de Bem Banhado Pet Shop - Desenvolvido por MR Solutions.")
        self.footer_layout.addWidget(self.footer_signature, alignment=Qt.AlignCenter)

        self.footer_frame.setLayout(self.footer_layout)
        main_layout.addWidget(self.footer_frame)

        self.setLayout(main_layout)
        self.load_clientes()

        #self.load_itens_nao_enviados()

    def get_random_phrase(self):
        return random.choice(self.motivational_phrases)

    def load_clientes(self):
        clientes = buscar_clientes()
        self.table_clientes.setRowCount(len(clientes))
        for row_idx, cliente in enumerate(clientes):
            for col_idx, value in enumerate(cliente):
                item = QTableWidgetItem(str(value))
                self.table_clientes.setItem(row_idx, col_idx, item)

    #def load_itens_nao_enviados(self):
    #    clientes = buscar_clientes_com_itens_nao_enviados()
    #    self.table_itens_nao_enviados.setRowCount(len(clientes))
    #    for row_idx, cliente in enumerate(clientes):
    #        for col_idx, value in enumerate(cliente):
    #            item = QTableWidgetItem(str(value))
    #            self.table_itens_nao_enviados.setItem(row_idx, col_idx, item)

    def buscar_cliente(self):
        search_term = self.search_input.text()
        #self.load_itens_nao_enviados()
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
            client_id = int(self.table_clientes.item(selected_row, 0).text())
            client_data = buscar_cliente_por_id(client_id)
            if client_data:
                dialog = ClientDialog(self, client_data)
                if dialog.exec_():
                    self.load_clientes()
            else:
                QMessageBox.warning(self, "Aviso", "Cliente não encontrado.")

    def excluir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            client_id = int(self.table_clientes.item(selected_row, 0).text())

            #Confirma excluir cliente
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Tem certeza que deseja apagar este cliente?")
            msg_box.setInformativeText(f"O cliente com o ID {client_id} será permanentemente excluido.")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            response = msg_box.exec_()
            if response == QMessageBox.Yes:
                try:
                    excluir_cliente(client_id)
                    print(f"Cliente com id {client_id} excluido com sucesso.")
                    self.load_clientes()
                except Exception as e:
                    print(f"Erro ao excluir cliente: {e}")
            else:
                print("Exclusão do cliente cancelada.")
        else:
            print("Nenhum cliente selecionado para exclusão.")

    def abrir_cliente(self):
        selected_row = self.table_clientes.currentRow()
        if selected_row != -1:
            client_id = int(self.table_clientes.item(selected_row, 0).text())
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
        self.input_proprietario = QLineEdit()
        self.input_raca = QLineEdit()
        self.input_endereco = QLineEdit()
        self.input_telefone = QLineEdit()
        #self.input_cidade = QLineEdit()  # Novo campo para cidade

        if self.client_data:
            self.input_nome.setText(self.client_data[1])
            self.input_proprietario.setText(self.client_data[2])
            self.input_raca.setText(self.client_data[3])
            self.input_endereco.setText(self.client_data[4])
            self.input_telefone.setText(self.client_data[5])
            #self.input_cidade.setText(self.client_data[6])  # Carregar cidade se estiver editando

        layout.addRow("Nome:", self.input_nome)
        layout.addRow("Proprietario:", self.input_proprietario)
        layout.addRow("Raca:", self.input_raca)
        layout.addRow("Endereço:", self.input_endereco)
        layout.addRow("Telefone:", self.input_telefone)
        #layout.addRow("Cidade:", self.input_cidade)  # Adicionar campo cidade

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save_client)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def save_client(self):
        nome = self.input_nome.text()
        proprietario = self.input_proprietario.text()
        raca = self.input_raca.text()
        endereco = self.input_endereco.text()
        telefone = self.input_telefone.text()
        #cidade = self.input_cidade.text()  # Adicionar cidade

        if self.client_data:
            client_id = self.client_data[0]
            editar_cliente(client_id, nome, proprietario, raca, endereco, telefone)  # Passar cidade
        else:
            cadastrar_cliente(nome, proprietario, raca, endereco, telefone)  # Passar cidade

        self.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    carregar_estilos(app, 'styles.qss')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())