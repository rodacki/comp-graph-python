"""Canvas OpenGL do ex08.

Este módulo implementa o widget central da aplicação (`QOpenGLWidget`) e
expõe um ciclo didático completo de renderização em OpenGL moderno:

1. `initializeGL`: cria recursos de GPU (via renderer) e define estado inicial;
2. `resizeGL`: atualiza viewport;
3. `paintGL`: desenha segmentos confirmados + preview temporário.

Também concentra a ponte entre eventos Qt (mouse/teclado) e a máquina de
estados (`Context`).
"""

from OpenGL.GL import GL_COLOR_BUFFER_BIT, glClear, glClearColor, glViewport
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QOpenGLWidget

from ..model.segmento import Segmento
from ..state.context import Context
from .renderer import SegmentRenderer


class GLCanvas(QOpenGLWidget):
    """Widget OpenGL minimalista para edição 2D por cliques.

    O canvas não armazena a cena por conta própria; ele consulta o modelo
    através de `self._context.global_vars` em cada frame.
    """

    def __init__(self, context: Context, parent=None) -> None:
        """Inicializa canvas e associa contexto de estado.

        Args:
            context: Contexto com estado de interação e modelo.
            parent: Widget pai Qt (opcional).

        Returns:
            None: Configura instância do canvas.

        Notes:
            - `StrongFocus` permite capturar a tecla `Esc` no próprio canvas.
            - `setMouseTracking(True)` habilita preview mesmo sem botão pressionado.
        """
        super().__init__(parent)
        self._context = context
        self._renderer = SegmentRenderer()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

    def initializeGL(self) -> None:
        """Configura recursos OpenGL e cor de fundo inicial.

        Returns:
            None: Inicializa renderer com shaders/VAO/VBO.

        Notes:
            Qt garante contexto OpenGL corrente durante esta chamada.
        """
        clear = self._context.global_vars.clear_color
        glClearColor(clear[0], clear[1], clear[2], clear[3])
        self._renderer.initialize()

    def resizeGL(self, w: int, h: int) -> None:
        """Atualiza viewport quando o widget é redimensionado.

        Args:
            w: Nova largura em pixels.
            h: Nova altura em pixels.

        Returns:
            None: Ajusta viewport OpenGL para novo tamanho.
        """
        glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        """Desenha frame atual da aplicação.

        Returns:
            None: Emite draw calls para segmentos confirmados e preview.

        Side Effects:
            Consome estado global (`ponto_pendente`/`ponto_cursor`) para decidir
            se deve renderizar segmento temporário de preview.
        """
        glClear(GL_COLOR_BUFFER_BIT)

        g = self._context.global_vars

        # Segmentos já confirmados no modelo: estilo sólido.
        self._renderer.draw(g.modelo.segmentos, g.line_color, g.line_width, dashed=False)

        # Preview temporário: estilo verde tracejado.
        if g.ponto_pendente is not None and g.ponto_cursor is not None:
            preview = Segmento(g.ponto_pendente, g.ponto_cursor)
            self._renderer.draw([preview], g.preview_color, g.line_width, dashed=True)

    def mousePressEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha clique para contexto e solicita repaint.

        Args:
            event: Evento de clique do mouse.

        Returns:
            None: Atualiza cena após possível alteração de dados.

        Side Effects:
            Pode inserir novo segmento no modelo (quando segundo ponto é clicado).
        """
        self._context.mouse_press_event(event)
        self.update()

    def keyPressEvent(
        self, event: QKeyEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha teclado para contexto e solicita repaint.

        Args:
            event: Evento de tecla pressionada.

        Returns:
            None: Permite ações de teclado como encerramento com Esc.
        """
        self._context.key_press_event(event)
        self.update()

    def mouseMoveEvent(
        self, event: QMouseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Encaminha movimento do mouse para atualização de preview.

        Args:
            event: Evento de movimento do mouse.

        Returns:
            None: Atualiza estado e repinta canvas.

        Side Effects:
            Pode atualizar ponto de cursor usado no preview.
        """
        self._context.mouse_move_event(event)
        self.update()

    def to_ndc(self, x_px: int, y_px: int) -> tuple[float, float]:
        """Converte coordenadas do widget para NDC.

        Args:
            x_px: Coordenada X em pixels do widget (origem no canto superior esquerdo).
            y_px: Coordenada Y em pixels do widget (origem no canto superior esquerdo).

        Returns:
            tuple[float, float]: Coordenadas `(x, y)` no espaço NDC [-1, 1].

        Notes:
            O eixo Y do Qt cresce para baixo; em NDC cresce para cima.
            Por isso há a inversão em `y_ndc`.
        """
        w = max(1, self.width())
        h = max(1, self.height())

        x_ndc = (2.0 * x_px / w) - 1.0
        y_ndc = 1.0 - (2.0 * y_px / h)
        return float(x_ndc), float(y_ndc)

    def closeEvent(
        self, event: QCloseEvent
    ) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Libera recursos OpenGL ao fechar widget.

        Args:
            event: Evento de fechamento do widget.

        Returns:
            None: Garante descarte do renderer antes de fechar.

        Notes:
            `makeCurrent()/doneCurrent()` garantem contexto válido para desalocar
            recursos de GPU com segurança.
        """
        self.makeCurrent()
        self._renderer.dispose()
        self.doneCurrent()
        super().closeEvent(event)
