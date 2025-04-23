from PyQt6.QtWidgets import *
from src.database import DB_Settings
from Forms.Registration_UI import Ui_RegistrationWindow

class RegistrationManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegistrationWindow()
        self.ui.setupUi(self)
        self.addPositions()

    def addPositions(self):
        try:
            with DB_Settings.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT PositionName FROM Position"
                    )
                    positions = cursor.fetchall()
                    for pos in positions:
                        self.ui.PositionComboBox.addItem(pos[0])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {str(e)}")