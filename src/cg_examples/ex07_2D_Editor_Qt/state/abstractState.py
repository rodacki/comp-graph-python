from __future__ import annotations
from abc import ABC
from typing import Optional
from PyQt5.QtGui import QMouseEvent, QKeyEvent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..state.context import Context  # só para type hints, não roda em runtime


# abstract state class
class State(ABC):
    """Base dos estados: expõe apenas ganchos de eventos Qt e ciclo de vida.
    Todos são no-op por padrão; cada estado implementa só o que precisa.
    """
    def __init__(self, context: Context) -> None:
        self._context = context

    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, newcontext: Context):
        self._context = newcontext

    # --- ciclo de vida do estado (opcionais) ---
    def on_enter(self) -> None:
        """Chamado quando o estado passa a ser o corrente."""
        pass

    def on_exit(self) -> None:
        """Chamado quando o estado deixa de ser o corrente."""
        pass

    # --- eventos de mouse (Qt) ---
    def mousePressEvent(self, event: QMouseEvent) -> None: pass
    def mouseMoveEvent(self, event: QMouseEvent) -> None: pass
    def mouseReleaseEvent(self, event: QMouseEvent) -> None: pass
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None: pass
    def keyPressEvent(self, event: QKeyEvent) -> None: pass

    # --- overlay opcional (ex.: “borrachinha” do círculo, segmento-guia do polígono) ---
    def display_overlay(self) -> None: pass