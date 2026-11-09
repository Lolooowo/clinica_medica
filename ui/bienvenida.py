from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt6.QtCore import Qt


class Bienvenida(QWidget):
    def __init__(self, volver_al_login, ir_a_crear_paciente,
                 ir_a_buscar_paciente, ir_a_crear_personal,
                 ir_a_crear_consulta, ir_a_mis_consultas):
        super().__init__()
        self.volver_al_login = volver_al_login
        self.init_ui(ir_a_crear_paciente, ir_a_buscar_paciente,
                     ir_a_crear_personal, ir_a_crear_consulta,
                     ir_a_mis_consultas)

    def init_ui(self, ir_a_crear_paciente, ir_a_buscar_paciente,
                ir_a_crear_personal, ir_a_crear_consulta,
                ir_a_mis_consultas):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titulo = QLabel("Sistema de Gestion - Clinica")
        self.titulo.setStyleSheet(
            "font-size: 28px; font-weight: bold; margin-bottom: 10px;"
        )
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.titulo)

        self.label_rol = QLabel("")
        self.label_rol.setStyleSheet(
            "font-size: 14px; color: #555; margin-bottom: 20px;"
        )
        self.label_rol.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_rol)

        self.botones_layout = QVBoxLayout()
        self.botones_layout.setSpacing(15)

        # Botones (se muestran/ocultan segun el rol)
        self.btn_crear_paciente = self._crear_boton(
            "Crear Paciente", ir_a_crear_paciente)
        self.btn_buscar_paciente = self._crear_boton(
            "Buscar Paciente", ir_a_buscar_paciente)
        self.btn_crear_consulta = self._crear_boton(
            "Crear Consulta", ir_a_crear_consulta)
        self.btn_mis_consultas = self._crear_boton(
            "Mis Consultas", ir_a_mis_consultas)
        self.btn_crear_personal = self._crear_boton(
            "Crear Personal", ir_a_crear_personal)

        for btn in [self.btn_crear_paciente, self.btn_buscar_paciente,
                    self.btn_crear_consulta, self.btn_mis_consultas,
                    self.btn_crear_personal]:
            self.botones_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.botones_layout)

        # Boton de cerrar sesion (siempre visible)
        self.btn_cerrar_sesion = QPushButton("Cerrar sesion")
        self.btn_cerrar_sesion.setMinimumHeight(40)
        self.btn_cerrar_sesion.setMinimumWidth(200)
        self.btn_cerrar_sesion.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_cerrar_sesion.clicked.connect(self.volver_al_login)
        layout.addSpacing(30)
        layout.addWidget(self.btn_cerrar_sesion, alignment=Qt.AlignmentFlag.AlignCenter)

    def _crear_boton(self, texto, funcion):
        btn = QPushButton(texto)
        btn.setMinimumHeight(50)
        btn.setMinimumWidth(300)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                background-color: #2d89ef;
                color: white;
            }
            QPushButton:hover {
                background-color: #1b6ec2;
            }
        """)
        btn.clicked.connect(funcion)
        return btn

    def configurar_rol(self, rol):
        """Muestra u oculta botones segun el rol del usuario logueado."""
        rol_normalizado = (rol or "").lower().replace("á", "a").replace("é", "e")

        # Por defecto, ocultar todo
        for btn in [self.btn_crear_paciente, self.btn_buscar_paciente,
                    self.btn_crear_consulta, self.btn_mis_consultas,
                    self.btn_crear_personal]:
            btn.hide()

        if rol_normalizado in ("recepcionista", "enfermera"):
            self.btn_crear_paciente.show()
            self.btn_buscar_paciente.show()
            self.btn_crear_consulta.show()
            self.label_rol.setText(f"Rol: {rol}")
        elif rol_normalizado == "medico":
            self.btn_mis_consultas.show()
            self.btn_crear_personal.show()
            self.label_rol.setText(f"Rol: {rol}")
        else:
            self.label_rol.setText(
                f"Rol: {rol or 'Sin rol asignado'} - Sin permisos configurados"
            )