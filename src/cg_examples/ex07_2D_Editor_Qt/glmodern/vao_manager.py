import OpenGL.GL as GL


class SimpleVAO:
    def __init__(self):
        self.vao = GL.glGenVertexArrays(1)

    def setup(self, vbo):
        GL.glBindVertexArray(self.vao)
        vbo.bind()

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, None)

    def bind(self):
        GL.glBindVertexArray(self.vao)
