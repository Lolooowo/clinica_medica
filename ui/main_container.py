from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QLabel, QStackedWidget, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class MainContainer(QWidget):
    def __init__(self, logout_cb, v_crear_paciente, v_buscar_paciente, 
                 v_crear_personal, v_crear_consulta, v_mis_consultas,
                 abrir_mis_consultas_cb):
        super().__init__()
        self.logout_cb = logout_cb
        
        # Referencias a tus vistas ya creadas
        self.v_crear_paciente = v_crear_paciente
        self.v_buscar_paciente = v_buscar_paciente
        self.v_crear_personal = v_crear_personal
        self.v_crear_consulta = v_crear_consulta
        self.v_mis_consultas = v_mis_consultas
        self.abrir_mis_consultas_cb = abrir_mis_consultas_cb

        self.init_ui()
        self.apply_stylesheet()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # ==================== MENU LATERAL ====================
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(240)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(15, 30, 15, 30)
        self.sidebar_layout.setSpacing(10)

        # Titulo y Rol
        self.lbl_title = QLabel("Clínica La esperanza")
        self.lbl_title.setObjectName("sidebarTitle")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_rol = QLabel("Rol: ...")
        self.lbl_rol.setObjectName("sidebarRol")
        self.lbl_rol.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebar_layout.addWidget(self.lbl_title)
        self.sidebar_layout.addWidget(self.lbl_rol)
        self.sidebar_layout.addSpacing(30)

        # Botones de navegacion
        self.btn_dashboard = self.crear_boton("Inicio")
        self.btn_crear_paciente = self.crear_boton("Crear Paciente")
        self.btn_buscar_paciente = self.crear_boton("Buscar Paciente")
        self.btn_crear_consulta = self.crear_boton("Crear Consulta")
        self.btn_mis_consultas = self.crear_boton("Mis Consultas")
        self.btn_crear_personal = self.crear_boton("Crear Personal")

        self.sidebar_layout.addWidget(self.btn_dashboard)
        self.sidebar_layout.addWidget(self.btn_crear_paciente)
        self.sidebar_layout.addWidget(self.btn_buscar_paciente)
        self.sidebar_layout.addWidget(self.btn_crear_consulta)
        self.sidebar_layout.addWidget(self.btn_mis_consultas)
        self.sidebar_layout.addWidget(self.btn_crear_personal)
        self.sidebar_layout.addStretch()

        # Boton de cerrar sesion
        self.btn_logout = QPushButton("Cerrar Sesión")
        self.btn_logout.setObjectName("btnLogout")
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.clicked.connect(self.logout_cb)
        self.sidebar_layout.addWidget(self.btn_logout)

        # ==================== ÁREA CENTRAL ====================
        self.content_area = QFrame()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(20, 20, 20, 20)

        self.stacked = QStackedWidget()
        
        # Pagina 0: Dashboard/Inicio (Reemplaza la antigua bienvenida visual)
        self.page_dashboard = QWidget()
        dash_layout = QVBoxLayout(self.page_dashboard)
        dash_lbl = QLabel("Bienvenido al Sistema de Gestión de la Clínica")
        dash_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dash_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50;")
        dash_layout.addWidget(dash_lbl)

        # Agregar todo al StackedWidget interno
        self.stacked.addWidget(self.page_dashboard)      # Index 0
        self.stacked.addWidget(self.v_crear_paciente)    # Index 1
        self.stacked.addWidget(self.v_buscar_paciente)   # Index 2
        self.stacked.addWidget(self.v_crear_consulta)    # Index 3
        self.stacked.addWidget(self.v_mis_consultas)     # Index 4
        self.stacked.addWidget(self.v_crear_personal)    # Index 5

        self.content_layout.addWidget(self.stacked)

        # Ensamblar layout principal
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

        # Conectar botones
        self.btn_dashboard.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.btn_crear_paciente.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        self.btn_buscar_paciente.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        self.btn_crear_consulta.clicked.connect(lambda: self.stacked.setCurrentIndex(3))
        # Este boton usa el callback para recargar la tabla antes de entrar
        self.btn_mis_consultas.clicked.connect(self.abrir_mis_consultas_cb)
        self.btn_crear_personal.clicked.connect(lambda: self.stacked.setCurrentIndex(5))

    def crear_boton(self, texto):
        btn = QPushButton(texto)
        btn.setProperty("class", "navButton")
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        return btn

    def configurar_rol(self, rol):
        """Muestra u oculta botones del menu segun el rol, igual que tu bienvenida.py"""
        rol_normalizado = (rol or "").lower().replace("á", "a").replace("é", "e")
        
        self.lbl_rol.setText(f"Rol: {rol}")

        # Ocultar todos primero
        self.btn_crear_paciente.hide()
        self.btn_buscar_paciente.hide()
        self.btn_crear_consulta.hide()
        self.btn_mis_consultas.hide()
        self.btn_crear_personal.hide()

        # Mostrar segun rol
        if rol_normalizado in ("recepcionista", "enfermera"):
            self.btn_crear_paciente.show()
            self.btn_buscar_paciente.show()
            self.btn_crear_consulta.show()
        elif rol_normalizado == "medico":
            self.btn_mis_consultas.show()
            self.btn_crear_personal.show()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            #sidebar {
                background-color: #1E2A38;
                border-right: 1px solid #141C26;
            }
            #sidebarTitle { color: #FFFFFF; font-size: 18px; font-weight: bold; }
            #sidebarRol { color: #A0B2C6; font-size: 12px; margin-bottom: 10px; }
            
            QPushButton.navButton {
                background-color: transparent;
                color: #A0B2C6;
                border: none;
                text-align: left;
                padding: 12px 15px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton.navButton:hover { background-color: #2C3E50; color: #FFFFFF; }
            QPushButton.navButton:pressed { background-color: #0F62FE; color: #FFFFFF; }
            
            #btnLogout {
                background-color: #E74C3C; color: white; border: none; 
                padding: 12px; border-radius: 8px; font-weight: bold;
            }
            #btnLogout:hover { background-color: #C0392B; }
            
            #contentArea { background-color: #F4F7F6; }
        """)