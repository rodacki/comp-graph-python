"""Renderer OpenGL moderno para desenhar um triangulo equilatero em linhas."""

from __future__ import annotations

import ctypes

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_LINE_LOOP,
    GL_STATIC_DRAW,
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
    glUniform3f,
    glUseProgram,
    glVertexAttribPointer,
)
from OpenGL.GL.shaders import compileProgram, compileShader

from .shaders import FRAGMENT_SHADER_SOURCE, VERTEX_SHADER_SOURCE


class TriangleRenderer:
    """Renderiza triangulo equilatero estatico com pipeline moderno."""

    def __init__(self) -> None:
        self._program: int = 0
        self._vao: int = 0
        self._vbo: int = 0
        self._u_color_loc: int = -1

    def initialize(self) -> None:
        """Cria programa de shaders e configura VAO/VBO."""
        vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
        fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
        self._program = compileProgram(vertex_shader, fragment_shader, validate=False)

        self._vao = glGenVertexArrays(1)
        self._vbo = glGenBuffers(1)

        vertices = np.array(
            [
                0.0,
                0.6,
                -0.51961524,
                -0.3,
                0.51961524,
                -0.3,
            ],
            dtype=np.float32,
        )

        glBindVertexArray(self._vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * 4, ctypes.c_void_p(0))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        self._u_color_loc = glGetUniformLocation(self._program, "u_color")

    def draw(self) -> None:
        """Desenha triangulo estatico usando GL_LINE_LOOP."""
        glUseProgram(self._program)
        if self._u_color_loc >= 0:
            glUniform3f(self._u_color_loc, 0.95, 0.95, 0.95)

        glBindVertexArray(self._vao)
        glDrawArrays(GL_LINE_LOOP, 0, 3)
        glBindVertexArray(0)
        glUseProgram(0)

    def dispose(self) -> None:
        """Libera recursos OpenGL do renderer."""
        if self._vbo:
            glDeleteBuffers(1, [self._vbo])
            self._vbo = 0
        if self._vao:
            glDeleteVertexArrays(1, [self._vao])
            self._vao = 0
        if self._program:
            glDeleteProgram(self._program)
            self._program = 0
