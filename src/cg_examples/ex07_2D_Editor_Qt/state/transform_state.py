# src/cg_examples/ex07_2D_Editor_Qt/state/transform_state.py
from __future__ import annotations

import logging
import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent

from ..model.circulo import Circulo
from ..model.poligono import Poligono
from ..model.ponto import Ponto
from ..model.transform_ops import (
    angle_from,
    apply_rotation,
    apply_scale,
    apply_translation,
    scale_from_vectors,
)
from ..view.draw_utils import get_world_coords
from ..view.selection_render import compute_selection_center
from .abstract_state import State
from .transform_mode import TransformMode

log = logging.getLogger(__name__)


class TransformState(State):
    """Estado único para translate/scale/rotate, com submodo."""

    def __init__(self, context, mode: TransformMode, handle: dict | None = None) -> None:
        super().__init__(context)
        self.mode: TransformMode = mode  # "translate" | "scale" | "rotate" | "pivot"
        self.handle = handle or {}
        self._curr_mouse: Ponto | None = None
        self._start_mouse: Ponto | None = None
        self._pivot: Ponto | None = None
        self._axis_from_handle: str | None = None  # "x"|"y"|None
        self._backups: list[Circulo | Poligono] = []
        self._committed: bool = False

    # ---------------- lifecycle ----------------
    def on_enter(self) -> None:
        gv = self.context.global_vars
        sel = gv.selected

        if not sel:
            log.info("TransformState: nada selecionado; voltando ao idle.")
            self.context.current_state = self.context.idle_state
            return

        # 1) pivot: use gv.pivot se existir, senão centro da seleção
        self._pivot = getattr(gv, "pivot", None) or compute_selection_center(sel)
        if self._pivot is None:
            self.context.current_state = self.context.idle_state
            return

        # 2) backups para permitir cancelamento
        self._backups = self._make_backups(sel)

        # 3) eixo para SCALE via aresta (edge)
        self._axis_from_handle = None
        if self.mode is TransformMode.SCALE and self.handle.get("kind") == "edge":
            idx = int(self.handle.get("index", -1)) % 4
            # convencione: 0=bottom(y), 1=right(x), 2=top(y), 3=left(x)
            self._axis_from_handle = "y" if idx in (0, 2) else "x"

        if self._pivot is None:
            # nada selecionado: volte ao idle
            self.context.current_state = self.context.idle_state
            return

        # 3) mouse inicial
        self._start_mouse = None
        self._curr_mouse = None
        self._committed = False
        log.info(
            "TransformState iniciado (mode=%s, axis=%s, pivot=(%.2f, %.2f))",
            self.mode.name,
            self._axis_from_handle,
            self._pivot.x,
            self._pivot.y,
        )

    def on_exit(self) -> None:
        # Se não foi commit, restaurar estado original
        if not self._committed:
            self._restore_backups(self.context.global_vars.selected, self._backups)
            self.context.canvas.update()
        log.info("TransformState finalizado (commit=%s)", self._committed)

    def mouse_press_event(self, event: QMouseEvent) -> None:
        # self._start_mouse = get_world_coords(self.context, event.x(), event.y())
        if event.button() == Qt.MouseButton.LeftButton:
            xw, yw = get_world_coords(self.context, event.x(), event.y())
            log.debug("press@world: (%.2f, %.2f)", xw, yw)
            self._start_mouse = Ponto(xw, yw)
            self._curr_mouse = Ponto(xw, yw)

    def _on_translate_move(self, event: QMouseEvent) -> None:
        if self._start_mouse is None or self._curr_mouse is None:
            return
        gv = self.context.global_vars
        dx = self._curr_mouse.x - self._start_mouse.x
        dy = self._curr_mouse.y - self._start_mouse.y
        log.debug(
            "translate dx=%.3f dy=%.3f (start=(%.2f,%.2f) curr=(%.2f,%.2f))",
            dx,
            dy,
            self._start_mouse.x,
            self._start_mouse.y,
            self._curr_mouse.x,
            self._curr_mouse.y,
        )

        if self._shift_pressed(event):
            # restringe ao eixo dominante
            if abs(dx) > abs(dy):
                dy = 0.0
            else:
                dx = 0.0

        apply_translation(gv.selected, dx, dy)
        # ⚠️ Atualiza o ponto de referência para evitar acúmulo de deslocamento
        self._start_mouse = Ponto(self._curr_mouse.x, self._curr_mouse.y)

    def _on_scale_move(self, event: QMouseEvent) -> None:
        if self._pivot is None or self._start_mouse is None or self._curr_mouse is None:
            log.warning("TransformState.scale: pivot indefinido, operação ignorada.")
            return

        axis = self._axis_from_handle  # None => uniforme (corner)
        sx, sy = scale_from_vectors(self._pivot, self._start_mouse, self._curr_mouse, axis)

        if self._shift_pressed(event):
            # força escala uniforme
            s = (sx * sy) ** 0.5
            sx = sy = s

        gv = self.context.global_vars
        apply_scale(gv.selected, sx, sy, self._pivot)

    def _on_rotate_move(self, event: QMouseEvent) -> None:
        if self._pivot is None or self._start_mouse is None or self._curr_mouse is None:
            log.warning("TransformState.rotate: pivot indefinido, operação ignorada.")
            return

        ang = angle_from(self._pivot, self._start_mouse, self._curr_mouse)

        if self._shift_pressed(event):
            step = getattr(self.context.global_vars, "snap_angle_deg", 15)
            ang = round(ang / math.radians(step)) * math.radians(step)

        gv = self.context.global_vars
        apply_rotation(gv.selected, ang, self._pivot)

    def mouse_move_event(self, event: QMouseEvent) -> None:
        if self._start_mouse is None:
            return
        x, y = get_world_coords(self.context, event.x(), event.y())
        log.debug("move@world: (%.2f, %.2f) mode=%s", x, y, self.mode)
        self._curr_mouse = Ponto(x, y)

        if self.mode is TransformMode.TRANSLATE:
            self._on_translate_move(event)
        elif self.mode is TransformMode.SCALE:
            self._on_scale_move(event)
        elif self.mode is TransformMode.ROTATE:
            self._on_rotate_move(event)

        self.context.canvas.update()

    def mouse_release_event(self, event: QMouseEvent) -> None:
        # botão esquerdo: commit
        if event.button() == Qt.MouseButton.LeftButton:
            self._committed = True
            self.context.current_state = self.context.idle_state
        # botão direito: cancelar
        elif event.button() == Qt.MouseButton.RightButton:
            self._committed = False
            self.context.current_state = self.context.idle_state

    def key_press_event(self, event: QKeyEvent) -> None:
        k = event.key()

        # Enter/Return => commit
        if k in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._committed = True
            self.context.current_state = self.context.idle_state
        # ESC => cancel
        elif k == Qt.Key.Key_Escape:
            self._committed = False
            self.context.current_state = self.context.idle_state

    def mouse_double_click_event(self, event: QMouseEvent) -> None:
        """Finaliza a transformação com duplo clique do botão esquerdo."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._committed = True
            self.context.clear_selection()
            self.context.current_state = self.context.idle_state
            log.info("TransformState: operação confirmada por duplo clique.")

    # overlay opcional (guias)
    def display_overlay(self) -> None:
        # se quiser, desenhe guias aqui no futuro (linha pivô->mouse, bbox fantasma etc.)
        pass

    # ---------------- helpers: backup/restore ----------------
    def _make_backups(self, objs):
        """Cria cópias profundas dos objetos selecionados antes da transformação."""
        backups: list[Circulo | Poligono] = []
        for o in objs:
            if isinstance(o, Circulo):
                backups.append(Circulo(o.xc, o.yc, o.raio))
            elif isinstance(o, Poligono):
                copia = Poligono()
                copia.pontos = [Ponto(p.x, p.y) for p in o.pontos]
                backups.append(copia)
            else:
                # opcional: emitir um log se tipo não for tratado
                log.warning("Tipo de objeto não suportado em _make_backups: %s", type(o).__name__)
        return backups

    def _restore_backups(self, objs, backups):
        """Restaura o estado original dos objetos a partir dos backups.
        Supõe a mesma ordem de `objs` em relação a `backups`.
        """
        if len(objs) != len(backups):
            log.warning(
                "restore_backups: tamanhos diferentes (objs=%d, backups=%d); "
                "tentando restaurar por zip.",
                len(objs),
                len(backups),
            )
        for o, b in zip(objs, backups, strict=False):
            if isinstance(o, Circulo) and isinstance(b, Circulo):
                o.xc, o.yc, o.raio = b.xc, b.yc, b.raio
            elif isinstance(o, Poligono) and isinstance(b, Poligono):
                o.pontos = [Ponto(p.x, p.y) for p in b.pontos]
            else:
                log.warning("Backup incompatível ou tipo não suportado: %s", type(o).__name__)

    def _shift_pressed(self, event: QMouseEvent) -> bool:
        # Compatível com PyQt5
        return bool(event.modifiers() & int(Qt.KeyboardModifier.ShiftModifier))
