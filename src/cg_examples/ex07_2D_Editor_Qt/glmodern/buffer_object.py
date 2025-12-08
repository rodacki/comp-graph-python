import numpy as np
import OpenGL.GL as GL


class VertexBuffer:
    def __init__(self):
        self.vbo = GL.glGenBuffers(1)
        self.count = 0

    def upload(self, points):
        # points é uma lista de (x, y)
        arr = np.array(points, dtype=np.float32)
        self.count = len(arr)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, arr.nbytes, arr, GL.GL_DYNAMIC_DRAW)

    def bind(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
