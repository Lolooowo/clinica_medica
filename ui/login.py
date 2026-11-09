from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class Login(QWidget):
    def __init__(self, iniciar_sesion_callback):
        super().__init__()
        self.iniciar_sesion_callback = iniciar_sesion_callback
        self.init_ui()

    def init_ui(self):
        # Todo el fondo de la pestaña será blanco puro
        self.setObjectName("pantallaLogin")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            #pantallaLogin {
                background-color: #FFFFFF;
            }
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 50, 40, 50)
        layout_principal.setSpacing(15)

        # Título
        titulo = QLabel("Clínica Médica")
        titulo.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #1E2A38; background: transparent;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titulo)

        subtitulo = QLabel("Sistema de Gestión")
        subtitulo.setStyleSheet(
            "color: #A0B2C6; font-size: 14px; background: transparent; margin-bottom: 20px;"
        )
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(subtitulo)

        # Campo: Usuario
        label_usuario = QLabel("Usuario")
        label_usuario.setStyleSheet(
            "color: #2C3E50; font-size: 13px; font-weight: bold; background: transparent;"
        )
        layout_principal.addWidget(label_usuario)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Ingrese su usuario")
        self.input_usuario.setMinimumHeight(45)
        self.input_usuario.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background: #F8FAFC;
                color: #1E2A38;
            }
            QLineEdit:focus {
                border: 2px solid #0F62FE;
                background: #FFFFFF;
            }
        """)
        layout_principal.addWidget(self.input_usuario)

        layout_principal.addSpacing(5)

        # Campo: Contraseña
        label_contrasena = QLabel("Contraseña")
        label_contrasena.setStyleSheet(
            "color: #2C3E50; font-size: 13px; font-weight: bold; background: transparent;"
        )
        layout_principal.addWidget(label_contrasena)

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("Ingrese su contraseña")
        self.input_contrasena.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_contrasena.setMinimumHeight(45)
        self.input_contrasena.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background: #F8FAFC;
                color: #1E2A38;
            }
            QLineEdit:focus {
                border: 2px solid #0F62FE;
                background: #FFFFFF;
            }
        """)
        layout_principal.addWidget(self.input_contrasena)

        layout_principal.addSpacing(20)

        # Botón: Ingresar
        self.btn_ingresar = QPushButton("Ingresar al Sistema")
        self.btn_ingresar.setMinimumHeight(50)
        self.btn_ingresar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_ingresar.setStyleSheet("""
            QPushButton {
                background-color: #0F62FE;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0050E6;
            }
            QPushButton:pressed {
                background-color: #1E2A38;
            }
        """)
        self.btn_ingresar.clicked.connect(self.intentar_ingresar)
        layout_principal.addWidget(self.btn_ingresar)

        # Mensaje de error
        self.label_error = QLabel("")
        self.label_error.setStyleSheet(
            "color: #E74C3C; font-size: 13px; font-weight: bold; background: transparent; margin-top: 5px;"
        )
        self.label_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_error.hide()
        layout_principal.addWidget(self.label_error)
        
        # Empujar todo hacia arriba para que no quede aplastado en el centro
        layout_principal.addStretch()

    def intentar_ingresar(self):
        usuario = self.input_usuario.text().strip()
        contrasena = self.input_contrasena.text()

        if usuario == "" or contrasena == "":
            self.mostrar_error("Complete usuario y contraseña.")
            return

        self.iniciar_sesion_callback(usuario, contrasena)

    def mostrar_error(self, mensaje):
        self.label_error.setText(mensaje)
        self.label_error.show()

    def limpiar(self):
        self.input_usuario.clear()
        self.input_contrasena.clear()
        self.label_error.hide()