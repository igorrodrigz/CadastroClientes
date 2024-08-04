import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QPushButton, QDialog, QFormLayout, QLineEdit, QCheckBox, QComboBox, QDateEdit
from PyQt5.QtCore import Qt, QDate
from lojaDB import buscar_compras, registrar_compra, editar_compra, excluir_compra
from utils import criar_seletor_data

class ClientWindow(QWidget):
    def __init__(self, client_id):
        super().__init__()
        self.client_id = client_id
        self.setWindowTitle('Detalhes do Cliente')
        self.setGeometry(100, 100, 900, 600)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Lista de compras
        self.table_compras = QTableWidget()
        self.table_compras.setColumnCount(10)  # Atualizar o número de colunas
        self.table_compras.setHorizontalHeaderLabels(
            ["Número Item", "ID", "Data da Venda", "Produto", "Valor da Venda", "Modo de Pagamento", "Data de Pagamento",
             "Data de Envio", "Código de Rastreio", "Enviado?"])
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

        # Aplicar estilo diretamente
        self.setStyleSheet("""
                            QWidget {
                                background-color: #f0f0f0;
                            }

                            QHeaderView::section {
                                background-color: #f0f0f0; 
                                color: black; 
                            }
                            QPushButton {
                                background-color: #3c4c7d;
                                color: white;
                                border-radius: 5px;
                                padding: 10px;
                                font-size: 16px;
                            }
                            QPushButton:hover {
                                background-color: #24346c;
                            }
                            QPushButton:pressed {
                                background-color: #465184;
                            }
                        """)

    def load_compras(self):
        try:
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
        except Exception as e:
            print(f"Erro ao carregar compras: {e}")

    def adicionar_compra(self):
        dialog = CompraDialog(self, self.client_id)
        if dialog.exec_():
            self.load_compras()

    def editar_compra(self):
        selected_row = self.table_compras.currentRow()
        if selected_row != -1:
            compra_id_item = self.table_compras.item(selected_row, 0)  # Ajustado para a coluna de ID
            if compra_id_item:
                compra_id = compra_id_item.text()
                print(f"ID da compra selecionada: {compra_id}")
                try:
                    compra_data = buscar_compras(self.client_id, compra_id)
                    print(f"Dados da compra: {compra_data}")
                    if compra_data:
                        compra_data = compra_data[0]
                        # Criação do diálogo para edição da compra
                        dialog = CompraDialog(self, self.client_id, compra_data)
                        if dialog.exec_():
                            # Captura os dados atualizados do diálogo
                            dados_atualizados = dialog.get_dados_compra()
                            # Atualização da compra no banco de dados
                            editar_compra(
                                compra_id,
                                dados_atualizados['data_venda'],
                                dados_atualizados['produto'],
                                dados_atualizados['valor_venda'],
                                dados_atualizados['modo_pagamento'],
                                dados_atualizados['data_pagamento'],
                                dados_atualizados.get('data_envio', None),
                                dados_atualizados.get('codigo_rastreio', None),
                                1 if dados_atualizados.get('enviado', False) else 0
                            )
                            # Recarregar as compras para refletir as mudanças
                            self.load_compras()
                    else:
                        print(f"Nenhuma compra encontrada com o ID: {compra_id}")
                except Exception as e:
                    print(f"Erro ao buscar dados da compra: {e}")
            else:
                print("O item da célula não contém um ID válido.")

    def excluir_compra(self):
        selected_row = self.table_compras.currentRow()
        if selected_row != -1:
            compra_id = self.table_compras.item(selected_row, 0).text()  # Ajustar para pegar o ID correto
            try:
                excluir_compra(compra_id)
                print(f"Compra com ID {compra_id} excluída com sucesso.")
                self.load_compras()
            except Exception as e:
                print(f"Erro ao excluir compra: {e}")


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
        self.input_valor_venda = QLineEdit()
        self.input_modo_pagamento = QComboBox()
        self.input_modo_pagamento.addItems(["Pix", "Débito", "Crédito", "Dinheiro"])
        self.input_data_pagamento = criar_seletor_data()
        self.input_data_envio = criar_seletor_data()
        self.input_codigo_rastreio = QLineEdit()
        self.checkbox_enviado = QCheckBox()

        if self.compra_data:
            try:
                self.input_data_venda.setDate(QDate.fromString(str(self.compra_data[2]), 'dd-MM-yyyy'))
                self.input_produto.setText(self.compra_data[3])
                self.input_valor_venda.setText(str(self.compra_data[4]))
                self.input_modo_pagamento.setCurrentText(self.compra_data[5])
                self.input_data_pagamento.setDate(QDate.fromString(str(self.compra_data[6]), 'dd-MM-yyyy'))
                self.input_data_envio.setDate(QDate.fromString(str(self.compra_data[7]), 'dd-MM-yyyy'))
                self.input_codigo_rastreio.setText(self.compra_data[8])
                self.checkbox_enviado.setChecked(bool(self.compra_data[9]))  # Verifica o valor da coluna "Enviado?"
            except Exception as e:
                print(f"Erro ao carregar dados da compra: {e}")

        layout.addRow("Data da Venda:", self.input_data_venda)
        layout.addRow("Produto:", self.input_produto)
        layout.addRow("Valor da Venda:", self.input_valor_venda)
        layout.addRow("Modo de Pagamento:", self.input_modo_pagamento)
        layout.addRow("Data de Pagamento:", self.input_data_pagamento)
        layout.addRow("Data de Envio:", self.input_data_envio)
        layout.addRow("Código de Rastreio:", self.input_codigo_rastreio)
        layout.addRow("Enviado?", self.checkbox_enviado)

        self.button_save = QPushButton("Salvar")
        self.button_save.clicked.connect(self.save_compra)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def get_dados_compra(self):
        return {
            'data_venda': self.input_data_venda.date().toString('dd-MM-yyyy'),
            'produto': self.input_produto.text(),
            'valor_venda': float(self.input_valor_venda.text().replace(',', '.')) if self.input_valor_venda.text() else 0.0,
            'modo_pagamento': self.input_modo_pagamento.currentText(),
            'data_pagamento': self.input_data_pagamento.date().toString('dd-MM-yyyy'),
            'data_envio': self.input_data_envio.date().toString('dd-MM-yyyy') if self.input_data_envio.date() != QDate.currentDate() else None,
            'codigo_rastreio': self.input_codigo_rastreio.text(),
            'enviado': self.checkbox_enviado.isChecked()
        }

    def save_compra(self):
        try:
            dados_compra = self.get_dados_compra()
            print(f"Salvando compra: {dados_compra}")
            if self.compra_data:
                editar_compra(
                    self.compra_data[1],  # ID da compra
                    dados_compra['data_venda'],
                    dados_compra['produto'],
                    dados_compra['valor_venda'],
                    dados_compra['modo_pagamento'],
                    dados_compra['data_pagamento'],
                    dados_compra.get('data_envio', None),
                    dados_compra.get('codigo_rastreio', None),
                    1 if dados_compra.get('enviado', False) else 0
                )
            else:
                registrar_compra(self.client_id, **dados_compra)

            self.accept()
        except ValueError as ve:
            print(f"Erro: valor da venda inválido '{dados_compra['valor_venda']}'. Detalhes: {ve}")
            # Adicionar uma mensagem de erro na interface se desejado
        except Exception as e:
            print(f"Erro ao salvar compra: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    client_window = ClientWindow(1)
    client_window.show()
    sys.exit(app.exec_())
