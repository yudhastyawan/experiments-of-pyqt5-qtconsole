import numpy as np
import sys #,os
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.console_widget import ConsoleWidget

from code_editor import QCodeEditor
import syntax
from qt_canvas import MplCanvas

class EditorText(QtWidgets.QPlainTextEdit):
    def __init__(self, parent=None):
        super(EditorText, self).__init__(parent)
    
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Tab:                
            tc = self.textCursor()
            tc.insertText("    ")
            return
        return QtWidgets.QPlainTextEdit.keyPressEvent(self,event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Editor')
        self.setGeometry(100, 100, 1200, 600)

        self.var1 = 10

        self.button1 = QtWidgets.QPushButton("reset")
        self.button2 = QtWidgets.QPushButton("Execute")
        self.plaintext1 = QCodeEditor()
        # font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont)
        # self.plaintext1.setFont(font)
        self.highlighter = syntax.PythonHighlighter()
        self.highlighter.setDocument(self.plaintext1.document())
        self.hlayout = QtWidgets.QHBoxLayout()
        self.vlayout = QtWidgets.QVBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        self.vlayout.addWidget(self.button1)
        self.vlayout.addWidget(self.plaintext1)
        self.vlayout.addWidget(self.button2)
        self.qwidget = QtWidgets.QWidget()
        self.qwidget.setLayout(self.hlayout)
        self.setCentralWidget(self.qwidget)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.hlayout.addWidget(self.sc)

        # self.plaintext1.setTabStopDistance(
        #     QtGui.QFontMetricsF(self.plaintext1.font()).horizontalAdvance(
        #         ' ' * 4
        #     )
        # )

        self.embed_console()
    
    def embed_console(self):
        global ipython_widget  # Prevent from being garbage collected

        # Create an in-process kernel
        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel(show_banner=False)
        kernel = kernel_manager.kernel
        kernel.gui = 'qt'

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        ipython_widget = RichJupyterWidget()
        ipython_widget.banner = ''
        ipython_widget.kernel_banner = ''
        ipython_widget.kernel_manager = kernel_manager
        ipython_widget.kernel_client = kernel_client
        self.vlayout.addWidget(ipython_widget)

        def execute_prompt():
            ipython_widget._append_plain_text(
                self.plaintext1.toPlainText(), False
            )
            ipython_widget.execute()

        self.button2.clicked.connect(lambda: execute_prompt())
        self.button1.clicked.connect(lambda: ipython_widget.reset(True))
        kernel.shell.push({'s':self, 'k':ipython_widget, 'fig':self.sc, 'ax': self.sc.axes, 'np': np})

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

# ipywid.reset(clear=True)
# .banner
# .kernel_banner
# .append_plain_text(blabla, False)