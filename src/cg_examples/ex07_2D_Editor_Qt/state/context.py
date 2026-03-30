"""Contexto da máquina de estados do editor 2D.

Este módulo concentra:
- criação e troca dos estados concretos;
- delegação de eventos Qt para o estado corrente;
- operações de seleção compartilhadas entre estados.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..globals.settings import GlobalDefinitions
from .abstract_state import State
from .draw_circle_state import DrawCircleState
from .draw_polygon_state import DrawPolygonState
from .idle_state import IdleState

log = logging.getLogger(__name__)


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

    def __post_init__(self) -> None:
        """Inicializa os estados dependentes deste contexto."""
        self.idle_state = IdleState(self)
        self.draw_circle_state = DrawCircleState(self)
        self.draw_polygon_state = DrawPolygonState(self)
        self._current_state = self.idle_state  # estado inicial
        log.info("Context inicializado (estado=%s)", type(self.current_state).__name__)
        self._current_state.on_enter()

    # ---------------------------
    # Troca de estado com hooks
    # ---------------------------
    @property
    def current_state(self) -> State:
        """Retorna o estado corrente da máquina de estados.

        Returns:
            State: Instância atualmente ativa.
        """
        return self._current_state

    @current_state.setter
    def current_state(self, new_state: State) -> None:
        """Troca o estado corrente executando hooks de saída/entrada.

        Args:
            new_state: Novo estado que passará a receber os eventos.

        Returns:
            None: Atualiza estado interno e dispara repaint do canvas.
        """
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
        """Encaminha clique do mouse para o estado corrente.

        Args:
            event: Evento Qt de mouse.

        Returns:
            None: A ação concreta é definida pelo estado ativo.
        """
        self._current_state.mouse_press_event(event)

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Encaminha movimento do mouse para o estado corrente.

        Args:
            event: Evento Qt de mouse.

        Returns:
            None: A ação concreta é definida pelo estado ativo.
        """
        self._current_state.mouse_move_event(event)

    def mouse_release_event(self, event: QMouseEvent) -> None:
        """Encaminha soltura do mouse para o estado corrente.

        Args:
            event: Evento Qt de mouse.

        Returns:
            None: A ação concreta é definida pelo estado ativo.
        """
        self._current_state.mouse_release_event(event)

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        """Encaminha duplo clique do mouse para o estado corrente.

        Args:
            event: Evento Qt de mouse.

        Returns:
            None: A ação concreta é definida pelo estado ativo.
        """
        self._current_state.mouse_double_click_event(event)

    def key_press_event(self, event: QKeyEvent) -> None:
        """Encaminha tecla pressionada para o estado corrente.

        Args:
            event: Evento Qt de teclado.

        Returns:
            None: A ação concreta é definida pelo estado ativo.
        """
        self._current_state.key_press_event(event)

    def display(self) -> None:
        """Render centralizado no GLCanvas; nada a fazer aqui."""
        pass

    # ---------------------------
    # Seleção de objetos
    # ---------------------------
    def clear_selection(self) -> None:
        """Limpa seleção atual e desmarca os objetos selecionados.

        Returns:
            None: Atualiza flags `selected` dos objetos e lista global de seleção.
        """
        if self.global_vars.selected:
            log.debug("Clear selection: %d objeto(s)", len(self.global_vars.selected))
        for obj in self.global_vars.selected:
            obj.selected = False
        self.global_vars.selected.clear()

    def select_object(self, obj: object, additive: bool = False) -> None:
        """Seleciona um objeto, com opção de seleção aditiva.

        Args:
            obj: Objeto de cena que possui atributo `selected`.
            additive: Quando `True`, mantém seleção prévia; quando `False`, limpa antes.

        Returns:
            None: Atualiza lista global de objetos selecionados.
        """
        if not additive:
            self.clear_selection()
        if obj not in self.global_vars.selected:
            obj.selected = True
            self.global_vars.selected.append(obj)
            log.info("Selecionado: %s", obj)

    def toggle_object(self, obj: object) -> None:
        """Alterna estado de seleção de um objeto.

        Args:
            obj: Objeto de cena que possui atributo `selected`.

        Returns:
            None: Inclui ou remove objeto da lista de seleção.
        """
        if obj in self.global_vars.selected:
            obj.selected = False
            self.global_vars.selected.remove(obj)
            log.info("Desmarcado: %s", obj)
        else:
            obj.selected = True
            self.global_vars.selected.append(obj)
            log.info("Marcado: %s", obj)
