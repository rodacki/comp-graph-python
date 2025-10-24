import pyglet
from OpenGL.GL import GL_COLOR_BUFFER_BIT, GL_VERSION, glClear, glClearColor, glGetString


def main():
    window = pyglet.window.Window(800, 600, "Ex01 - Hello OpenGL")

    @window.event
    def on_draw():
        glClearColor(0.1, 0.12, 0.16, 1.0)  # fundo cinza escuro
        glClear(GL_COLOR_BUFFER_BIT)

    def print_version(_):
        v = glGetString(GL_VERSION)
        if isinstance(v, (bytes, bytearray)):
            v = v.decode()
        print(f"OpenGL version: {v}")

    pyglet.clock.schedule_once(print_version, 0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
