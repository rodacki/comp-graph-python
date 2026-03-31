"""Renderer OpenGL moderno para desenhar segmentos 2D.

Este módulo centraliza a parte "GPU" da aplicação e separa responsabilidades:

- **Estado de GPU**: programa de shader, VAO, VBO e uniforms;
- **Conversão de dados**: lista de segmentos -> array linear `float32`;
- **Desenho**: upload dos vértices e chamada `glDrawArrays(GL_LINES)`.

Didaticamente, ele mostra o fluxo mínimo de OpenGL moderno para 2D sem usar
matrizes de projeção (os dados já chegam em NDC).
"""

from __future__ import annotations

import ctypes

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_DYNAMIC_DRAW,
    GL_FALSE,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_LINES,
    GL_VERTEX_SHADER,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glDeleteBuffers,
    glDeleteProgram,
    glDeleteVertexArrays,
    glDrawArrays,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glGetUniformLocation,
    glLineWidth,
    glUniform1f,
    glUniform1i,
    glUniform3f,
    glUseProgram,
    glVertexAttribPointer,
)
from OpenGL.GL.shaders import compileProgram, compileShader

from ..model.segmento import Segmento
from .shaders import FRAGMENT_SHADER_SOURCE, VERTEX_SHADER_SOURCE


class SegmentRenderer:
    """Renderiza uma lista de segmentos usando OpenGL moderno.

    Attributes:
        _program: ID do programa de shader linkado.
        _vao: Vertex Array Object com layout dos atributos.
        _vbo: Vertex Buffer Object com dados de vértices.
        _u_color_loc: Local do uniform `u_color` no shader.
        _u_use_dashed_loc: Local do uniform que liga/desliga traçado.
        _u_dash_length_loc: Local do uniform com tamanho do traço.
        _u_gap_length_loc: Local do uniform com tamanho do espaço.
    """

    def __init__(self) -> None:
        """Inicializa ids de recursos OpenGL.

        Returns:
            None: Recursos reais são criados em `initialize`.
        """
        self._program: int = 0
        self._vao: int = 0
        self._vbo: int = 0
        self._u_color_loc: int = -1
        self._u_use_dashed_loc: int = -1
        self._u_dash_length_loc: int = -1
        self._u_gap_length_loc: int = -1

    def initialize(self) -> None:
        """Cria shaders, programa e buffers (VAO/VBO).

        Returns:
            None: Deixa o renderer pronto para receber dados e desenhar.

        Notes:
            Este método deve ser chamado com contexto OpenGL corrente
            (no ex08 isso ocorre dentro de `QOpenGLWidget.initializeGL`).
        """
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
        # Em QOpenGLWidget (especialmente no macOS), a validação explícita do
        # programa pode falhar no initializeGL por estado de framebuffer.
        # O link já garante consistência dos shaders para este exemplo.
        self._program = compileProgram(vertex_shader, fragment_shader, validate=False)

        self._vao = glGenVertexArrays(1)
        self._vbo = glGenBuffers(1)

        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)

        # Reserva inicial mínima; o conteúdo real é enviado a cada draw.
        glBufferData(GL_ARRAY_BUFFER, 0, None, GL_DYNAMIC_DRAW)

        # Layout(location=0) recebe 2 floats por vértice (x, y).
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self._u_color_loc = glGetUniformLocation(self._program, "u_color")
        self._u_use_dashed_loc = glGetUniformLocation(self._program, "u_use_dashed")
        self._u_dash_length_loc = glGetUniformLocation(self._program, "u_dash_length")
        self._u_gap_length_loc = glGetUniformLocation(self._program, "u_gap_length")

    def draw(
        self,
        segmentos: list[Segmento],
        color: tuple[float, float, float],
        line_width: float,
        dashed: bool = False,
    ) -> None:
        """Desenha todos os segmentos informados.

        Args:
            segmentos: Lista de segmentos do modelo.
            color: Cor RGB aplicada uniformemente às linhas.
            line_width: Espessura de linha em pixels.
            dashed: Quando `True`, aplica padrão tracejado no fragment shader.

        Returns:
            None: Atualiza VBO e emite draw call para GL_LINES.

        Notes:
            Em muitos drivers core profile no macOS, `glLineWidth` suporta
            apenas `1.0`. Por isso a chamada força esse valor para estabilidade.
        """
        if not segmentos:
            return

        vertices = self._segments_to_numpy(segmentos)

        glUseProgram(self._program)
        if self._u_color_loc >= 0:
            glUniform3f(self._u_color_loc, color[0], color[1], color[2])
        if self._u_use_dashed_loc >= 0:
            glUniform1i(self._u_use_dashed_loc, 1 if dashed else 0)
        if self._u_dash_length_loc >= 0:
            glUniform1f(self._u_dash_length_loc, 8.0)
        if self._u_gap_length_loc >= 0:
            glUniform1f(self._u_gap_length_loc, 6.0)

        # Em muitos drivers core profile (ex.: macOS), apenas largura 1.0 é suportada.
        glLineWidth(1.0)
        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)

        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
        glDrawArrays(GL_LINES, 0, vertices.size // 2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        glUseProgram(0)

    def dispose(self) -> None:
        """Libera recursos OpenGL alocados pelo renderer.

        Returns:
            None: Deleta VBO, VAO e programa quando existentes.

        Notes:
            Deve ser chamado com contexto OpenGL corrente.
        """
        if self._vbo:
            glDeleteBuffers(1, [self._vbo])
            self._vbo = 0
        if self._vao:
            glDeleteVertexArrays(1, [self._vao])
            self._vao = 0
        if self._program:
            glDeleteProgram(self._program)
            self._program = 0

    def _segments_to_numpy(self, segmentos: list[Segmento]) -> np.ndarray:
        """Converte lista de segmentos em array linear de vértices float32.

        Args:
            segmentos: Segmentos a converter.

        Returns:
            np.ndarray: Vetor `[x1,y1,x2,y2,...]` no formato `float32`.

        Notes:
            Cada segmento gera 4 floats (2 vértices com 2 coordenadas cada).
        """
        data: list[float] = []
        for s in segmentos:
            data.extend([s.p1.x, s.p1.y, s.p2.x, s.p2.y])
        return np.array(data, dtype=np.float32)
