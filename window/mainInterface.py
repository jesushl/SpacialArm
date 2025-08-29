# https://github.com/juan-suarezp/PythonPyQtTutorial
import sys
from PyQt5 import QtWidgets, uic, QtOpenGL, QtGui, QtCore
import OpenGL.GL as gl
from OpenGL import GLU


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        # super.__init__(self,parent)
        QtOpenGL.QGLWidget.__init__(self, parent)
    
    def initializeGL(self) -> None:
        self.qglClearColor(QtGui.QColor(0,0,255))
        gl.glEnable(gl.GL_DEPTH_TEST)
    
    def resizeGL(self, width, height) -> None:
        gl.glViewport(0,0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)
        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        


class ArmWindow(QtWidgets.QMainWindow):
    def __init__(self, root=None):
        QtWidgets.QMainWindow.__init__(self, root)
        uic.loadUi("main.ui", self)
        self.resize(600, 600)
        self.setWindowTitle("Ejemplo")
        self.button_draw.clicked.connect(self.labelNameChange)
        glwidget = GLWidget(self)
        self.openGLWidget = glwidget

    def labelNameChange(self):
        self.label_sample.setText("Tecnologia")

app = QtWidgets.QApplication(sys.argv)
window = ArmWindow()
window.show()
sys.exit(app.exec_())