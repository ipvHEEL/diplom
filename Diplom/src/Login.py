from PyQt6.QtWidgets import *
from Forms.Login_UI import Ui_LoginWindow
from src.database import DB_Settings
from src.Registration import RegistrationManager
from src.lobby import MainWindow

class LoginManager(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.username = None
        self.password = None
        self.setupUi(self)
        self.LoginButton.clicked.connect(self.login_user)
        self.RegistrationButton.clicked.connect(self.OpenRegistrationWindow)
        self.current_user = None

    def OpenRegistrationWindow(self):
        self.hide()
        self.registration_window = RegistrationManager()
        self.registration_window.show()

    def login_user(self):
        """Авторизация пользователя"""
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()

        try:
            with DB_Settings.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT userId, UserName, UserName as UserFullName, Position.PositionName
                           FROM user 
                           INNER JOIN Position ON user.UserPositionId = Position.PositionId 
                           WHERE UserName = %s AND UserPassword = %s""",
                        (self.username, self.password)
                    )
                    user = cursor.fetchone()
                    if user:
                        self.current_user = {
                            'id': user[0],
                            'username': user[1],
                            'full_name': user[2],
                            'role': user[3].lower()  # Приводим роль к нижнему регистру
                        }
                        self.open_lobby_window()
                    else:
                        QMessageBox.warning(self, 'Ошибка', 'Неверные логин или пароль')
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {str(e)}")

    def open_lobby_window(self):
        """Открывает главное окно приложения после авторизации"""
        self.hide()
        self.lobby_window = MainWindow(user_data=self.current_user)  # Теперь передаем user_data
        self.lobby_window.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoginManager()
    window.show()
    sys.exit(app.exec())