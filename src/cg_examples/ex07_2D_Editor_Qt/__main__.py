# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
# from PyQt5.QtOpenGL import QGLWidget
# from OpenGL.GL import (
#     GL_COLOR_BUFFER_BIT,
#     GL_DEPTH_BUFFER_BIT,
#     GL_TRIANGLES,
#     glClearColor,
#     glViewport,
#     glClear,
#     glBegin,
#     glColor3f,
#     glVertex2f,
#     glEnd
# )


# class MyGLWidget(QGLWidget):
#     def initializeGL(self):
#         glClearColor(0.1, 0.2, 0.3, 1.0)  # Cor de fundo

#     def resizeGL(self, w, h):
#         glViewport(0, 0, w, h)

#     def paintGL(self):
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # type: ignore
#         glBegin(GL_TRIANGLES)
#         glColor3f(1, 0, 0)
#         glVertex2f(-0.5, -0.5)
#         glColor3f(0, 1, 0)
#         glVertex2f(0.5, -0.5)
#         glColor3f(0, 0, 1)
#         glVertex2f(0.0, 0.5)
#         glEnd()


# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("PyQt5 + OpenGL Example")
#         self.setGeometry(200, 200, 600, 500)

#         # Layout principal (vertical)
#         layout = QVBoxLayout()

#         # Canvas OpenGL
#         self.glWidget = MyGLWidget()
#         layout.addWidget(self.glWidget)

#         # Barra de botões
#         button_layout = QHBoxLayout()

#         self.btn_start = QPushButton("Start")
#         self.btn_start.clicked.connect(self.on_start)

#         self.btn_exit = QPushButton("Exit")
#         self.btn_exit.clicked.connect(self.on_exit)

#         button_layout.addWidget(self.btn_start)
#         button_layout.addWidget(self.btn_exit)

#         layout.addLayout(button_layout)
#         self.setLayout(layout)

#     def on_start(self):
#         print("Start button pressed")
#         self.glWidget.update()  # Redesenha o canvas

#     def on_exit(self):
#         print("Exiting...")
#         self.close()


# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#    main()



import sys
from PyQt5.QtWidgets import QApplication
from .mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()