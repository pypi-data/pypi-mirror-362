import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox, 
    QFileDialog, QLabel, QTextEdit, QStatusBar, QToolBar, QAction
)
from PyQt5.QtCore import Qt, QThread, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices

import subprocess
import signal
import os


import simple_ocrmypdf.about as about
from simple_ocrmypdf.modules.wabout   import show_about_window
from simple_ocrmypdf.desktop import create_desktop_file, create_desktop_directory, create_desktop_menu

#sudo apt install ocrmypdf



def exec_ocrmypdf(input_path: str, output_path: str) -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["ocrmypdf", input_path, output_path],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        # Mesmo em caso de erro, retornamos as saídas para depuração
        return e.stdout, e.stderr
    except FileNotFoundError:
        return "", "Erro: ocrmypdf não está instalado ou não está no PATH."


def add_ocr_in_name(pdf_path: str) -> str:
    base, ext = os.path.splitext(pdf_path)
    return f"{base}.ocr.pdf"

# Thread que vai rodar a função lenta
class WorkerThread(QThread):
    def __init__(self, input_path, output_path):
        super().__init__() 
        self.input_path = input_path
        self.outputt_path = output_path
        self.output_std = ""
        self.output_err = ""
        
    def run(self):
        self.output_std, self.output_err = exec_ocrmypdf(   self.input_path,
                                                            self.outputt_path)

    
class DragDropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setText("Or drag and drop PDF or BMP or PNG or JPG file here")
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)  # Ativa quebra de linha
        self.setStyleSheet("border: 2px dashed #aaa; padding: 10px;")
        
        self.file = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.file = urls[0].toLocalFile()
            
            if self.file.lower().endswith(".pdf") or \
               self.file.lower().endswith(".bmp") or \
               self.file.lower().endswith(".png") or \
               self.file.lower().endswith(".jpg") or \
               self.file.lower().endswith(".jpeg"):
                self.setText(self.file)
            else:
                self.file = None


class MainWindow(QMainWindow):
    ############################################################################
    def __init__(self):
        super().__init__()
        self.setWindowTitle(about.__program_name__)
        self.setGeometry(100, 100, 400, 300)

        ## Icon
        # Get base directory for icons
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')
        self.setWindowIcon(QIcon(icon_path)) 

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Coffee
        coffee_action = QAction(QIcon.fromTheme("emblem-favorite"),"Coffee", self)
        coffee_action.setToolTip("Buy me a coffee (TrucomanX)")
        coffee_action.triggered.connect(self.on_coffee_action_click)
        toolbar.addAction(coffee_action)
                
        # About
        about_action = QAction(QIcon.fromTheme("help-about"),"About", self)
        about_action.setToolTip("About the program")
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)

        # Widgets
        
        # Select
        self.select_button = QPushButton("Select PDF or IMAGE file")
        self.select_button.setToolTip("Select the file that needs to be OCR applied.")
        self.select_button.setIcon(QIcon.fromTheme("x-office-document-template"))
        self.select_button.clicked.connect(self.select_file)

        # Drag and drop
        self.drag_drop_area = DragDropArea()

        # Print
        self.save_button = QPushButton("Save OCR file")
        self.save_button.setToolTip("Save the file with OCR (Optical Character Recognition) applied.")
        self.save_button.setIcon(QIcon.fromTheme("document-save-as"))
        self.save_button.clicked.connect(self.print_file)


        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.select_button)
        layout.addWidget(self.drag_drop_area)
        layout.addWidget(self.save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.rodando = False
        
        # Timer para mostrar "atividade"
        self.contador = 0
        self.timer = self.startTimer(500)  # Atualiza a cada 500ms

    ############################################################################
    def timerEvent(self, event):
        if self.rodando:
            pontos = '.' * (self.contador % 32)
            self.status.showMessage(f"Working{pontos}")
            self.contador += 1

    ############################################################################
    def on_coffee_action_click(self):
        QDesktopServices.openUrl(QUrl("https://ko-fi.com/trucomanx"))

    ############################################################################
    def show_about(self):
        #QMessageBox.information(self, "Sobre", "Exemplo criado com PyQt5.\n(c) Fernando")
        
        data = {
            "version": about.__version__,
            "package": about.__package__,
            "program_name": about.__program_name__,
            "author": about.__author__,
            "email": about.__email__,
            "description": about.__description__,
            "url_source": about.__url_source__,
            "url_funding": about.__url_funding__,
            "url_bugs": about.__url_bugs__
        }
        
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_dir_path, 'icons', 'logo.png')
        
        show_about_window(data,logo_path)

    ############################################################################
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName( self, 
                                                    "Select file", 
                                                    "", 
                                                    "Selected file (*.pdf *.png *.jpg *.jpeg *.bmp)")
        
        if file_path: 
            if  file_path.lower().endswith(".pdf") or \
                file_path.lower().endswith(".bmp") or \
                file_path.lower().endswith(".png") or \
                file_path.lower().endswith(".jpg") or \
                file_path.lower().endswith(".jpeg"):
                self.drag_drop_area.setText(file_path)

    ############################################################################
    def funcao_finalizou(self):
        self.status.showMessage("Work end!", 3000)  # Mostra por 3 segundos
        
        self.rodando = False
        self.save_button.setEnabled(True)
        
        if self.thread.output_std != "":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.critical)
            msg.setWindowTitle("Error output")
            msg.setText(self.thread.output_std)
            msg.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
            msg.exec()
            
        if self.thread.output_err != "":
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("All OK - Work ended!")
            msg.setText(self.thread.output_err)
            msg.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
            msg.exec()

        
    ############################################################################
    def print_file(self):
        if self.rodando:
            return
            
        input_path = self.drag_drop_area.text()
        new_pdf = add_ocr_in_name(input_path)

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF file",
            new_pdf,  # <--- sugestão de nome
            "PDF files (*.pdf)"
        )

        if file_path:
            if not file_path.lower().endswith(".pdf"):
                file_path += ".pdf"  
            new_pdf = file_path  
            
            self.save_button.setEnabled(False)
            #str_std, str_err = exec_ocrmypdf(input_path, new_pdf)
            
            self.rodando = True
            self.status.showMessage("Working")
            self.thread = WorkerThread(input_path, new_pdf)
            self.thread.finished.connect(self.funcao_finalizou)
            self.thread.start()


        else:
            QMessageBox.warning(self, "No file", "You did not select any file.")



def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    create_desktop_directory()    
    create_desktop_menu()
    create_desktop_file('~/.local/share/applications')
    
    for n in range(len(sys.argv)):
        if sys.argv[n] == "--autostart":
            create_desktop_directory(overwrite = True)
            create_desktop_menu(overwrite = True)
            create_desktop_file('~/.config/autostart', overwrite=True)
            return
        if sys.argv[n] == "--applications":
            create_desktop_directory(overwrite = True)
            create_desktop_menu(overwrite = True)
            create_desktop_file('~/.local/share/applications', overwrite=True)
            return
    
    app = QApplication(sys.argv)
    app.setApplicationName(about.__package__) # xprop WM_CLASS # *.desktop -> StartupWMClass
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
