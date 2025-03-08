import sys
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt

DATA_FILE = "calendar_data.json"

class CalendarWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario de Publicaciones")
        self.setGeometry(100, 100, 500, 350)
        
        layout = QVBoxLayout()
        
        # Crear tabla
        self.table = QTableWidget()
        self.table.setRowCount(5)  # 5 redes sociales
        self.table.setColumnCount(7)  # 7 días de la semana
        
        # Configurar encabezados
        self.table.setHorizontalHeaderLabels(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        self.table.setVerticalHeaderLabels(["Facebook", "Instagram", "TikTok", "YouTube", "Pinterest"])
        
        # Cargar datos guardados
        self.load_data()
        
        # Conectar clics en la tabla
        self.table.cellClicked.connect(self.toggle_cell)
        
        # Botón para limpiar la tabla
        self.clear_button = QPushButton("Reiniciar Semana")
        self.clear_button.clicked.connect(self.clear_table)
        
        layout.addWidget(self.table)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)
    
    def toggle_cell(self, row, col):
        item = self.table.item(row, col)
        if item is None or item.text() == "":
            self.table.setItem(row, col, QTableWidgetItem("✔"))
        else:
            self.table.setItem(row, col, QTableWidgetItem(""))
        self.save_data()
    
    def save_data(self):
        data = {}
        for row in range(5):
            for col in range(7):
                item = self.table.item(row, col)
                data[f"{row},{col}"] = item.text() if item else ""
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    
    def load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            for key, value in data.items():
                row, col = map(int, key.split(","))
                if value:
                    self.table.setItem(row, col, QTableWidgetItem(value))
        except FileNotFoundError:
            pass
    
    def clear_table(self):
        self.table.clearContents()
        self.save_data()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Publicaciones")
        self.setGeometry(100, 100, 300, 200)
        
        # Configurar el fondo de la ventana
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2c3e50"))  # Azul oscuro moderno
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        
        # Agregar título
        self.title = QLabel("Organizador")
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setStyleSheet("color: white; text-align: center;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)
        
        # Crear botón con estilo
        self.calendar_button = QPushButton("Calendario de Publicaciones")
        
        # Aplicar estilo al botón
        button_style = (
            "QPushButton {"
            "background-color: #3498db; color: white; border-radius: 10px; padding: 10px;"
            "font-size: 14px;"
            "min-width: 150px;"
            "}"
            "QPushButton:hover {background-color: #2980b9;}"
        )
        
        self.calendar_button.setStyleSheet(button_style)
        
        layout.addWidget(self.calendar_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        
        # Conectar botón de calendario a la nueva ventana
        self.calendar_button.clicked.connect(self.open_calendar)
    
    def open_calendar(self):
        self.calendar_window = CalendarWindow()
        self.calendar_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
