from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox, QHBoxLayout
)
from dao.consulta_dao import ConsultaDAO


class AtenderConsulta(QDialog):
    def __init__(self, id_consulta, datos_consulta, parent=None):
        super().__init__(parent)
        self.id_consulta = id_consulta
        self.dao = ConsultaDAO()
        self.setWindowTitle(f"Atender Consulta #{id_consulta}")
        self.setFixedWidth(500)
        self.init_ui(datos_consulta)

    def init_ui(self, datos):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        
        # Titulo
        titulo = QLabel(f"Atendiendo consulta #{self.id_consulta}")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        # Datos del paciente (solo lectura)
        info = QLabel(
            f"<b>Paciente:</b> {datos[1]}<br>"
            f"<b>Fecha de consulta:</b> {datos[2]}<br>"
            f"<b>Tipo de sangre:</b> {datos[4]}<br>"
            f"<b>Alergias:</b> {datos[5]}"
        )
        info.setWordWrap(True)
        info.setStyleSheet(
            "background-color: #f0f8ff; padding: 10px; "
            "border-radius: 8px; font-size: 13px;"
            "color: #34495e;"
        )
        layout.addWidget(info)

        # Motivo de visita (solo lectura)
        label_motivo = QLabel("Motivo de visita (registrado por recepcion):")
        label_motivo.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(label_motivo)

        motivo = QLabel(datos[3])
        motivo.setWordWrap(True)
        motivo.setStyleSheet(
            "background-color: #fff9e6; padding: 10px; "
            "border-radius: 8px; font-size: 13px;"
            "color: #34495e;"
        )
        layout.addWidget(motivo)

        # Formulario de atencion
        form = QFormLayout()
        self.texto_diagnostico = QTextEdit()
        self.texto_diagnostico.setPlaceholderText(
            "Diagnostico del paciente..."
        )
        self.texto_diagnostico.setMaximumHeight(100)

        self.texto_nota = QTextEdit()
        self.texto_nota.setPlaceholderText(
            "Notas medicas, observaciones, indicaciones..."
        )
        self.texto_nota.setMaximumHeight(100)

        form.addRow("Diagnostico:", self.texto_diagnostico)
        form.addRow("Nota medica:", self.texto_nota)
        layout.addLayout(form)

        # Botones
        botones = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar atencion")
        self.btn_cancelar = QPushButton("Cancelar")

        self.btn_guardar.clicked.connect(self.guardar_atencion)
        self.btn_cancelar.clicked.connect(self.reject)

        botones.addWidget(self.btn_guardar)
        botones.addWidget(self.btn_cancelar)
        layout.addLayout(botones)

    def guardar_atencion(self):
        diagnostico = self.texto_diagnostico.toPlainText().strip()
        nota = self.texto_nota.toPlainText().strip()

        if diagnostico == "" or nota == "":
            QMessageBox.warning(self, "Validacion",
                "Diagnostico y nota medica son obligatorios.")
            return

        exito, error = self.dao.atender_consulta(
            self.id_consulta, diagnostico, nota
        )
        if exito:
            QMessageBox.information(self, "Exito",
                "Atencion registrada correctamente.")
            self.accept()  # cierra el dialogo
        else:
            QMessageBox.critical(self, "Error", error)