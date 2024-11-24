import sys
import os
from pathlib import Path
import PyPDF2
import pyttsx3
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QWidget,
    QTextEdit,
    QComboBox,
    QMessageBox,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PDFToAudioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF to Audio Converter")
        self.setGeometry(300, 300, 800, 600)  # Improved resolution
        self.pdf_file_path = None
        self.engine = pyttsx3.init()

        # UI Components
        self.label = QLabel("Select a PDF file to convert to audio:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")

        self.preview_box = QTextEdit(self)
        self.preview_box.setReadOnly(True)
        self.preview_box.setPlaceholderText("PDF preview will appear here...")
        self.preview_box.setStyleSheet("background-color: #f4f4f4; padding: 10px;")
        self.preview_box.setFont(QFont("Arial", 12))

        self.browse_button = QPushButton("Browse PDF", self)
        self.browse_button.setStyleSheet("background-color: #0078d7; color: white; font-size: 14px;")
        self.browse_button.clicked.connect(self.browse_pdf)

        self.voice_label = QLabel("Select Voice Type:", self)
        self.voice_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.voice_label.setStyleSheet("font-size: 14px; color: #555;")

        self.voice_dropdown = QComboBox(self)
        self.voice_dropdown.setStyleSheet("padding: 5px; font-size: 14px;")
        self.populate_voice_options()

        self.download_button = QPushButton("Download MP3 to Desktop", self)
        self.download_button.setStyleSheet("background-color: #28a745; color: white; font-size: 14px;")
        self.download_button.clicked.connect(self.save_audio)
        self.download_button.setEnabled(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.browse_button)

        layout.addWidget(self.preview_box)
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(self.voice_label)
        voice_layout.addWidget(self.voice_dropdown)
        layout.addLayout(voice_layout)

        layout.addWidget(self.download_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_pdf(self):
        # Open file dialog to select a PDF file
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select PDF File", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.pdf_file_path = file_path
            self.label.setText(f"Selected File: {file_path}")
            self.download_button.setEnabled(True)
            self.show_pdf_preview()
        else:
            self.label.setText("No file selected.")
            self.preview_box.clear()

    def show_pdf_preview(self):
        """Displays a preview of the PDF content."""
        try:
            pdf_reader = PyPDF2.PdfReader(open(self.pdf_file_path, "rb"))
            preview_text = ""
            for page in pdf_reader.pages[:1]:  # Preview only the first page
                text = page.extract_text()
                if text:
                    preview_text += text.strip()
            self.preview_box.setPlainText(preview_text[:500])  # Show up to 500 characters
        except Exception as e:
            self.preview_box.setPlainText(f"Error reading PDF: {e}")

    def populate_voice_options(self):
        """Populates the dropdown with available voices."""
        voices = self.engine.getProperty("voices")
        for voice in voices:
            self.voice_dropdown.addItem(voice.name)

    def save_audio(self):
        if not self.pdf_file_path:
            QMessageBox.critical(self, "Error", "No PDF file selected!")
            return

        try:
            # Extract audio from the PDF and save to Desktop
            desktop_folder = str(Path.home() / "Desktop")
            output_file_path = os.path.join(desktop_folder, "output.mp3")

            selected_voice = self.voice_dropdown.currentText()
            self.convert_pdf_to_audio(self.pdf_file_path, output_file_path, selected_voice)
            QMessageBox.information(
                self, "Success", f"Audio file saved to Desktop:\n{output_file_path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def convert_pdf_to_audio(self, pdf_file_path, output_file_path, voice_name):
        """Converts a PDF file to audio and saves it to the specified path."""
        pdf_reader = PyPDF2.PdfReader(open(pdf_file_path, "rb"))
        text_to_speech = pyttsx3.init()

        # Set selected voice
        voices = text_to_speech.getProperty("voices")
        for voice in voices:
            if voice.name == voice_name:
                text_to_speech.setProperty("voice", voice.id)
                break

        full_text = ""
        for page in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page].extract_text()
            if text:
                full_text += text.strip().replace("\n", " ")

        text_to_speech.save_to_file(full_text, output_file_path)
        text_to_speech.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFToAudioApp()
    window.show()
    sys.exit(app.exec())
