from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate

def criar_seletor_data():
    date_edit = QDateEdit()
    date_edit.setCalendarPopup(True)
    date_edit.setDate(QDate.currentDate())
    return date_edit