"""Cria uma janela Pyglet com uma área de visualização OpenGL."""

import ctypes

import pyglet

from .shaders import FRAGMENT_SHADER_SOURCE, VERTEX_SHADER_SOURCE

# Mantém o tamanho da janela em unidades lógicas e permite que o framebuffer
# use a resolução física da tela (por exemplo, 2x em um Retina display).
pyglet.options.dpi_scaling = "stretch"


class CADWindow(pyglet.window.Window):
    """Janela principal do exemplo de CAD 2D."""

    def __init__(self) -> None:
        """Cria a janela e solicita um contexto OpenGL moderno."""
        config = pyglet.gl.Config(
            major_version=3,
            minor_version=3,
            double_buffer=True,
        )
        super().__init__(
            width=800,
            height=600,
            caption="Ex09 - CAD 2D com Pyglet",
            config=config,
            resizable=True,
        )

        pyglet.gl.glClearColor(0.08, 0.10, 0.14, 1.0)

        print(f"Tamanho lógico da janela: {self.get_size()}")
        print(f"Tamanho físico do framebuffer: {self.get_framebuffer_size()}")

        self._is_closing = False
        # Compila e liga (link) os dois shaders. O resultado é o programa que
        # será ativado em on_draw para executar código na GPU.
        self._shader_program = self._create_shader_program()

        # Estas duas linhas NÃO criam ainda objetos OpenGL. Elas criam apenas
        # variáveis ctypes, na CPU, capazes de guardar identificadores GLuint.
        # glGenVertexArrays e glGenBuffers preencherão essas variáveis abaixo.
        self._vao = pyglet.gl.GLuint()
        self._vbo = pyglet.gl.GLuint()

        # Agora os objetos OpenGL são criados, configurados e recebem os dados.
        self._create_axes_buffers()

    @staticmethod
    def _create_shader_program():
        """Compila os shaders e cria o programa executado pela GPU."""
        # Shader transforma o texto GLSL em um shader compilado.
        vertex_shader = pyglet.graphics.shader.Shader(VERTEX_SHADER_SOURCE, "vertex")
        fragment_shader = pyglet.graphics.shader.Shader(FRAGMENT_SHADER_SOURCE, "fragment")

        # ShaderProgram liga os shaders compilados em um único programa.
        return pyglet.graphics.shader.ShaderProgram(vertex_shader, fragment_shader)

    def _create_axes_buffers(self) -> None:
        """Cria um VAO e um VBO persistente com os dois eixos em NDC."""
        # Cada vértice contém: x, y, vermelho, verde, azul.
        vertices = (pyglet.gl.GLfloat * 20)(
            -0.9,
            0.0,
            1.0,
            0.0,
            0.0,
            0.9,
            0.0,
            1.0,
            0.0,
            0.0,
            0.0,
            -0.9,
            0.0,
            1.0,
            0.0,
            0.0,
            0.9,
            0.0,
            1.0,
            0.0,
        )

        # Pede ao OpenGL um VAO e grava seu identificador em self._vao.
        pyglet.gl.glGenVertexArrays(1, ctypes.byref(self._vao))

        # Pede ao OpenGL um buffer e grava seu identificador em self._vbo.
        pyglet.gl.glGenBuffers(1, ctypes.byref(self._vbo))

        # Um bind seleciona o objeto sobre o qual as próximas chamadas atuarão.
        # A configuração de atributos feita a seguir ficará registrada no VAO.
        pyglet.gl.glBindVertexArray(self._vao)

        # Seleciona nosso VBO como o buffer de vértices atualmente ativo.
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, self._vbo)

        # Reserva memória para o VBO e copia 'vertices' da CPU para o OpenGL.
        # GL_STATIC_DRAW informa que os dados mudarão raramente, mas serão
        # utilizados muitas vezes para desenhar.
        pyglet.gl.glBufferData(
            pyglet.gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(vertices),
            vertices,
            pyglet.gl.GL_STATIC_DRAW,
        )

        # Distância, em bytes, entre o início de dois vértices consecutivos:
        # cinco floats = x, y, vermelho, verde e azul.
        stride = 5 * ctypes.sizeof(pyglet.gl.GLfloat)

        # Descreve o atributo de posição, correspondente a:
        # layout (location = 0) in vec2 position;
        # Ele começa no byte 0 e consome dois floats de cada vértice.
        pyglet.gl.glVertexAttribPointer(
            0, 2, pyglet.gl.GL_FLOAT, pyglet.gl.GL_FALSE, stride, ctypes.c_void_p(0)
        )
        pyglet.gl.glEnableVertexAttribArray(0)

        # A cor começa depois dos dois floats usados pela posição.
        color_offset = 2 * ctypes.sizeof(pyglet.gl.GLfloat)

        # Descreve o atributo de cor, correspondente a:
        # layout (location = 1) in vec3 color;
        # Ele consome três floats de cada vértice.
        pyglet.gl.glVertexAttribPointer(
            1,
            3,
            pyglet.gl.GL_FLOAT,
            pyglet.gl.GL_FALSE,
            stride,
            ctypes.c_void_p(color_offset),
        )
        pyglet.gl.glEnableVertexAttribArray(1)

        # Retira os objetos de seu estado ativo. Isso evita que outras partes
        # do programa os modifiquem acidentalmente durante a inicialização.
        pyglet.gl.glBindBuffer(pyglet.gl.GL_ARRAY_BUFFER, 0)
        pyglet.gl.glBindVertexArray(0)

    def on_draw(self) -> None:
        """Limpa a área de desenho e desenha os eixos X e Y."""
        # No macOS, um redraw que já estava agendado pode chegar enquanto a
        # janela está fechando, depois da liberação dos recursos OpenGL.
        if self._is_closing:
            return

        self.clear()

        # Ativa o programa de shaders que processará os próximos vértices.
        self._shader_program.use()

        # Seleciona o VAO. Ele recupera a descrição dos atributos e a ligação
        # com o VBO configuradas em _create_axes_buffers.
        pyglet.gl.glBindVertexArray(self._vao)

        # Interpreta os quatro vértices como pares independentes:
        # vértices 0-1 formam o eixo X; vértices 2-3 formam o eixo Y.
        pyglet.gl.glDrawArrays(pyglet.gl.GL_LINES, 0, 4)

        # Encerra explicitamente o uso dos objetos neste frame.
        pyglet.gl.glBindVertexArray(0)
        self._shader_program.stop()

    def on_close(self) -> None:
        """Libera os recursos OpenGL antes de fechar a janela."""
        if self._is_closing:
            return

        self._is_closing = True
        pyglet.gl.glDeleteBuffers(1, ctypes.byref(self._vbo))
        pyglet.gl.glDeleteVertexArrays(1, ctypes.byref(self._vao))
        self._shader_program.delete()
        self.close()


def main() -> None:
    """Cria a janela e inicia o loop de eventos do Pyglet."""
    # Window.__init__ registra esta instância em pyglet.app.windows.
    # Mantemos também uma referência explícita enquanto o loop está ativo.
    window = CADWindow()
    pyglet.app.run()
    del window  # O loop terminou; nossa referência à janela não é mais necessária.


if __name__ == "__main__":
    main()
