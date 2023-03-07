import os
import sys
import pptx
import PyPDF2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QTextEdit, QCheckBox

class PPTXtoPDFConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PPTX to PDF Converter'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.filepath_label = QLabel('File path(s):', self)
        self.filepath_label.move(20, 20)

        self.filepath_lineedit = QLineEdit(self)
        self.filepath_lineedit.setReadOnly(True)
        self.filepath_lineedit.setGeometry(90, 20, 400, 20)

        self.browse_button = QPushButton('Browse', self)
        self.browse_button.setGeometry(500, 20, 80, 20)
        self.browse_button.clicked.connect(self.browse_file)

        self.convert_button = QPushButton('Convert', self)
        self.convert_button.setGeometry(270, 80, 80, 30)
        self.convert_button.clicked.connect(self.convert_pptx_to_pdf)

        # Align the "Convert" and "Browse" buttons
        self.convert_button.move(self.browse_button.x(), self.convert_button.y())

        self.selected_files_label = QLabel('Selected Files:', self)
        self.selected_files_label.move(20, 120)

        self.selected_files_textedit = QTextEdit(self)
        self.selected_files_textedit.setGeometry(20, 140, 560, 200)
        self.selected_files_textedit.setReadOnly(True)

        self.num_files_label = QLabel('Number of Files:', self)
        self.num_files_label.move(20, 360)

        self.num_files_value_label = QLabel('0', self)
        self.num_files_value_label.move(130, 360)

        self.combine_files_checkbox = QCheckBox('Combine files into single PDF', self)
        self.combine_files_checkbox.setGeometry(20, 400, 200, 30)

        self.show()

    def browse_file(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open File', os.getenv('HOME'), 'PPTX Files (*.pptx)')
        if filenames:
            self.filepath_lineedit.setText(', '.join(filenames))
            self.selected_files_textedit.setText('\n'.join(filenames))
            self.num_files_value_label.setText(str(len(filenames)))

    def convert_pptx_to_pdf(self):
        filepaths = self.filepath_lineedit.text().split(', ')
        if not filepaths:
            QMessageBox.critical(self, 'Error', 'No files selected.')
            return
        for filepath in filepaths:
            if not filepath.endswith('.pptx'):
                QMessageBox.critical(self, 'Error', f'File "{filepath}" is not a PPTX file.')
                return

        combine_files = self.combine_files_checkbox.isChecked()
        output_file = None
        if combine_files:
            output_file, _ = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'), 'PDF Files (*.pdf)')

        pdf_files = []
        for filepath in filepaths:
            pdf_filepath = filepath.replace('.pptx', '.pdf')
            if os.path.exists(pdf_filepath):
                response = QMessageBox.warning(self, 'Warning', f'File "{pdf_filepath}" already exists. Overwrite?', QMessageBox.Yes | QMessageBox)
                if response == QMessageBox.No:
                    return

            pptx_file = pptx.Presentation(filepath)
            pptx_file.save(pdf_filepath)

        QMessageBox.information(self, 'Success', 'Conversion completed.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PPTXtoPDFConverter()
    sys.exit(app.exec_())