"""Estado padrão de edição do ex08.

Neste estado:
- cada clique esquerdo define um ponto em NDC;
- a cada par de pontos, um segmento é criado e armazenado no modelo;
- tecla Esc encerra a aplicação.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtWidgets import QApplication

from ..model.ponto import Ponto
from ..model.segmento import Segmento
from .abstract_state import State


class IdleState(State):
    """Estado único para inserção de segmentos por pares de cliques."""

    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Processa clique esquerdo para montar segmentos de reta.

        Args:
            event: Evento de clique de mouse recebido do canvas.

        Returns:
            None: Atualiza ponto pendente e modelo de segmentos.
        """
        if event.button() != Qt.MouseButton.LeftButton:
            return

        canvas = self.context.canvas
        if canvas is None:
            return

        x_ndc, y_ndc = canvas.to_ndc(event.x(), event.y())
        point = Ponto(x_ndc, y_ndc)
        g = self.context.global_vars

        if g.ponto_pendente is None:
            g.ponto_pendente = point
            g.ponto_cursor = point
            return

        segmento = Segmento(g.ponto_pendente, point)
        g.modelo.add_segmento(segmento)
        g.ponto_pendente = None
        g.ponto_cursor = None

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Atualiza ponto do cursor para preview de segmento.

        Args:
            event: Evento de movimento do mouse.

        Returns:
            None: Mantém `ponto_cursor` sincronizado quando há ponto pendente.
        """
        canvas = self.context.canvas
        if canvas is None:
            return

        g = self.context.global_vars
        if g.ponto_pendente is None:
            g.ponto_cursor = None
            return

        x_ndc, y_ndc = canvas.to_ndc(event.x(), event.y())
        g.ponto_cursor = Ponto(x_ndc, y_ndc)

    def key_press_event(self, event: QKeyEvent) -> None:
        """Encerra aplicação quando o usuário pressiona Esc.

        Args:
            event: Evento de tecla pressionada.

        Returns:
            None: Solicita encerramento da aplicação Qt.
        """
        if event.key() == Qt.Key.Key_Escape:
            app = QApplication.instance()
            if app is not None:
                app.quit()
