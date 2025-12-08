import OpenGL.GL as GL


class ShaderProgram:
    def __init__(self, vert_src: str, frag_src: str):
        self.program = GL.glCreateProgram()

        vs = self._compile(GL.GL_VERTEX_SHADER, vert_src)
        fs = self._compile(GL.GL_FRAGMENT_SHADER, frag_src)

        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)

        if GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS) != GL.GL_TRUE:
            log = GL.glGetProgramInfoLog(self.program)
            raise RuntimeError(f"Shader link error: {log}")

        GL.glDeleteShader(vs)
        GL.glDeleteShader(fs)

    def _compile(self, shader_type, source):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)

        if GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS) != GL.GL_TRUE:
            log = GL.glGetShaderInfoLog(shader)
            raise RuntimeError(f"Shader compile error: {log}")

        return shader

    def use(self):
        GL.glUseProgram(self.program)

    def uniform_location(self, name):
        return GL.glGetUniformLocation(self.program, name)
