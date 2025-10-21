from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glClear,
    glClearColor,
    glLoadIdentity,
    glBegin,
    glEnd,
    glVertex2f,
    glColor3f,
    glViewport,
    GL_LINES,
)
from .draw_utils import axis
from ..state.context import Context

class GLCanvas(QGLWidget):
    def __init__(self, state_context: Context, parent=None):
        super().__init__(parent)
        self.state_context = state_context
        self.setMouseTracking(True)

    def initializeGL(self):
        from ..view.draw_utils import init
        glClearColor(0.2, 0.3, 0.4, 1.0)
        init(self.state_context)  # ← importante

    def resizeGL(self, w, h):
        # Corrige para monitores HiDPI (Retina)
        ratio = self.devicePixelRatioF()
        pixel_w = int(w * ratio)
        pixel_h = int(h * ratio)

        glViewport(0, 0, pixel_w, pixel_h)

        gv = self.state_context.global_vars

        gv.w = pixel_w
        gv.h = pixel_h

        # --- cálculo do tamanho do handler em coordenadas do mundo ---
        from ..view.draw_utils import px_to_world
        gv.handle_size_world = px_to_world(self.state_context, gv.handle_size_px ,"avg")
        print(f"[resizeGL] Logical: ({w}, {h})  Physical: ({pixel_w}, {pixel_h})  ratio={ratio:.2f}")

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # type: ignore
        glLoadIdentity()
        axis(self.state_context)
        self.state_context.display()
        #self.swapBuffers()
        
    # def draw_axes(self):
    #     """Desenha os eixos X e Y"""
    #     glColor3f(0.8, 0.8, 0.8)
    #     glBegin(GL_LINES)
    #     glVertex2f(-1, 0)
    #     glVertex2f(1, 0)
    #     glVertex2f(0, -1)
    #     glVertex2f(0, 1)
        # glEnd()

    # Eventos do mouse — delegados para o contexto
    def mousePressEvent(self, event: QMouseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        self.state_context.mousePressEvent(event)
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        self.state_context.mouseMoveEvent(event)
        self.update()

    def keyPressEvent(self, event: QKeyEvent) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        key = event.text().encode()
        self.state_context.keyboard(key, 0, 0)
        self.update()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None: # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha o duplo clique ao estado atual."""
        print("GLCanvas recebeu duplo clique")  # para debug
        if hasattr(self.state_context.currentState, "mouseDoubleClickEvent"):
            self.state_context.currentState.mouseDoubleClickEvent(event)
        self.update()