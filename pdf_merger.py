import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, 
    QLabel, QFrame, QStyle, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyPDF2 import PdfReader, PdfWriter

class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.initUI()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton#removeBtn {
                background-color: #f44336;
            }
            QPushButton#removeBtn:hover {
                background-color: #d32f2f;
            }
        """)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        central_widget.setLayout(main_layout)

        # Title Label with icon
        title_layout = QHBoxLayout()
        title_icon = QLabel()
        # Replace SP_DrivePDFFile with SP_FileIcon
        title_icon.setPixmap(self.style().standardIcon(QStyle.SP_FileIcon).pixmap(32, 32))
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("PDF Merger")
        title_font = QFont("Segoe UI", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        title_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(title_layout)

        # Instructions Label
        instructions = QLabel("Drag and drop PDF files to reorder them")
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(instructions)

        # Frame for the PDF list
        list_frame = QFrame()
        list_frame.setFrameShape(QFrame.StyledPanel)
        list_layout = QVBoxLayout()
        list_layout.setContentsMargins(10, 10, 10, 10)
        list_frame.setLayout(list_layout)

        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.setMinimumHeight(300)
        list_layout.addWidget(self.list_widget)
        main_layout.addWidget(list_frame)

        # Progress Bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        main_layout.addLayout(buttons_layout)

        # Add PDF button
        self.btn_add = QPushButton("Add PDF")
        self.btn_add.setIcon(QIcon("pdf-file.png"))
        self.btn_add.clicked.connect(self.add_pdf)
        buttons_layout.addWidget(self.btn_add)

        # Remove PDF button
        self.btn_remove = QPushButton("Remove PDF")
        self.btn_remove.setObjectName("removeBtn")
        self.btn_remove.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.btn_remove.clicked.connect(self.remove_pdf)
        buttons_layout.addWidget(self.btn_remove)

        # Merge PDFs button
        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.btn_merge.clicked.connect(self.merge_pdfs)
        buttons_layout.addWidget(self.btn_merge)

        # Status Label
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        main_layout.addWidget(self.status_label)

    def add_pdf(self):
        """Opens a file dialog to select one or more PDF files and adds them with default PDF icons."""
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Select PDF files",
            "",
            "PDF Files (*.pdf)",
            options=options
        )
        if files:
            for file in files:
                if not any(self.list_widget.item(i).text() == file 
                          for i in range(self.list_widget.count())):
                    # Replace SP_DrivePDFFile with SP_FileIcon here too
                    item = QListWidgetItem(
                        self.style().standardIcon(QStyle.SP_FileIcon),
                        file
                    )
                    self.list_widget.addItem(item)
            self.status_label.setText(f"{len(files)} PDF(s) added")

    def remove_pdf(self):
        """Removes the selected PDF files from the list."""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            self.status_label.setText("No files selected to remove")
            return
        for item in selected_items:
            self.list_widget.takeItem(self.list_widget.row(item))
        self.status_label.setText(f"{len(selected_items)} PDF(s) removed")

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
