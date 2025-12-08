import OpenGL.GL as GL

from .buffer_object import VertexBuffer
from .shader_program import ShaderProgram
from .vao_manager import SimpleVAO


class Renderer2D:
    def __init__(self, vert_src: str, frag_src: str):
        self.shader = ShaderProgram(vert_src, frag_src)

    def draw_polygon(self, poly, color, viewproj):
        vbo = VertexBuffer()
        vbo.upload([(p.x, p.y) for p in poly.pontos])

        vao = SimpleVAO()
        vao.setup(vbo)

        self.shader.use()
        GL.glUniformMatrix4fv(self.shader.uniform_location("u_viewproj"), 1, GL.GL_FALSE, viewproj)
        GL.glUniform3f(self.shader.uniform_location("u_color"), *color)

        vao.bind()
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, vbo.count)

    def draw_circle(self, circle, color, viewproj):
        # discretizar circumferência
        import math

        n = 64
        pts = [
            (
                circle.xc + circle.raio * math.cos(2 * math.pi * i / n),
                circle.yc + circle.raio * math.sin(2 * math.pi * i / n),
            )
            for i in range(n)
        ]

        vbo = VertexBuffer()
        vbo.upload(pts)

        vao = SimpleVAO()
        vao.setup(vbo)

        self.shader.use()
        GL.glUniformMatrix4fv(self.shader.uniform_location("u_viewproj"), 1, GL.GL_FALSE, viewproj)
        GL.glUniform3f(self.shader.uniform_location("u_color"), *color)

        vao.bind()
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, vbo.count)
