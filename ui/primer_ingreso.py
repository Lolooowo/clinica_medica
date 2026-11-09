from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from dao.usuario_dao import UsuarioDAO


class PrimerIngreso(QDialog):
    def __init__(self, nombre_usuario, parent=None):
        super().__init__(parent)
        self.nombre_usuario = nombre_usuario
        self.dao = UsuarioDAO()
        self.setWindowTitle("Primer ingreso - Configurar contrasena")
        self.setFixedWidth(380)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        mensaje = QLabel(
            f"Bienvenido/a, <b>{self.nombre_usuario}</b>.<br><br>"
            "Es tu primer ingreso al sistema. Por seguridad, "
            "configura tu contrasena para continuar."
        )
        mensaje.setWordWrap(True)
        layout.addWidget(mensaje)

        self.input_nueva = QLineEdit()
        self.input_nueva.setPlaceholderText("Nueva contrasena")
        self.input_nueva.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_nueva)

        self.input_confirmar = QLineEdit()
        self.input_confirmar.setPlaceholderText("Confirmar contrasena")
        self.input_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_confirmar)

        btn_guardar = QPushButton("Guardar contrasena")
        btn_guardar.clicked.connect(self.guardar)
        layout.addWidget(btn_guardar)

    def guardar(self):
        nueva = self.input_nueva.text()
        confirmar = self.input_confirmar.text()

        if len(nueva) < 6:
            QMessageBox.warning(self, "Validacion",
                "La contrasena debe tener al menos 6 caracteres.")
            return
        if nueva != confirmar:
            QMessageBox.warning(self, "Validacion",
                "Las contrasenas no coinciden.")
            return

        exito, error = self.dao.configurar_password(self.nombre_usuario, nueva)
        if exito:
            QMessageBox.information(self, "Exito",
                "Contrasena configurada correctamente. Ya puedes iniciar sesion.")
            self.accept()  # cierra el dialogo
        else:
            QMessageBox.critical(self, "Error", error)