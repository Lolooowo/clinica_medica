import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt6.QtGui import QGuiApplication

from db.conexion import Conexion
from ui.login import Login
from ui.main_container import MainContainer
from ui.crear_paciente import CrearPaciente
from ui.buscar_paciente import BuscarPaciente
from ui.crear_personal import CrearPersonal
from ui.crear_consulta import CrearConsulta
from ui.mis_consultas import MisConsultas
from dao.usuario_dao import UsuarioDAO
from ui.primer_ingreso import PrimerIngreso

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión - Clínica Médica")
        
        # Iniciar con el tamaño de la ventana de Login
        self.ajustar_tamano_login()

        self.conexion = Conexion()
        if not self.conexion.probar_conexion():
            QMessageBox.critical(self, "Error de conexión", "No se pudo conectar a la base de datos.")
        
        self.usuario_dao = UsuarioDAO()
        self.id_personal_sesion = None  
        self.rol_sesion = None

        self.stacked_principal = QStackedWidget()
        self.setCentralWidget(self.stacked_principal)

        # 1. Login
        self.login = Login(iniciar_sesion_callback=self.intentar_ingresar)
        self.stacked_principal.addWidget(self.login)

        # 2. Vistas Internas
        self.crear_paciente = CrearPaciente(volver_al_menu=self.ir_a_dashboard)
        self.buscar_paciente = BuscarPaciente(volver_al_menu=self.ir_a_dashboard)
        self.buscar_paciente.editar_solicitado = self.abrir_edicion_paciente
        self.crear_personal = CrearPersonal(volver_al_menu=self.ir_a_dashboard)
        self.crear_consulta = CrearConsulta(volver_al_menu=self.ir_a_dashboard, ventana=self)
        self.mis_consultas = MisConsultas(volver_al_menu=self.ir_a_dashboard, ventana=self)

        # 3. Contenedor Principal
        self.main_container = MainContainer(
            logout_cb=self.cerrar_sesion,
            v_crear_paciente=self.crear_paciente,
            v_buscar_paciente=self.buscar_paciente,
            v_crear_personal=self.crear_personal,
            v_crear_consulta=self.crear_consulta,
            v_mis_consultas=self.mis_consultas,
            abrir_mis_consultas_cb=self.abrir_mis_consultas
        )
        self.stacked_principal.addWidget(self.main_container)

    # --- MÉTODOS DE REDIMENSIONAMIENTO ---
    def ajustar_tamano_login(self):
        self.resize(400, 520) # Tamaño pequeño para el login
        self.centrar_en_pantalla()

    def ajustar_tamano_principal(self):
        self.resize(1100, 700) # Tamaño grande para el sistema
        self.centrar_en_pantalla()

    def centrar_en_pantalla(self):
        # Calcula el centro de la pantalla y mueve la ventana ahí
        geometria_ventana = self.frameGeometry()
        centro_pantalla = self.screen().availableGeometry().center()
        geometria_ventana.moveCenter(centro_pantalla)
        self.move(geometria_ventana.topLeft())

    # --- LÓGICA DE SESIÓN ---
    def intentar_ingresar(self, usuario, contrasena):
        id_personal, rol, error = self.usuario_dao.validar_login(usuario, contrasena)

        if error == "PRIMER_INGRESO":
            dialogo = PrimerIngreso(usuario, self)
            dialogo.exec()
            return
        if error is not None:
            self.login.mostrar_error(error)
            return

        self.id_personal_sesion = id_personal
        self.rol_sesion = rol
        self.main_container.configurar_rol(rol)
        self.login.limpiar()
        
        # Expandir ventana y entrar al sistema
        self.ajustar_tamano_principal()
        self.stacked_principal.setCurrentIndex(1)
        self.main_container.stacked.setCurrentIndex(0) 

    def cerrar_sesion(self):
        self.id_personal_sesion = None
        self.rol_sesion = None
        self.login.limpiar()
        
        # Encoger ventana y volver al login
        self.ajustar_tamano_login()
        self.stacked_principal.setCurrentIndex(0) 

    # --- NAVEGACIÓN ---
    def ir_a_dashboard(self):
        self.main_container.stacked.setCurrentIndex(0)

    def abrir_edicion_paciente(self, id_paciente):
        self.crear_paciente.cargar_paciente(id_paciente)
        self.main_container.stacked.setCurrentIndex(1) 

    def abrir_mis_consultas(self):
        self.mis_consultas.cargar_consultas()
        self.main_container.stacked.setCurrentIndex(4) 

def main():
    app = QApplication(sys.argv)
    font = app.font()
    font.setFamily("Segoe UI")
    app.setFont(font)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()