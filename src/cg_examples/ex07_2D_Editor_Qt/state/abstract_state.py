"""Infraestrutura base para os estados da aplicação.

Este módulo define a classe `State`, que centraliza os ganchos de ciclo de vida
e os callbacks de eventos Qt usados pela máquina de estados do editor.
"""

from __future__ import annotations

from typing import Any

from PyQt5.QtGui import QKeyEvent, QMouseEvent


# state class
class State:
    """Base dos estados: expõe apenas ganchos de eventos Qt e ciclo de vida.
    Todos são no-op por padrão; cada estado implementa só o que precisa.
    """

    def __init__(self, context) -> None:
        """Armazena referência ao contexto compartilhado entre estados.

        Args:
            context: Instância de `Context` com acesso ao modelo e à view.

        Returns:
            None: Inicializa o estado base.
        """
        self._context = context

    @property
    def context(self) -> Any:
        """Retorna o contexto associado ao estado.

        Returns:
            Any: Contexto da aplicação (tipado de forma ampla para evitar ciclo).
        """
        return self._context

    @context.setter
    def context(self, newcontext: Any) -> None:
        """Atualiza o contexto associado ao estado.

        Args:
            newcontext: Novo contexto compartilhado.

        Returns:
            None: Apenas substitui a referência interna.
        """
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
        """Hook de pressionamento do mouse.

        Args:
            event: Evento Qt recebido pelo canvas.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass

    def mouse_move_event(self, event: QMouseEvent) -> None:
        """Hook de movimento do mouse.

        Args:
            event: Evento Qt recebido pelo canvas.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass

    def mouse_release_event(self, event: QMouseEvent) -> None:
        """Hook de soltura do mouse.

        Args:
            event: Evento Qt recebido pelo canvas.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        """Hook de duplo clique do mouse.

        Args:
            event: Evento Qt recebido pelo canvas.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass

    def key_press_event(self, event: QKeyEvent) -> None:
        """Hook de tecla pressionada.

        Args:
            event: Evento Qt de teclado.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass

    # --- overlay opcional (ex.: “borrachinha” do círculo, segmento-guia do polígono) ---
    def display_overlay(self) -> None:
        """Hook opcional para desenhar overlays temporários do estado.

        Returns:
            None: Implementação padrão é no-op.
        """
        pass
