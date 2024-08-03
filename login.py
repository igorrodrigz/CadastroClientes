import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from main import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Acesso')
        self.setGeometry(100, 100, 280, 150)

        layout = QVBoxLayout()

        self.label_user = QLabel('Usuário')
        self.input_user = QLineEdit()
        self.label_password = QLabel('Senha')
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton('Login')
        self.button_login.clicked.connect(self.check_login)

        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def check_login(self):
        user = self.input_user.text()
        password = self.input_password.text()

        if user == 'usuario' and password == 'senha':
            QMessageBox.information(self, 'Login', 'Login bem-sucedido!')
            self.close()
            self.open_main_window()
        else:
            QMessageBox.warning(self, 'Login', 'Usuário ou senha incorretos.')

    def open_main_window(self):
        try:
            self.main_window = MainWindow()
            self.main_window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Ocorreu um erro ao abrir a janela principal: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
