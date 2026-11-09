from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox,
    QStackedWidget, QFrame, QFormLayout, QTextEdit, QHeaderView, QAbstractItemView,
    QLineEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

from dao.consulta_dao import ConsultaDAO


class MisConsultas(QWidget):
    def __init__(self, volver_al_menu, ventana):
        super().__init__()
        self.dao = ConsultaDAO()
        self.volver_al_menu = volver_al_menu
        self.ventana = ventana
        self.id_consulta_seleccionada = None
        self.filas_receta = [] # Lista para almacenar las filas dinámicas de medicamentos
        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        self.stacked = QStackedWidget()
        layout_principal.addWidget(self.stacked)

        # =========================================================
        # PÁGINA 0: LISTA DE CONSULTAS PENDIENTES
        # =========================================================
        self.page_lista = QWidget()
        layout_lista = QVBoxLayout(self.page_lista)
        layout_lista.setContentsMargins(40, 40, 40, 40)
        layout_lista.setSpacing(20)

        titulo_lista = QLabel("Mis Consultas Pendientes")
        titulo_lista.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        titulo_lista.setStyleSheet("color: #1E2A38;")
        layout_lista.addWidget(titulo_lista)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels([
            "ID", "Paciente", "Fecha / Hora", "Motivo", "Tipo Sangre", "Alergias"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabla.setColumnWidth(3, 250)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.verticalHeader().setVisible(False)
        
        self.tabla.cellClicked.connect(self.seleccionar_fila)
        self.tabla.cellDoubleClicked.connect(self.abrir_atencion)
        layout_lista.addWidget(self.tabla)

        btn_layout = QHBoxLayout()
        self.btn_actualizar = QPushButton("Actualizar Lista")
        self.btn_actualizar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_actualizar.setObjectName("btnSecundario")
        self.btn_actualizar.clicked.connect(self.cargar_consultas)

        self.btn_atender = QPushButton("Atender Consulta")
        self.btn_atender.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_atender.setEnabled(False)
        self.btn_atender.clicked.connect(self.abrir_atencion)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_actualizar)
        btn_layout.addWidget(self.btn_atender)
        layout_lista.addLayout(btn_layout)

        self.stacked.addWidget(self.page_lista)

        # =========================================================
        # PÁGINA 1: FORMULARIO PARA ATENDER CONSULTA
        # =========================================================
        self.page_atencion = QWidget()
        layout_atencion = QVBoxLayout(self.page_atencion)
        layout_atencion.setContentsMargins(40, 20, 40, 20)
        layout_atencion.setSpacing(15)

        self.lbl_titulo_atencion = QLabel("Atendiendo Consulta")
        self.lbl_titulo_atencion.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.lbl_titulo_atencion.setStyleSheet("color: #1E2A38;")
        layout_atencion.addWidget(self.lbl_titulo_atencion)

        # Área con Scroll para que no se deforme la ventana si agregan muchos medicamentos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        scroll_layout.setSpacing(15)

        # --- Tarjeta 1: Información del Paciente ---
        tarjeta_info = QFrame()
        tarjeta_info.setObjectName("tarjetaInfo")
        layout_info = QFormLayout(tarjeta_info)
        layout_info.setContentsMargins(20, 20, 20, 20)

        self.lbl_paciente = QLabel()
        self.lbl_fecha = QLabel()
        self.lbl_sangre = QLabel()
        self.lbl_alergias = QLabel()
        self.lbl_motivo = QLabel()
        self.lbl_motivo.setWordWrap(True)

        estilo_dato = "color: #0F62FE; font-size: 14px; font-weight: bold;"
        for lbl in [self.lbl_paciente, self.lbl_fecha, self.lbl_sangre, self.lbl_alergias]:
            lbl.setStyleSheet(estilo_dato)
        self.lbl_motivo.setStyleSheet("color: #E74C3C; font-size: 14px; font-weight: bold;") 

        layout_info.addRow(QLabel("Paciente:"), self.lbl_paciente)
        layout_info.addRow(QLabel("Fecha de Cita:"), self.lbl_fecha)
        layout_info.addRow(QLabel("Tipo Sangre:"), self.lbl_sangre)
        layout_info.addRow(QLabel("Alergias:"), self.lbl_alergias)
        layout_info.addRow(QLabel("Motivo:"), self.lbl_motivo)
        
        scroll_layout.addWidget(tarjeta_info)

        # --- Tarjeta 2: Formulario de Diagnóstico ---
        tarjeta_medica = QFrame()
        tarjeta_medica.setObjectName("tarjetaForm")
        layout_medica = QVBoxLayout(tarjeta_medica)
        layout_medica.setContentsMargins(25, 25, 25, 25)

        self.texto_diagnostico = QTextEdit()
        self.texto_diagnostico.setPlaceholderText("Redacte el diagnóstico del paciente (Obligatorio)...")
        self.texto_diagnostico.setMaximumHeight(80)

        self.texto_nota = QTextEdit()
        self.texto_nota.setPlaceholderText("Notas, observaciones e indicaciones generales (Obligatorio)...")
        self.texto_nota.setMaximumHeight(80)

        layout_medica.addWidget(QLabel("Diagnóstico Clínico:"))
        layout_medica.addWidget(self.texto_diagnostico)
        layout_medica.addWidget(QLabel("Nota Médica:"))
        layout_medica.addWidget(self.texto_nota)
        
        scroll_layout.addWidget(tarjeta_medica)

        # --- Tarjeta 3: Receta Médica Dinámica ---
        tarjeta_receta = QFrame()
        tarjeta_receta.setObjectName("tarjetaForm")
        layout_tarjeta_receta = QVBoxLayout(tarjeta_receta)
        layout_tarjeta_receta.setContentsMargins(25, 25, 25, 25)
        layout_tarjeta_receta.setSpacing(10)

        header_receta = QHBoxLayout()
        header_receta.addWidget(QLabel("Receta Médica:"))
        
        self.btn_add_med = QPushButton("Agregar Medicamento")
        self.btn_add_med.setObjectName("btnSecundario")
        self.btn_add_med.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_add_med.setFixedWidth(200)
        self.btn_add_med.clicked.connect(self.agregar_fila_receta)
        
        header_receta.addWidget(self.btn_add_med, alignment=Qt.AlignmentFlag.AlignRight)
        layout_tarjeta_receta.addLayout(header_receta)

        # Contenedor donde se insertarán las filas dinámicamente
        self.contenedor_medicamentos = QVBoxLayout()
        self.contenedor_medicamentos.setSpacing(10)
        layout_tarjeta_receta.addLayout(self.contenedor_medicamentos)

        scroll_layout.addWidget(tarjeta_receta)
        scroll_layout.addStretch()

        # Ensamblar Scroll Area
        scroll_area.setWidget(scroll_content)
        layout_atencion.addWidget(scroll_area)

        # --- Botones Finales ---
        botones_atencion = QHBoxLayout()
        self.btn_cancelar = QPushButton("Cancelar / Volver")
        self.btn_cancelar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancelar.setObjectName("btnSecundario")
        
        self.btn_guardar = QPushButton("Finalizar y Guardar Atención")
        self.btn_guardar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.btn_cancelar.clicked.connect(self.volver_a_lista)
        self.btn_guardar.clicked.connect(self.guardar_atencion)

        botones_atencion.addStretch()
        botones_atencion.addWidget(self.btn_cancelar)
        botones_atencion.addWidget(self.btn_guardar)
        
        layout_atencion.addLayout(botones_atencion)

        self.stacked.addWidget(self.page_atencion)

        # =========================================================
        # ESTILOS QSS
        # =========================================================
        self.setStyleSheet("""
            QWidget { background-color: #F4F7F6; }
            
            QTextEdit, QLineEdit {
                border: 2px solid #E0E6ED; border-radius: 8px; padding: 10px;
                font-size: 14px; background: #F8FAFC; color: #1E2A38;
            }
            QTextEdit:focus, QLineEdit:focus { border: 2px solid #0F62FE; background: #FFFFFF; }
            
            QPushButton {
                background-color: #0F62FE; color: white; border: none;
                border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0050E6; }
            QPushButton:disabled { background-color: #94A3B8; color: #E2E8F0; }
            
            QPushButton#btnSecundario {
                background-color: #F8FAFC; color: #2C3E50; border: 2px solid #E0E6ED;
            }
            QPushButton#btnSecundario:hover { background-color: #E0E6ED; }

            QPushButton#btnEliminar {
                background-color: #FEE2E2; color: #DC2626; border: none; padding: 10px; font-size: 16px;
            }
            QPushButton#btnEliminar:hover { background-color: #FECACA; }

            QTableWidget {
                background-color: #FFFFFF; border: 1px solid #E0E6ED; border-radius: 8px; color: #2C3E50;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #F8FAFC; }
            QTableWidget::item:selected { background-color: #0F62FE; color: #FFFFFF; }
            QHeaderView::section {
                background-color: #1E2A38; color: #FFFFFF; font-weight: bold; padding: 10px; border: none;
            }

            QFrame#tarjetaForm, QFrame#tarjetaInfo {
                background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E0E6ED;
            }
            QFrame#tarjetaInfo { background-color: #F0F4F8; border-left: 5px solid #0F62FE; }
            QLabel { font-size: 14px; font-weight: bold; color: #2C3E50; border: none; }
            QScrollArea { border: none; }
        """)

    # =========================================================
    # LÓGICA DE INTERFAZ Y DATOS
    # =========================================================
    def cargar_consultas(self):
        id_medico = self.ventana.id_personal_sesion
        if id_medico is None:
            self.tabla.setRowCount(0)
            return
        datos = self.dao.listar_pendientes_medico(id_medico)
        self.llenar_tabla(datos)
        self.btn_atender.setEnabled(False)
        self.id_consulta_seleccionada = None

    def llenar_tabla(self, datos):
        self.tabla.setRowCount(0)
        for fila_idx, fila in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            for col_idx, valor in enumerate(fila):
                self.tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))
        self.tabla.resizeRowsToContents()

    def seleccionar_fila(self, fila, columna):
        self.id_consulta_seleccionada = int(self.tabla.item(fila, 0).text())
        self.btn_atender.setEnabled(True)

    def abrir_atencion(self):
        fila = self.tabla.currentRow()
        if fila < 0 or self.id_consulta_seleccionada is None:
            return

        # Limpiar receta anterior
        self.limpiar_receta()

        paciente = self.tabla.item(fila, 1).text()
        fecha = self.tabla.item(fila, 2).text()
        motivo = self.tabla.item(fila, 3).text()
        sangre = self.tabla.item(fila, 4).text()
        alergias = self.tabla.item(fila, 5).text()

        self.lbl_titulo_atencion.setText(f"Atendiendo Consulta #{self.id_consulta_seleccionada}")
        self.lbl_paciente.setText(paciente)
        self.lbl_fecha.setText(fecha)
        self.lbl_sangre.setText(sangre)
        self.lbl_alergias.setText(alergias)
        self.lbl_motivo.setText(motivo)

        self.texto_diagnostico.clear()
        self.texto_nota.clear()
        
        # Agregamos una fila vacía por defecto a la receta
        self.agregar_fila_receta()
        
        self.stacked.setCurrentIndex(1)

    # =========================================================
    # LÓGICA DE RECETA DINÁMICA
    # =========================================================
    def agregar_fila_receta(self):
        fila_widget = QWidget()
        layout_fila = QHBoxLayout(fila_widget)
        layout_fila.setContentsMargins(0, 0, 0, 0)
        layout_fila.setSpacing(10)

        input_med = QLineEdit()
        input_med.setPlaceholderText("Nombre del medicamento")
        
        input_dosis = QLineEdit()
        input_dosis.setPlaceholderText("Ej. 1 tableta c/8 hrs por 5 días")
        
        btn_eliminar = QPushButton("❌")
        btn_eliminar.setObjectName("btnEliminar")
        btn_eliminar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_eliminar.setFixedWidth(45)
        
        layout_fila.addWidget(input_med, 2)   # Proporción 2
        layout_fila.addWidget(input_dosis, 3) # Proporción 3 (más ancha)
        layout_fila.addWidget(btn_eliminar)

        self.contenedor_medicamentos.addWidget(fila_widget)
        
        # Guardar las referencias para extraer los textos y para eliminar la fila
        fila_datos = {"widget": fila_widget, "med": input_med, "dosis": input_dosis}
        self.filas_receta.append(fila_datos)
        
        btn_eliminar.clicked.connect(lambda: self.eliminar_fila_receta(fila_datos))

    def eliminar_fila_receta(self, fila_datos):
        widget = fila_datos["widget"]
        self.contenedor_medicamentos.removeWidget(widget)
        widget.deleteLater()
        if fila_datos in self.filas_receta:
            self.filas_receta.remove(fila_datos)

    def limpiar_receta(self):
        for fila_datos in self.filas_receta:
            self.contenedor_medicamentos.removeWidget(fila_datos["widget"])
            fila_datos["widget"].deleteLater()
        self.filas_receta.clear()

    # =========================================================
    # GUARDAR DATOS
    # =========================================================
    def guardar_atencion(self):
        diagnostico = self.texto_diagnostico.toPlainText().strip()
        nota = self.texto_nota.toPlainText().strip()

        if not diagnostico or not nota:
            QMessageBox.warning(self, "Validación", "El diagnóstico y la nota médica son obligatorios.")
            return

        # Extraer la lista de medicamentos ingresados
        lista_receta = []
        for fila in self.filas_receta:
            med = fila["med"].text().strip()
            dosis = fila["dosis"].text().strip()
            if med and dosis:
                lista_receta.append((med, dosis))
            elif med or dosis:
                QMessageBox.warning(self, "Validación Receta", "Si ingresas un medicamento, debes especificar su dosis (y viceversa).")
                return

        # Llamar al DAO actualizado
        exito, error = self.dao.atender_consulta(
            self.id_consulta_seleccionada, diagnostico, nota, lista_receta
        )
        
        if exito:
            QMessageBox.information(self, "Éxito", "Atención y receta guardadas correctamente.")
            self.volver_a_lista()
        else:
            QMessageBox.critical(self, "Error", error)

    def volver_a_lista(self):
        self.id_consulta_seleccionada = None
        self.btn_atender.setEnabled(False)
        self.cargar_consultas()
        self.stacked.setCurrentIndex(0)