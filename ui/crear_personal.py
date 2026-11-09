from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QMessageBox, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

from dao.personal_dao import PersonalDAO


class CrearPersonal(QWidget):
    def __init__(self, volver_al_menu):
        super().__init__()
        self.dao = PersonalDAO()
        self.volver_al_menu = volver_al_menu
        self.id_rol_medico = None
        self.init_ui()
        self.cargar_roles()

    def init_ui(self):
        # Layout principal de la pestaña
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # Encabezado
        self.lbl_titulo = QLabel("Registro de Personal")
        self.lbl_titulo.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.lbl_titulo.setStyleSheet("color: #1E2A38;")
        layout_principal.addWidget(self.lbl_titulo)

        # --- Tarjeta del Formulario ---
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjetaForm")
        tarjeta.setStyleSheet("""
            QFrame#tarjetaForm {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E6ED;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2C3E50;
                border: none;
            }
            QLineEdit, QComboBox {
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background: #F8FAFC;
                color: #1E2A38;
                min-height: 25px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0F62FE;
                background: #FFFFFF;
            }
            /* Estilo específico para indicar visualmente que está bloqueado */
            QLineEdit:disabled {
                background-color: #E2E8F0;
                color: #94A3B8;
                border: 2px solid #CBD5E1;
            }
            /* Corrección de colores en las listas desplegables */
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1E2A38;
                selection-background-color: #0F62FE;
                selection-color: #FFFFFF;
                border: 1px solid #E0E6ED;
                border-radius: 4px;
                outline: none;
            }
        """)

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(30, 30, 30, 30)
        layout_tarjeta.setSpacing(20)

        # Formulario
        form = QFormLayout()
        form.setSpacing(15)

        self.input_nombres = QLineEdit()
        self.input_nombres.setPlaceholderText("Ej: Ana María")
        
        self.input_apellidos = QLineEdit()
        self.input_apellidos.setPlaceholderText("Ej: Rojas Silva")
        
        self.combo_rol = QComboBox()
        self.combo_rol.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.input_colegiado = QLineEdit()
        self.input_colegiado.setEnabled(False) # Bloqueado por defecto
        self.input_colegiado.setPlaceholderText("Solo obligatorio para médicos")

        form.addRow("Nombres:", self.input_nombres)
        form.addRow("Apellidos:", self.input_apellidos)
        form.addRow("Rol en la clínica:", self.combo_rol)
        form.addRow("Número de colegiado:", self.input_colegiado)
        
        layout_tarjeta.addLayout(form)

        # Conectar el cambio de rol para habilitar/deshabilitar el colegiado
        self.combo_rol.currentIndexChanged.connect(self.cambio_rol)

        # Espaciador antes de los botones
        layout_tarjeta.addSpacing(10)

        # --- Botones ---
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(15)

        self.btn_volver = QPushButton("Cancelar / Volver")
        self.btn_volver.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #F8FAFC;
                color: #2C3E50;
                border: 2px solid #E0E6ED;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0E6ED; }
            QPushButton:pressed { background-color: #CBD5E1; }
        """)

        self.btn_guardar = QPushButton("Guardar Personal")
        self.btn_guardar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #0F62FE;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0050E6; }
            QPushButton:pressed { background-color: #1E2A38; }
        """)

        self.btn_volver.clicked.connect(self.cancelar_creacion)
        self.btn_guardar.clicked.connect(self.guardar_personal)

        botones_layout.addStretch()
        botones_layout.addWidget(self.btn_volver)
        botones_layout.addWidget(self.btn_guardar)

        layout_tarjeta.addLayout(botones_layout)
        
        # Añadir tarjeta al layout principal
        layout_principal.addWidget(tarjeta)
        layout_principal.addStretch()

    # =========================================================
    # LÓGICA DEL NEGOCIO (Intacta)
    # =========================================================
    def cargar_roles(self):
        roles = self.dao.listar_roles()
        for id_rol, nombre in roles:
            self.combo_rol.addItem(nombre, id_rol)
            # Detecta y guarda el id del rol "Medico" (ignorando tildes y mayúsculas)
            if nombre.lower().replace("á", "a").replace("é", "e") == "medico":
                self.id_rol_medico = id_rol

    def cambio_rol(self):
        """Habilita el campo de colegiado solo si el rol es Médico."""
        if self.combo_rol.currentData() == self.id_rol_medico:
            self.input_colegiado.setEnabled(True)
        else:
            self.input_colegiado.setEnabled(False)
            self.input_colegiado.clear()

    def cancelar_creacion(self):
        self.limpiar_formulario()
        self.volver_al_menu()

    def guardar_personal(self):
        # Validación básica
        if not self.input_nombres.text().strip() or not self.input_apellidos.text().strip():
            QMessageBox.warning(self, "Validación", "Nombres y apellidos son obligatorios.")
            return

        id_rol = self.combo_rol.currentData()

        # Validación del número de colegiado (solo para médicos)
        numero_colegiado = None
        if self.combo_rol.currentData() == self.id_rol_medico:
            texto = self.input_colegiado.text().strip()
            if texto == "":
                QMessageBox.warning(
                    self, "Validación",
                    "El número de colegiado es obligatorio para médicos."
                )
                return
            if not texto.isdigit():
                QMessageBox.warning(
                    self, "Validación",
                    "El número de colegiado debe contener solo números."
                )
                return
            numero_colegiado = int(texto)

        # Insertar (el trigger en BD crea automáticamente el usuario)
        id_personal, nombre_usuario, error = self.dao.insertar(
            self.input_nombres.text().strip(),
            self.input_apellidos.text().strip(),
            id_rol,
            numero_colegiado
        )
        if id_personal is None:
            QMessageBox.critical(self, "Error", error)
            return

        QMessageBox.information(
            self, "Personal Guardado",
            f"Personal registrado correctamente.\n\n"
            f"Usuario para iniciar sesión: {nombre_usuario}\n"
            f"Contraseña: pendiente de configurar en el primer ingreso."
        )
        self.limpiar_formulario()
        self.volver_al_menu()

    def limpiar_formulario(self):
        self.input_nombres.clear()
        self.input_apellidos.clear()
        self.combo_rol.setCurrentIndex(0)
        self.input_colegiado.clear()
        self.input_colegiado.setEnabled(False)