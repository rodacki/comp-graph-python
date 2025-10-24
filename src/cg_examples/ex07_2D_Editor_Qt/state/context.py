from __future__ import annotations

from dataclasses import dataclass, field

from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..globals.settings import GlobalDefinitions
from .abstract_state import State
from .draw_circle_state import DrawCircleState
from .draw_polygon_state import DrawPolygonState
from .idle_state import IdleState


# ----------------------------------------------------- #
#  Classe contexto do padrão de projetos State          #
# ----------------------------------------------------- #
@dataclass
class Context:
    """Gerencia o estado atual e as transições do editor 2D."""

    global_vars: GlobalDefinitions
    canvas: object | None = None

    # estados (definidos no pós-init)
    idle_state: IdleState = field(init=False)
    draw_circle_state: DrawCircleState = field(init=False)
    draw_polygon_state: DrawPolygonState = field(init=False)

    # Estado atual (privado, com property)
    _current_state: State = field(init=False, repr=False)

    def __post_init__(self):
        """Inicializa os estados dependentes deste contexto."""
        self.idle_state = IdleState(self)
        self.draw_circle_state = DrawCircleState(self)
        self.draw_polygon_state = DrawPolygonState(self)
        self._current_state = self.idle_state  # estado inicial
        self._current_state.on_enter()

    # ---------------------------
    # Troca de estado com hooks
    # ---------------------------
    @property
    def current_state(self) -> State:
        return self._current_state

    @current_state.setter
    def current_state(self, new_state: State) -> None:
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
    def mouse_press_event(self, event: QMouseEvent) -> None:
        self._current_state.mouse_press_event(event)

    def mouse_move_event(self, event: QMouseEvent) -> None:
        self._current_state.mouse_move_event(event)

    def mouse_release_event(self, event: QMouseEvent) -> None:
        self._current_state.mouse_release_event(event)

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        self._current_state.mouse_double_click_event(event)

    def key_press_event(self, event: QKeyEvent) -> None:
        self._current_state.key_press_event(event)

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
        if self.current_state is not None:
            self.current_state.on_exit()
        self.current_state = new_state
        self.current_state.on_enter()
        if self.canvas:
            self.canvas.update()
