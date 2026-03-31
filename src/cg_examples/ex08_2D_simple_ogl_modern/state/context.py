"""Contexto da máquina de estados do ex08."""

from dataclasses import dataclass, field

from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..globals.settings import GlobalDefinitions
from .abstract_state import State
from .idle_state import IdleState


@dataclass
class Context:
    """Gerencia estado corrente e delega eventos para ele.

    Attributes:
        global_vars: Estado global compartilhado da aplicação.
        canvas: Referência opcional ao widget OpenGL.
    """

    global_vars: GlobalDefinitions
    canvas: object | None = None
    idle_state: IdleState = field(init=False)
    _current_state: State = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Cria estado idle como estado inicial.

        Returns:
            None: Inicializa a máquina de estados.
        """
        self.idle_state = IdleState(self)
        self._current_state = self.idle_state

    @property
    def current_state(self) -> State:
        """Retorna estado corrente.

        Returns:
            State: Estado atualmente ativo.
        """
        return self._current_state

    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Delega clique de mouse para o estado corrente.

        Args:
            event: Evento de mouse.

        Returns:
            None: Encaminha a lógica para o estado ativo.
        """
        self._current_state.mouse_press_event(event)

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Delega movimento de mouse para o estado corrente.

        Args:
            event: Evento de movimento de mouse.

        Returns:
            None: Encaminha a lógica para o estado ativo.
        """
        self._current_state.mouse_move_event(event)

    def key_press_event(self, event: QKeyEvent) -> None:
        """Delega teclado para o estado corrente.

        Args:
            event: Evento de teclado.

        Returns:
            None: Encaminha a lógica para o estado ativo.
        """
        self._current_state.key_press_event(event)
