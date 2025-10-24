from __future__ import annotations

from PyQt5.QtGui import QKeyEvent, QMouseEvent


# state class
class State:
    """Base dos estados: expõe apenas ganchos de eventos Qt e ciclo de vida.
    Todos são no-op por padrão; cada estado implementa só o que precisa.
    """

    def __init__(self, context) -> None:
        self._context = context

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, newcontext):
        self._context = newcontext

    # --- ciclo de vida do estado (opcionais) ---
    def on_enter(self) -> None:
        """Chamado quando o estado passa a ser o corrente."""
        pass

    def on_exit(self) -> None:
        """Chamado quando o estado deixa de ser o corrente."""
        pass

    # --- eventos de mouse (Qt) ---
    def mouse_press_event(self, event: QMouseEvent) -> None:
        pass

    def mouse_move_event(self, event: QMouseEvent) -> None:
        pass

    def mouse_release_event(self, event: QMouseEvent) -> None:
        pass

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        pass

    def key_press_event(self, event: QKeyEvent) -> None:
        pass

    # --- overlay opcional (ex.: “borrachinha” do círculo, segmento-guia do polígono) ---
    def display_overlay(self) -> None:
        pass
