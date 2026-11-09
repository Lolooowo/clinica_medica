from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox, 
    QStackedWidget, QFrame, QFormLayout, QDateEdit, QComboBox,
    QCompleter, QHeaderView, QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QCursor

from dao.paciente_dao import PacienteDAO


class BuscarPaciente(QWidget):
    def __init__(self, volver_al_menu):
        super().__init__()
        self.dao = PacienteDAO()
        self.volver_al_menu = volver_al_menu
        self.id_seleccionado = None
        
        self.init_ui()
        self.cargar_tipos_sangre()
        self.cargar_pacientes()

    def init_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        self.stacked = QStackedWidget()
        layout_principal.addWidget(self.stacked)

        # =========================================================
        # PÁGINA 0: LISTA DE PACIENTES Y BÚSQUEDA
        # =========================================================
        self.page_lista = QWidget()
        layout_lista = QVBoxLayout(self.page_lista)
        layout_lista.setContentsMargins(40, 40, 40, 40)
        layout_lista.setSpacing(20)

        titulo_lista = QLabel("Directorio de Pacientes")
        titulo_lista.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        titulo_lista.setStyleSheet("color: #1E2A38;")
        layout_lista.addWidget(titulo_lista)

        # Buscador con Autocompletado
        busqueda_layout = QHBoxLayout()
        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar paciente por nombre completo (Separados por coma) Ej. Juan,Pérez")
        
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.input_busqueda.setCompleter(self.completer)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        busqueda_layout.addWidget(self.input_busqueda)
        busqueda_layout.addWidget(self.btn_buscar)
        layout_lista.addLayout(busqueda_layout)

        # Tabla Principal
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre Completo del Paciente"])
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabla.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.cellDoubleClicked.connect(self.abrir_edicion_desde_boton)
        layout_lista.addWidget(self.tabla)

        # Botones de Acción (Editar e Historial)
        btn_layout = QHBoxLayout()
        self.btn_editar = QPushButton("Editar Paciente")
        self.btn_editar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_editar.setObjectName("btnSecundario")
        self.btn_editar.clicked.connect(self.abrir_edicion_desde_boton)
        
        self.btn_historial = QPushButton(" Ver Historial Médico")
        self.btn_historial.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_historial.clicked.connect(self.abrir_historial_desde_boton)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_editar)
        btn_layout.addWidget(self.btn_historial)
        layout_lista.addLayout(btn_layout)

        self.stacked.addWidget(self.page_lista) # Index 0

        # =========================================================
        # PÁGINA 1: FORMULARIO DE EDICIÓN
        # =========================================================
        self.page_edicion = QWidget()
        layout_edicion = QVBoxLayout(self.page_edicion)
        layout_edicion.setContentsMargins(40, 40, 40, 40)
        layout_edicion.setSpacing(20)

        titulo_edicion = QLabel("Detalles del Paciente")
        titulo_edicion.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        titulo_edicion.setStyleSheet("color: #1E2A38;")
        layout_edicion.addWidget(titulo_edicion)

        tarjeta_edicion = QFrame()
        tarjeta_edicion.setObjectName("tarjetaForm")
        form_layout = QVBoxLayout(tarjeta_edicion)
        form_layout.setContentsMargins(30, 30, 30, 30)
        
        form = QFormLayout()
        form.setSpacing(15)

        self.input_nombres = QLineEdit()
        self.input_apellidos = QLineEdit()
        self.input_fecha_nac = QDateEdit()
        self.input_fecha_nac.setCalendarPopup(True)
        self.combo_tipo_sangre = QComboBox()
        self.combo_tipo_sangre.addItem("Sin especificar", None)
        self.combo_tipo_sangre.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.input_alergias = QLineEdit()

        form.addRow("Nombres:", self.input_nombres)
        form.addRow("Apellidos:", self.input_apellidos)
        form.addRow("Fecha de nacimiento:", self.input_fecha_nac)
        form.addRow("Tipo de sangre:", self.combo_tipo_sangre)
        form.addRow("Alergias conocidas:", self.input_alergias)
        form_layout.addLayout(form)

        botones_edicion = QHBoxLayout()
        self.btn_volver_lista = QPushButton("Volver a la Lista")
        self.btn_volver_lista.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.btn_volver_lista.clicked.connect(self.volver_a_lista)
        self.btn_guardar.clicked.connect(self.actualizar_paciente)

        botones_edicion.addStretch()
        botones_edicion.addWidget(self.btn_volver_lista)
        botones_edicion.addWidget(self.btn_guardar)
        form_layout.addSpacing(15)
        form_layout.addLayout(botones_edicion)

        layout_edicion.addWidget(tarjeta_edicion)
        layout_edicion.addStretch()
        self.stacked.addWidget(self.page_edicion) # Index 1

        # =========================================================
        # PÁGINA 2: HISTORIAL MÉDICO
        # =========================================================
        self.page_historial = QWidget()
        layout_historial = QVBoxLayout(self.page_historial)
        layout_historial.setContentsMargins(40, 40, 40, 40)
        layout_historial.setSpacing(20)

        titulo_historial = QLabel("Expediente Clínico")
        titulo_historial.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        titulo_historial.setStyleSheet("color: #1E2A38;")
        layout_historial.addWidget(titulo_historial)

        # Tarjeta de resumen superior (Datos estáticos)
        tarjeta_resumen = QFrame()
        tarjeta_resumen.setObjectName("tarjetaResumen")
        layout_resumen = QFormLayout(tarjeta_resumen)
        layout_resumen.setContentsMargins(20, 20, 20, 20)
        
        self.lbl_hist_paciente = QLabel()
        self.lbl_hist_fecha_nac = QLabel()
        self.lbl_hist_sangre = QLabel()
        self.lbl_hist_alergias = QLabel()
        
        # Aplicamos estilo a las etiquetas de datos dinámicos para resaltarlas
        estilo_dato = "color: #0F62FE; font-size: 15px; font-weight: bold;"
        for lbl in [self.lbl_hist_paciente, self.lbl_hist_fecha_nac, self.lbl_hist_sangre, self.lbl_hist_alergias]:
            lbl.setStyleSheet(estilo_dato)

        layout_resumen.addRow(QLabel("Paciente:"), self.lbl_hist_paciente)
        layout_resumen.addRow(QLabel("Fecha de Nac:"), self.lbl_hist_fecha_nac)
        layout_resumen.addRow(QLabel("Tipo de Sangre:"), self.lbl_hist_sangre)
        layout_resumen.addRow(QLabel("Alergias:"), self.lbl_hist_alergias)
        layout_historial.addWidget(tarjeta_resumen)

        # Tabla del historial de consultas
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(6)
        self.tabla_historial.setHorizontalHeaderLabels([
            "Fecha Consulta", "Médico", "Motivo", "Diagnóstico", "Nota Médica", "Receta Médica"
        ])
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_historial.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabla_historial.verticalHeader().setVisible(False)
        self.tabla_historial.setWordWrap(True) # Para que textos largos bajen de línea
        layout_historial.addWidget(self.tabla_historial)

        # Botón volver
        btn_hist_layout = QHBoxLayout()
        self.btn_volver_lista_hist = QPushButton("Volver a la Lista")
        self.btn_volver_lista_hist.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_volver_lista_hist.clicked.connect(self.volver_a_lista)
        
        btn_hist_layout.addStretch()
        btn_hist_layout.addWidget(self.btn_volver_lista_hist)
        layout_historial.addLayout(btn_hist_layout)

        self.stacked.addWidget(self.page_historial) # Index 2

        # =========================================================
        # ESTILOS QSS
        # =========================================================
        self.setStyleSheet("""
            QWidget { background-color: #F4F7F6; }
            
            QLineEdit {
                border: 2px solid #E0E6ED; border-radius: 8px; padding: 10px;
                font-size: 14px; background: #FFFFFF; color: #1E2A38; min-height: 25px;
            }
            QLineEdit:focus { border: 2px solid #0F62FE; }
            
            QPushButton {
                background-color: #0F62FE; color: white; border: none;
                border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0050E6; }
            
            QPushButton#btnSecundario, QPushButton[text="Volver a la Lista"] {
                background-color: #F8FAFC; color: #2C3E50; border: 2px solid #E0E6ED;
            }
            QPushButton#btnSecundario:hover, QPushButton[text="Volver a la Lista"]:hover { 
                background-color: #E0E6ED; 
            }

            QTableWidget {
                background-color: #FFFFFF; border: 1px solid #E0E6ED;
                border-radius: 8px; font-size: 14px; color: #2C3E50;
            }
            QTableWidget::item { padding: 10px; border-bottom: 1px solid #F8FAFC; }
            QTableWidget::item:selected { background-color: #0F62FE; color: #FFFFFF; }
            QHeaderView::section {
                background-color: #1E2A38; color: #FFFFFF; font-weight: bold;
                padding: 10px; border: none;
            }

            QFrame#tarjetaForm, QFrame#tarjetaResumen {
                background-color: #FFFFFF; border-radius: 12px; border: 1px solid #E0E6ED;
            }
            QLabel { font-size: 14px; font-weight: bold; color: #2C3E50; border: none; }
            
            QDateEdit, QComboBox {
                border: 2px solid #E0E6ED; border-radius: 8px; padding: 10px;
                font-size: 14px; background: #F8FAFC; color: #1E2A38; min-height: 25px;
            }
            QDateEdit:focus, QComboBox:focus { border: 2px solid #0F62FE; background: #FFFFFF; }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF; color: #1E2A38;
                selection-background-color: #0F62FE; selection-color: #FFFFFF;
                border: 1px solid #E0E6ED;
            }
        """)

        self.btn_buscar.clicked.connect(self.buscar_pacientes)
        self.input_busqueda.returnPressed.connect(self.buscar_pacientes)

    # =========================================================
    # LÓGICA DE DATOS
    # =========================================================
    def cargar_tipos_sangre(self):
        tipos = self.dao.listar_tipos_sangre()
        for id_tipo, nombre in tipos:
            self.combo_tipo_sangre.addItem(nombre, id_tipo)

    def cargar_pacientes(self):
        datos = self.dao.listar_todos()
        self.llenar_tabla(datos)

    def llenar_tabla(self, datos):
        self.tabla.setRowCount(0)
        lista_nombres = [] 

        for fila_idx, fila in enumerate(datos):
            self.tabla.insertRow(fila_idx)
            id_paciente = str(fila[0])
            nombre_completo = f"{fila[1]}, {fila[2]}"
            
            self.tabla.setItem(fila_idx, 0, QTableWidgetItem(id_paciente))
            self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre_completo))
            lista_nombres.append(nombre_completo)

        from PyQt6.QtCore import QStringListModel
        modelo = QStringListModel(lista_nombres)
        self.completer.setModel(modelo)

    def buscar_pacientes(self):
        texto = self.input_busqueda.text().strip()
        if texto == "":
            self.cargar_pacientes()
        else:
            datos = self.dao.buscar(texto)
            self.llenar_tabla(datos)

    def volver_a_lista(self):
        self.id_seleccionado = None
        self.input_busqueda.clear()
        self.cargar_pacientes()
        self.stacked.setCurrentIndex(0)

    # =========================================================
    # EDICIÓN DE PACIENTES (Index 1)
    # =========================================================
    def abrir_edicion_desde_boton(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un paciente de la tabla primero.")
            return
        
        self.id_seleccionado = int(self.tabla.item(fila, 0).text())
        datos = self.dao.obtener_paciente(self.id_seleccionado)
        if datos is None:
            QMessageBox.warning(self, "Error", "No se encontró el paciente.")
            return

        self.input_nombres.setText(datos[1])
        self.input_apellidos.setText(datos[2])
        self.input_fecha_nac.setDate(QDate.fromString(str(datos[3]), "yyyy-MM-dd"))

        index = self.combo_tipo_sangre.findText(datos[4])
        if index >= 0:
            self.combo_tipo_sangre.setCurrentIndex(index)
        else:
            self.combo_tipo_sangre.setCurrentIndex(0)

        alergias = datos[5]
        if alergias == "Sin alergias":
            self.input_alergias.clear()
        else:
            self.input_alergias.setText(alergias)

        self.stacked.setCurrentIndex(1)

    def actualizar_paciente(self):
        if not self.input_nombres.text().strip() or not self.input_apellidos.text().strip():
            QMessageBox.warning(self, "Validación", "Nombres y apellidos son obligatorios.")
            return

        id_tipo_sangre = self.combo_tipo_sangre.currentData()
        exito, error = self.dao.actualizar(
            self.id_seleccionado, self.input_nombres.text().strip(),
            self.input_apellidos.text().strip(), self.input_fecha_nac.date().toString("yyyy-MM-dd"),
            id_tipo_sangre
        )
        
        if exito:
            texto_alergias = self.input_alergias.text().strip()
            alergias_actuales = self.dao.listar_alergias(self.id_seleccionado)
            alergias_nuevas = [a.strip().lower() for a in texto_alergias.split(",") if a.strip()]

            for nombre in alergias_actuales:
                if nombre not in alergias_nuevas:
                    id_alergia = self.dao.buscar_o_crear_alergia(nombre)
                    if id_alergia is not None:
                        self.dao.desvincular_alergia(self.id_seleccionado, id_alergia)

            for nombre in alergias_nuevas:
                id_alergia = self.dao.buscar_o_crear_alergia(nombre)
                if id_alergia is not None:
                    self.dao.vincular_alergia(self.id_seleccionado, id_alergia)

            QMessageBox.information(self, "Éxito", "Paciente actualizado correctamente.")
            self.volver_a_lista()
        else:
            QMessageBox.critical(self, "Error", "No se pudo actualizar el paciente.")

    # =========================================================
    # HISTORIAL MÉDICO (Index 2)
    # =========================================================
    def abrir_historial_desde_boton(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Selección", "Selecciona un paciente de la tabla primero.")
            return
            
        self.id_seleccionado = int(self.tabla.item(fila, 0).text())
        
        # Llamar a la nueva vista a través del DAO
        registros = self.dao.obtener_historial(self.id_seleccionado)
        
        if not registros:
            QMessageBox.warning(self, "Historial", "No se encontró información para este paciente.")
            return

        # La vista siempre devuelve al menos una fila (por el LEFT JOIN a paciente)
        primer_registro = registros[0]
        
        # Llenar la tarjeta superior con datos estáticos del paciente
        self.lbl_hist_paciente.setText(str(primer_registro[1]))
        self.lbl_hist_fecha_nac.setText(str(primer_registro[2]))
        self.lbl_hist_sangre.setText(str(primer_registro[3]))
        self.lbl_hist_alergias.setText(str(primer_registro[4]))

        # Llenar la tabla inferior con las consultas
        self.tabla_historial.setRowCount(0)
        
        # Si fila[5] (id_consulta) es None, significa que el paciente está registrado pero no tiene citas
        if primer_registro[5] is None:
            self.tabla_historial.insertRow(0)
            self.tabla_historial.setItem(0, 0, QTableWidgetItem("Sin registros"))
            self.tabla_historial.setItem(0, 1, QTableWidgetItem("-"))
            self.tabla_historial.setItem(0, 2, QTableWidgetItem("El paciente aún no tiene consultas previas."))
            self.tabla_historial.setItem(0, 3, QTableWidgetItem("-"))
            self.tabla_historial.setItem(0, 4, QTableWidgetItem("-"))
            self.tabla_historial.setItem(0, 5, QTableWidgetItem("-"))
        else:
            for idx, reg in enumerate(registros):
                self.tabla_historial.insertRow(idx)
                
                # Formatear la fecha
                fecha_formato = reg[6].strftime("%d/%m/%Y %H:%M") if reg[6] else "N/A"
                
                self.tabla_historial.setItem(idx, 0, QTableWidgetItem(fecha_formato))
                self.tabla_historial.setItem(idx, 1, QTableWidgetItem(str(reg[8] or "N/A")))
                self.tabla_historial.setItem(idx, 2, QTableWidgetItem(str(reg[7] or "N/A")))
                self.tabla_historial.setItem(idx, 3, QTableWidgetItem(str(reg[9] or "Pendiente/N/A")))
                self.tabla_historial.setItem(idx, 4, QTableWidgetItem(str(reg[10] or "Pendiente/N/A")))
                self.tabla_historial.setItem(idx, 5, QTableWidgetItem(str(reg[11] or "Sin receta")))
                
            # Ajustar la altura de las celdas automáticamente para leer todo el diagnóstico
            self.tabla_historial.resizeRowsToContents()

        # Cambiar a la vista del historial
        self.stacked.setCurrentIndex(2)