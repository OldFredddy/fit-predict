import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

# Для импорта load_model, prepare_data, predict, calculate_probability, column_names из вашего модуля
# Обновите путь импорта в соответствии с вашей структурой проекта
from predict import load_model, prepare_data, predict, calculate_probability, column_names

class DragDropBox(QLineEdit):
    def __init__(self, placeholder_text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText(placeholder_text)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 5px;
                background: #333333;
                color: #ffffff;
            }
            QLineEdit:hover {
                border: 2px solid #aaaaaa;
            }
        """)
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            if urls and len(urls) == 1:
                filepath = str(urls[0].toLocalFile())
                self.setText(filepath)
        else:
            event.ignore()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 200)
        self.setWindowTitle('Предсказание данных с Drag and Drop')
        self.setStyleSheet("""
            QWidget {
                background-color: #222222;
            }
            QPushButton {
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 5px;
                background: #333333;
                color: #ffffff;
            }
            QPushButton:hover {
                border: 2px solid #aaaaaa;
            }
        """)

        layout = QVBoxLayout()

        self.logPathEdit = DragDropBox("Перетащите сюда файл log")
        self.modelPathEdit = DragDropBox("Перетащите сюда файл модели .joblib")
        self.predictButton = QPushButton("Старт")
        self.predictButton.clicked.connect(self.performPrediction)

        layout.addWidget(self.logPathEdit)
        layout.addWidget(self.modelPathEdit)
        layout.addWidget(self.predictButton)

        self.setLayout(layout)

    def performPrediction(self):
        log_path = self.logPathEdit.text()
        model_path = self.modelPathEdit.text()
        if log_path and model_path:
            model = load_model(model_path)
            data = prepare_data(log_path, column_names)
            predictions = predict(model, data)
            result = calculate_probability(predictions)

            # Создание кастомного QMessageBox
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Результат")
            msgBox.setText(result)

            # Применение кастомного стиля для изменения цвета текста и фона
            msgBox.setStyleSheet("""
            QMessageBox {
                color: #ffffff; /* Белый текст */
                background-color: #333333; /* Темный фон */
            }
            QMessageBox QLabel {
                color: #ffffff; /* Убедитесь, что это изменит цвет текста на белый */
            }
            QMessageBox QPushButton {
                color: #ffffff; /* Белый текст */
                background-color: #555555; /* Темный фон для кнопок */
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 5px;
                min-height: 20px; /* Минимальная высота кнопок */
                min-width: 80px; /* Минимальная ширина кнопок */
            }
            QMessageBox QPushButton:hover {
                border-color: #aaaaaa; /* Цвет границы кнопки при наведении */
            }
        """)
            msgBox.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
