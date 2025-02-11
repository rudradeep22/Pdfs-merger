import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyPDF2 import PdfReader, PdfWriter

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        main_layout.addWidget(self.list_widget)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.btn_add = QPushButton("Add PDF")
        self.btn_add.clicked.connect(self.add_pdf)
        buttons_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Remove PDF")
        self.btn_remove.clicked.connect(self.remove_pdf)
        buttons_layout.addWidget(self.btn_remove)

        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.clicked.connect(self.merge_pdfs)
        buttons_layout.addWidget(self.btn_merge)

    def add_pdf(self):
        """Opens a file dialog to select one or more PDF files."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "",
                                                "PDF Files (*.pdf)", options=options)
        if files:
            for file in files:
                if not any(self.list_widget.item(i).text() == file for i in range(self.list_widget.count())):
                    self.list_widget.addItem(file)

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
