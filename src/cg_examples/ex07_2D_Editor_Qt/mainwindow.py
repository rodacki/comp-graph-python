# pyright: reportIncompatibleMethodOverride=false

import qtawesome as qta
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from .globals.settings import GlobalDefinitions
from .state.context import Context
from .view.glcanvas import GLCanvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Editor 2D - PyQt + OpenGL")
        self.setGeometry(200, 200, 800, 800)
        self._cross_cursor = QCursor(Qt.CursorShape.CrossCursor)

        # Variáveis globais e contexto de estados
        self.global_vars = GlobalDefinitions()
        self.state_context = Context(self.global_vars)

        # Layout principal
        layout = QVBoxLayout()

        # Canvas OpenGL
        self.canvas = GLCanvas(self.state_context)
        self.state_context.canvas = self.canvas  # referência cruzada
        layout.addWidget(self.canvas)

        # Barra de botões
        button_layout = QHBoxLayout()

        self.btn_circle = QPushButton()
        self.btn_circle.setIcon(qta.icon("fa6.circle", color="gray"))
        self.btn_circle.setIconSize(QSize(32, 32))

        # self.btn_idle = QPushButton("Idle")

        self.btn_init_poligono = QPushButton()
        self.btn_init_poligono.setIcon(qta.icon("fa6s.draw-polygon", color="gray"))
        self.btn_init_poligono.setIconSize(QSize(32, 32))

        # self.btn_end_poligono = QPushButton("End Pol")
        self.btn_exit = QPushButton()
        self.btn_exit.setIcon(qta.icon("fa6s.right-from-bracket", color="gray"))
        self.btn_exit.setIconSize(QSize(32, 32))

        # Ligações de eventos
        # self.btn_idle.clicked.connect(self.on_idle)
        self.btn_circle.clicked.connect(self.on_start_circle)
        self.btn_init_poligono.clicked.connect(self.on_start_polygon)
        # self.btn_end_poligono.clicked.connect(self.on_stop_polygon)
        self.btn_exit.clicked.connect(self.on_exit)

        # button_layout.addWidget(self.btn_idle)
        button_layout.addWidget(self.btn_circle)
        button_layout.addWidget(self.btn_init_poligono)
        # button_layout.addWidget(self.btn_end_poligono)
        button_layout.addWidget(self.btn_exit)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Timer para repintura contínua (~60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.canvas.update)
        self.timer.start(16)

    # ------------------------------------------------ #
    # Ações dos botões
    # ------------------------------------------------ #

    def on_start_circle(self):
        self.state_context.current_state = self.state_context.draw_circle_state
        print("🟢 Estado: Iniciar círculo")

    def on_start_polygon(self):
        self.state_context.current_state = self.state_context.draw_polygon_state
        print("🟢 Estado: Iniciar poligono")

    def on_exit(self):
        print("Saindo...")
        self.close()
