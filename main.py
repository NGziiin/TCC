import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget

gui = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(gui, 'gui'))
from gui.inicial import Ui_Form

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.showMaximized()
    sys.exit(app.exec_())