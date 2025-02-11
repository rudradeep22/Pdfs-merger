import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyPDF2 import PdfReader, PdfWriter

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 600, 450)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        central_widget.setLayout(main_layout)

        # Title Label
        title_label = QLabel("PDF Merger")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Frame for the PDF list
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(5, 5, 5, 5)
        list_frame.setLayout(list_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        list_layout.addWidget(self.list_widget)
        main_layout.addWidget(list_frame)

        # Horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        main_layout.addLayout(buttons_layout)

        self.btn_add = QPushButton("Add PDF")
        self.btn_add.setStyleSheet("padding: 10px;")
        self.btn_add.clicked.connect(self.add_pdf)
        buttons_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Remove PDF")
        self.btn_remove.setStyleSheet("padding: 10px;")
        self.btn_remove.clicked.connect(self.remove_pdf)
        buttons_layout.addWidget(self.btn_remove)

        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.setStyleSheet("padding: 10px;")
        self.btn_merge.clicked.connect(self.merge_pdfs)
        buttons_layout.addWidget(self.btn_merge)

    def add_pdf(self):
        """Opens a file dialog to select one or more PDF files and adds them with default PDF icons."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "",
                                                "PDF Files (*.pdf)", options=options)
        if files:
            for file in files:
                # Prevent adding duplicate entries
                if not any(self.list_widget.item(i).text() == file for i in range(self.list_widget.count())):
                    # Create a list widget item with an icon.
                    item = QListWidgetItem(QIcon("pdf-file.png"), file)
                    self.list_widget.addItem(item)

    def remove_pdf(self):
        """Removes the selected PDF files from the list."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))

    def merge_pdfs(self):
        """Merges the PDFs in the order displayed in the list widget."""
        if self.list_widget.count() == 0:
            QMessageBox.warning(self, "Warning", "No PDF files to merge.")
            return

        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Merged PDF", "",
                                                   "PDF Files (*.pdf)", options=options)
        if not save_path:
            return

        pdf_writer = PdfWriter()
        pdf_files_ordered = [self.list_widget.item(i).text() for i in range(self.list_widget.count())]

        try:
            for pdf_path in pdf_files_ordered:
                pdf_reader = PdfReader(pdf_path)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

            with open(save_path, 'wb') as out_file:
                pdf_writer.write(out_file)

            QMessageBox.information(self, "Success", "PDF files merged successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec_())
