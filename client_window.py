import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QFormLayout, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt, QDate
from lojaDB import buscar_compras, registrar_compra, editar_compra, excluir_compra
from utils import criar_seletor_data


class ClientWindow(QWidget):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        self.setWindowTitle('Detalhes do Cliente')
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Lista de compras
        self.table_compras = QTableWidget()
        self.table_compras.setColumnCount(8)  # Atualizar o número de colunas
        self.table_compras.setHorizontalHeaderLabels(
            ["Número Item", "ID", "Data da Venda", "Produto", "Data de Pagamento", "Data de Envio",
             "Código de Rastreio", "Enviado?"])
        self.table_compras.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_compras.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajustar largura das colunas
        self.table_compras.resizeColumnsToContents()

        # Botões
        button_layout = QHBoxLayout()
        self.button_add_compra = QPushButton("Adicionar Compra")
        self.button_edit_compra = QPushButton("Editar Compra")
        self.button_delete_compra = QPushButton("Excluir Compra")

        self.button_add_compra.clicked.connect(self.adicionar_compra)
        self.button_edit_compra.clicked.connect(self.editar_compra)
        self.button_delete_compra.clicked.connect(self.excluir_compra)

        button_layout.addWidget(self.button_add_compra)
        button_layout.addWidget(self.button_edit_compra)
        button_layout.addWidget(self.button_delete_compra)

        main_layout.addWidget(self.table_compras)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_compras()
        self.table_compras.resizeColumnsToContents()  # Ajustar após carregar os dados

    def load_compras(self):
        compras = buscar_compras(self.client_id)
        print(f"Compras carregadas: {compras}")
        self.table_compras.setRowCount(len(compras))
        for row_idx, compra in enumerate(compras):
            for col_idx, value in enumerate(compra[:-1]):
                item = QTableWidgetItem(str(value))
                self.table_compras.setItem(row_idx, col_idx, item)

            enviado_checkbox = QTableWidgetItem()
            enviado_checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            enviado_checkbox.setCheckState(Qt.Checked if compra[-1] else Qt.Unchecked)
            self.table_compras.setItem(row_idx, len(compra) - 1, enviado_checkbox)

    def adicionar_compra(self):
        dialog = CompraDialog(self, self.client_id)
        if dialog.exec_():
            self.load_compras()

    def editar_compra(self):
        selected_row = self.table_compras.currentRow()
        if selected_row != -1:
            compra_id_item = self.table_compras.item(selected_row, 0)  # Coluna 1 é o ID
            if compra_id_item:
                compra_id = compra_id_item.text()
                print(f"ID da compra selecionada: {compra_id}")
                compra_data = buscar_compras(self.client_id, compra_id)
                print(f"Dados da compra: {compra_data}")
                if compra_data:
                    compra_data = compra_data[0]
                    dialog = CompraDialog(self, self.client_id, compra_data)
                    if dialog.exec_():
                        self.load_compras()
                else:
                    print(f"Nenhuma compra encontrada com o ID: {compra_id}")
            else:
                print("O item da célula não contém um ID válido.")

    def excluir_compra(self):
        selected_row = self.table_compras.currentRow()
        if selected_row != -1:
            compra_id = self.table_compras.item(selected_row, 1).text()  # Ajustar para pegar o ID correto
            excluir_compra(compra_id)
            self.load_compras()


class CompraDialog(QDialog):
    def __init__(self, parent=None, client_id=None, compra_data=None):
        super().__init__(parent)
        self.client_id = client_id
        self.compra_data = compra_data
        self.setWindowTitle("Adicionar Compra" if compra_data is None else "Editar Compra")
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        self.input_data_venda = criar_seletor_data()
        self.input_produto = QLineEdit()
        self.input_data_pagamento = criar_seletor_data()
        self.input_data_envio = criar_seletor_data()
        self.input_codigo_rastreio = QLineEdit()
        self.checkbox_enviado = QCheckBox()

        if self.compra_data:
            # Certifique-se de que os dados são strings e estão no formato correto
            self.input_data_venda.setDate(QDate.fromString(str(self.compra_data[2]), 'dd-MM-yyyy'))
            self.input_produto.setText(self.compra_data[3])
            self.input_data_pagamento.setDate(QDate.fromString(str(self.compra_data[4]), 'dd-MM-yyyy'))
            self.input_data_envio.setDate(QDate.fromString(str(self.compra_data[5]), 'dd-MM-yyyy'))
            self.input_codigo_rastreio.setText(self.compra_data[6])
            self.checkbox_enviado.setChecked(bool(self.compra_data[7]))  # Verifica o valor da coluna "Enviado?"

        layout.addRow("Data da Venda:", self.input_data_venda)
        layout.addRow("Produto:", self.input_produto)
        layout.addRow("Data de Pagamento:", self.input_data_pagamento)
        layout.addRow("Data de Envio:", self.input_data_envio)
        layout.addRow("Código de Rastreio:", self.input_codigo_rastreio)
        layout.addRow("Enviado?", self.checkbox_enviado)

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save_compra)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def save_compra(self):
        data_venda = self.input_data_venda.date().toString('dd-MM-yyyy')
        produto = self.input_produto.text()
        data_pagamento = self.input_data_pagamento.date().toString('dd-MM-yyyy')
        data_envio = self.input_data_envio.date().toString('dd-MM-yyyy')
        codigo_rastreio = self.input_codigo_rastreio.text()
        enviado = self.checkbox_enviado.isChecked()

        try:
            if self.compra_data:
                editar_compra(self.compra_data[0], self.client_id, data_venda, produto, data_pagamento, data_envio,
                              codigo_rastreio, enviado)
            else:
                registrar_compra(self.client_id, data_venda, produto, data_pagamento, data_envio, codigo_rastreio, enviado)

            self.accept()
        except Exception as e:
            print(f"Erro ao salvar compra: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = ClientWindow(1)
    client_window.show()
    sys.exit(app.exec_())
