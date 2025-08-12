import glfw
import numpy as np
from OpenGL.GL import *

 # --- Dados de vértices (float32) ---
vertices = np.array([
    -0.5, -0.5, 0.0,  # v0
     0.5, -0.5, 0.0,  # v1
     0.0,  0.5, 0.0   # v2
], dtype=np.float32)


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)

def main(): 
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if (window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        return  
    
    # Torna o contexto OpenGL atual
    glfw.make_context_current(window)

    glViewport(0, 0, 800, 600)

    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback) 

    while not glfw.window_should_close(window):
        processInput(window)

        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

    return

""" def main():
    # Inicializa o GLFW
    if not glfw.init():
        raise Exception("Falha ao inicializar o GLFW")

    # Cria uma janela
    window = glfw.create_window(800, 600, "Exemplo GLFW", None, None)
    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    # Torna o contexto OpenGL atual
    glfw.make_context_current(window)

    # Loop principal
    while not glfw.window_should_close(window):
        # Limpa a tela
        glClearColor(0.2, 0.3, 0.3, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        # Desenha um triângulo simples
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex2f(-0.5, -0.5)
        glColor3f(0, 1, 0)
        glVertex2f(0.5, -0.5)
        glColor3f(0, 0, 1)
        glVertex2f(0.0, 0.5)
        glEnd()

        # Troca os buffers e processa eventos
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
 """
if __name__ == "__main__":
    main()