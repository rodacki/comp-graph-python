from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from PyQt5.QtGui import QMouseEvent, QKeyEvent

from ..globals.settings import GlobalDefinitions
from .abstractState import State
from .idleState import IdleState
from .drawCircleState import DrawCircleState
from .drawPolygonState import DrawPolygonState


# ----------------------------------------------------- #
#  Classe contexto do padrão de projetos State          #
# ----------------------------------------------------- #
@dataclass
class Context:
    """Gerencia o estado atual e as transições do editor 2D."""
    global_vars: GlobalDefinitions
    canvas: Optional[object] = None

    # estados (definidos no pós-init)
    idleState: IdleState = field(init=False)
    drawCircleState: DrawCircleState = field(init=False)
    drawPolygonState: DrawPolygonState = field(init=False)
    
    # Estado atual (privado, com property)
    _current_state: State = field(init=False, repr=False)

    def __post_init__(self):
            """Inicializa os estados dependentes deste contexto."""
            self.idleState = IdleState(self)
            self.drawCircleState = DrawCircleState(self)
            self.drawPolygonState = DrawPolygonState(self)
            self._current_state = self.idleState  # estado inicial
            self._current_state.on_enter()
    
    # ---------------------------
    # Troca de estado com hooks
    # ---------------------------
    @property
    def currentState(self) -> State:
        return self._current_state

    @currentState.setter
    def currentState(self, new_state: State) -> None:
        if new_state is self._current_state:
            return
        if self._current_state is not None:
            self._current_state.on_exit()
        self._current_state = new_state
        if self._current_state is not None:
            self._current_state.on_enter()
        # redraw quando troca de estado
        if self.canvas is not None:
            self.canvas.update()


    # ---------------------------------------------------------------- #
    #    Acoes (callbacks) a serem implementadas em cada estado da app #
    # ---------------------------------------------------------------- #
    # ---------------------------
    # Delegação de eventos (Qt)
    # ---------------------------
    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._current_state.mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self._current_state.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._current_state.mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self._current_state.mouseDoubleClickEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self._current_state.keyPressEvent(event)

    def display(self) -> None:
        """Render centralizado no GLCanvas; nada a fazer aqui."""
        pass

    # ---------------------------
    # Seleção de objetos
    # ---------------------------
    def clear_selection(self):
        for obj in self.global_vars.selected:
            obj.selected = False
        self.global_vars.selected.clear()

    def select_object(self, obj, additive: bool = False):
        if not additive:
            self.clear_selection()
        if obj not in self.global_vars.selected:
            obj.selected = True
            self.global_vars.selected.append(obj)

    def toggle_object(self, obj):
        if obj in self.global_vars.selected:
            obj.selected = False
            self.global_vars.selected.remove(obj)
        else:
            obj.selected = True
            self.global_vars.selected.append(obj)

    def set_state(self, new_state):
        if self.currentState is not None:
            self.currentState.on_exit()
        self.currentState = new_state
        self.currentState.on_enter()
        if self.canvas:
            self.canvas.update()
