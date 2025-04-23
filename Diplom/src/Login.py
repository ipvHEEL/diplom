from PyQt6.QtWidgets import *
from Forms.Login_UI import Ui_LoginWindow
from src.database import DB_Settings
from src.Registration import RegistrationManager
# src/Login.py

class LoginManager(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.setupUi(self)
        self.LoginButton.clicked.connect(self.login_user)
        self.RegistrationButton.clicked.connect(self.OpenRegistrationWindow)

    def OpenRegistrationWindow(self):
        self.hide()
        self.registration_window = RegistrationManager()
        self.registration_window .show()

    def login_user(self):
        """Авторизация пользователя"""
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()

        try:
            with DB_Settings.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT userId 
                            FROM user 
                            WHERE 
                                UserName  = %s 
                                AND 
                                UserPassword = %s""",
                        (self.username, self.password)
                    )
                    user = cursor.fetchone()
                    if user:
                        QMessageBox.information(self, 'Успех', 'Успех!')
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Пользователя с такими данными не существует')
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {str(e)}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = LoginManager()
    window.show()
    sys.exit(app.exec())
