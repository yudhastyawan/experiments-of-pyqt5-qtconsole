# editor.py

from PyQt5 import QtGui, QtWidgets, QtCore
import syntax

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.editor = QtWidgets.QPlainTextEdit(self)
        highlight = syntax.PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

app = QtWidgets.QApplication([])
# editor = QtWidgets.QPlainTextEdit()
# highlight = syntax.PythonHighlighter(editor.document())
# editor.show()
main = MainWindow()
main.show()
# Load syntax.py into the editor for demo purposes
# infile = open('syntax.py', 'r')
# editor.setPlainText(infile.read())

app.exec_()