"""Classe base para estados de interação do ex08."""

from typing import Any

from PyQt5.QtGui import QKeyEvent, QMouseEvent


class State:
    """Estado base com callbacks de eventos Qt.

    Todas as funções são no-op por padrão e podem ser sobrescritas.
    """

    def __init__(self, context: Any) -> None:
        """Inicializa estado com referência ao contexto.

        Args:
            context: Contexto compartilhado da aplicação.

        Returns:
            None: Apenas armazena a referência.
        """
        self._context = context

    @property
    def context(self) -> Any:
        """Retorna o contexto associado ao estado.

        Returns:
            Any: Contexto da aplicação.
        """
        return self._context

    def mouse_press_event(self, event: QMouseEvent) -> None:
        """Callback para clique do mouse.

        Args:
            event: Evento de mouse recebido pelo canvas.

        Returns:
            None: Implementação padrão não executa ação.
        """

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Callback para movimento do mouse.

        Args:
            event: Evento de movimento recebido pelo canvas.

        Returns:
            None: Implementação padrão não executa ação.
        """

    def key_press_event(self, event: QKeyEvent) -> None:
        """Callback para tecla pressionada.

        Args:
            event: Evento de teclado recebido pelo canvas.

        Returns:
            None: Implementação padrão não executa ação.
        """
