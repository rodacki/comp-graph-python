from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
import math


# ----------------------------------------------------- #
#  Global variables - window (WCS)                      #
# ----------------------------------------------------- #
left = -10.0
right = 110.0
bottom = -30.0
top = 90.0


    
# tamanho da janela no sistema de interface
w,h= 500,500

class Button():
    def __init__(self, xc=0, yc=0, alt=10, larg=10, raio=2) -> None:
        self._xc = xc
        self._yc = yc
        self._larg = larg
        self._alt = alt
        self._raio = raio

    def draw(self):
        glColor3ub(150,150,150)
        glBegin(GL_QUADS)
        glVertex2d(self._xc - self._larg/2, self._yc - self._alt/2)
        glVertex2d(self._xc + self._larg/2, self._yc - self._alt/2)
        glVertex2d(self._xc + self._larg/2, self._yc + self._alt/2)
        glVertex2d(self._xc - self._larg/2, self._yc + self._alt/2)
        glEnd()
        glLineWidth(2.0)
        glColor3ub(94,93,91)
        glBegin(GL_LINE_LOOP)
        glVertex2d(self._xc - self._larg/2, self._yc - self._alt/2)
        glVertex2d(self._xc + self._larg/2, self._yc - self._alt/2)
        glVertex2d(self._xc + self._larg/2, self._yc + self._alt/2)
        glVertex2d(self._xc - self._larg/2, self._yc + self._alt/2)
        glEnd()

    def isInside(self, x, y):
        return x>=self._xc-self._larg/2 and x<=self._xc+self._larg/2 and y>=self._yc-self._alt/2 and y<=self._yc+self._alt/2

    def draw2(self):
        glLineWidth(2.0)
        glColor3ub(94,93,91)
        glBegin(GL_LINES)
        # base
        glVertex2d(self._xc - self._larg/2 + self._raio, self._yc-self._alt/2)
        glVertex2d(self._xc + self._larg/2 - self._raio, self._yc-self._alt/2)
        # dir
        glVertex2d(self._xc+self._larg/2, self._yc - self._alt/2+self._raio)
        glVertex2d(self._xc+self._larg/2, self._yc + self._alt/2-self._raio)
        # topo
        glVertex2d(self._xc - self._larg/2 + self._raio, self._yc+self._alt/2)
        glVertex2d(self._xc + self._larg/2 - self._raio, self._yc+self._alt/2)
        #esq
        glVertex2d(self._xc-self._larg/2, self._yc - self._alt/2+self._raio)
        glVertex2d(self._xc-self._larg/2, self._yc + self._alt/2-self._raio)
        glEnd()

        # sup direito
        glBegin(GL_LINE_STRIP)
        xo = self._xc + self._larg/2 - self._raio
        yo = self._yc + self._alt/2 - self._raio
        for i in range(0, 105, 15):
            x = xo + self._raio * math.cos(math.radians(i))
            y = yo + self._raio * math.sin(math.radians(i))
            glVertex2d(x, y)
        glEnd()

        # sup esquerdo
        glBegin(GL_LINE_STRIP)
        xo = self._xc - self._larg/2 + self._raio
        yo = self._yc + self._alt/2 - self._raio
        for i in range(90, 195, 15):
            x = xo + self._raio * math.cos(math.radians(i))
            y = yo + self._raio * math.sin(math.radians(i))
            glVertex2d(x, y)
        glEnd()

        # inf esquerdo
        glBegin(GL_LINE_STRIP)
        xo = self._xc - self._larg/2 + self._raio
        yo = self._yc - self._alt/2 + self._raio
        for i in range(180, 285, 15):
            x = xo + self._raio * math.cos(math.radians(i))
            y = yo + self._raio * math.sin(math.radians(i))
            glVertex2d(x, y)
        glEnd()

        # inf direito
        glBegin(GL_LINE_STRIP)
        xo = self._xc + self._larg/2 - self._raio
        yo = self._yc - self._alt/2 + self._raio
        for i in range(270, 375, 15):
            x = xo + self._raio * math.cos(math.radians(i))
            y = yo + self._raio * math.sin(math.radians(i))
            glVertex2d(x, y)
        glEnd()
        
    


class Slider():
    def __init__(self, xo, yo, larg, alt, r, g, b) -> None:
        self._xo = xo
        self._yo = yo
        self._larg = larg
        self._alt = alt
        self._r = r
        self._g = g
        self._b = b
        self._selector = Selector(xo+larg/2, yo+alt/2, alt)

    @property
    def selector(self):
        return self._selector
    
    @property 
    def value(self):
        return (self._selector.xc - self._xo)/self._larg
    
    @value.setter
    def value(self, novoValue):
        self._selector.xc = self._xo + novoValue * self._larg


    def draw(self):
        glBegin(GL_QUADS)
        glColor3ub(0,0,0)
        glVertex2d(self._xo, self._yo+self._alt)
        glVertex2d(self._xo, self._yo)
        glColor3ub(self._r,self._g, self._b)
        glVertex2d(self._xo+self._larg, self._yo)
        glVertex2d(self._xo+self._larg, self._yo+self._alt)
        glEnd()
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glColor3ub(94,93,91)
        glVertex2d(self._xo, self._yo+self._alt)
        glVertex2d(self._xo, self._yo)
        glVertex2d(self._xo+self._larg, self._yo)
        glVertex2d(self._xo+self._larg, self._yo+self._alt)
        glEnd()
        self._selector.draw()

    def isInside(self, x, y):
        return x>=self._xo and x<=self._xo+self._larg and y>=self._yo and y<=self._yo+self._alt


class Selector():
    def __init__(self, xc, yc, alt = 10) -> None:
        self._xc = xc
        self._yc = yc
        self._alt = alt
        self._selected = False
    
    @property
    def isSelected(self):
        return self._selected


    @property
    def xc(self):
        return self._xc
    
    @xc.setter
    def xc(self, novoxc):
        self._xc = novoxc

    @property
    def yc(self):
        return self._yc
    
    @yc.setter
    def yc(self, novoyc):
        self._yc = novoyc

    def draw(self):
        dy = self._alt/2.0
        glPushAttrib(GL_COLOR_BUFFER_BIT)
        glLineWidth(2.0)
        glColor3ub(255,255,255)
        glBegin(GL_LINES)
        glVertex2f(self.xc, self.yc-dy)
        glVertex2f(self.xc, self.yc+dy)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(self.xc, self.yc+dy-0.2)
        glVertex2f(self.xc-1, self.yc+dy+1.5)
        glVertex2f(self.xc+1, self.yc+dy+1.5)
        glEnd()
        glBegin(GL_TRIANGLES)
        glVertex2f(self.xc, self.yc-dy+0.2)
        glVertex2f(self.xc-1, self.yc-dy-1.5)
        glVertex2f(self.xc+1, self.yc-dy-1.5)
        glEnd()
        glPopAttrib()

    def isInside(self, x, y):
        return x>=self._xc-2 and x<=self._xc+2 and y>=self._yc-self._alt/2-2 and y<=self._yc+self._alt/2+2
    
    def select(self):
        self._selected = True

    def unselect(self):
        self._selected = False



# ----------------------------------------------------- #
#  Desenho da cor resultante                            #
# ----------------------------------------------------- #
def resultColor():
    glPushAttrib(GL_COLOR_BUFFER_BIT)
    glColor3ub(red,green,blue)
    glBegin(GL_QUADS)
    glVertex2d(20,0)
    glVertex2d(40,0)
    glVertex2d(40,15)
    glVertex2d(20,15)
    glEnd()
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(94,93,91)
    glVertex2d(20,0)
    glVertex2d(40,0)
    glVertex2d(40,15)
    glVertex2d(20,15)
    glEnd()
    glPopAttrib()


# ----------------------------------------------------- #
# Inicialização do OpenGL                               #
# ----------------------------------------------------- #
def init():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, -1.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ----------------------------------------------------- #
# Callback de redesenho de tela                         #
# ----------------------------------------------------- #
def showScreen():
    glClearColor(42/255, 40/255, 37/255, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    resultColor()
    sliderR.draw()
    sliderG.draw()
    sliderB.draw()
    resetButton.draw()
    glutSwapBuffers()


# ----------------------------------------------------- #
# Callback de eventos de teclado                        #
# ----------------------------------------------------- #   
def onKeyboard(key, x, y):
    print(key, type(key))
    # tecla escape para encerrar a aplicação
    if key.decode() == chr(27): 
        glutDestroyWindow(wind)
        sys.exit(0)

   
    
# ----------------------------------------------------- #
# Callback de eventos click de mouse                    #
# ----------------------------------------------------- #      
def onMouseButton(button, state, x,y):
    # conversão de coordenadas de tela para WCS
    global red
    global green
    global blue
    xw, yw = getWorldCoords(x,y)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print("x: {:3d} y: {:3d} \twx: {:.2f} wy: {:.2f}".format(x, y, xw, yw))

        if sliderR.isInside(xw, yw):
            #sliderR.selector.xc = xw
            #print("Dentro vermelhor!", sliderR.value)
            #red = int(sliderR.value * 255)
            if sliderR.selector.isInside(xw,yw):
                sliderR.selector.select()
                print("Seletor R")
    
        elif sliderG.isInside(xw, yw):
           # print("Dentro verde!", sliderG.value)
            #sliderG.selector.xc = xw
            #green = int(sliderG.value * 255)
            if sliderG.selector.isInside(xw,yw):
                sliderG.selector.select()
                print("Seletor G")
    
        elif sliderB.isInside(xw, yw):
            #print("Dentro azul!", sliderB.value)
            #sliderB.selector.xc = xw
            #blue = int(sliderB.value * 255)
            if sliderB.selector.isInside(xw,yw):
                sliderB.selector.select()
                print("Seletor B")

        elif resetButton.isInside(xw, yw):
            print("Reset")
            sliderR.value = 0.5
            sliderG.value = 0.5
            sliderB.value = 0.5
            red = int(sliderR.value * 255)
            green = int(sliderG.value * 255)
            blue = int(sliderB.value * 255)
        else: 
            print("Fora!")

    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        sliderR.selector.unselect()
        sliderG.selector.unselect()
        sliderB.selector.unselect()
        print("unselect")

    

    glutPostRedisplay()
        
# ----------------------------------------------------- #
# Callback de movimento de mouse                        #
# ----------------------------------------------------- #      
def mouseMotion(x,y):
    global red
    global green
    global blue
    wx, wy = getWorldCoords(x,y)
    if sliderR.selector.isSelected and sliderR.isInside(wx, wy):
        sliderR.selector.xc = wx
        red = int(sliderR.value * 255)
        glutPostRedisplay()
    elif sliderG.selector.isSelected and sliderG.isInside(wx, wy):
        sliderG.selector.xc = wx
        green = int(sliderG.value * 255)
        glutPostRedisplay()
    elif sliderB.selector.isSelected and sliderB.isInside(wx, wy):
        sliderB.selector.xc = wx
        blue = int(sliderB.value * 255)
        glutPostRedisplay()



# ----------------------------------------------------- #
# Projecao inversa de coordenadas                       #
# ----------------------------------------------------- #
def getWorldCoords(x, y):
    """
    Transforms screen coordinates (x, y) to OpenGL world coordinates.

    Args:
        x (int): The x screen coordinate.
        y (int): The y screen coordinate.

    Returns:
        tuple: A tuple containing the x and y world coordinates.

    Raises:
        ValueError: If the input screen coordinates are not within the viewport.

    This function calculates the world coordinates corresponding to the provided screen coordinates (x, y) by performing the following steps:

    1. Retrieves the current modelview and projection matrices, and the viewport dimensions using OpenGL calls.
    2. Inverts the projection and modelview matrices.
    3. Converts the screen coordinates to normalized device coordinates (NDC) in the range [-1, 1] for both x and y axes.
    4. Constructs a 4D NDC vector with z and w components set to 0 and 1, respectively.
    5. Transforms the NDC vector to clip space by multiplying with the inverse projection matrix.
    6. Transforms the clip space vector to world space by multiplying with the inverse modelview matrix.
    7. Extracts the x and y components of the transformed world space vector and returns them as a tuple.

    Note that this function assumes the depth is always 0 and only returns the x and y world coordinates. If you need all three world coordinates (x, y, z), you can modify the function to extract them accordingly.

    **Error Handling:**

    The function raises a `ValueError` if the provided screen coordinates are not within the viewport bounds.

    **Example Usage:**

    ```python
    x, y = 100, 200
    world_x, world_y = getWorldCoords(x, y)
    print(f"World coordinates: ({world_x:.2f}, {world_y:.2f})")
    ```
           
    # Reference: Karsten Lehn, Merijam Gotzes, Frank Klawonn. 
    # Introduction to Computer Graphics Using OpenGL and Java, 3. Ed.
    # Springer, ISBN 978-3-031-28134-1
    # págs. 171 e 416
     """
    # coordenadas do volume de visualização
    xr = right
    xl = left
    yt = top
    yb = bottom
    zn = 1.0
    zf = -1.0
    
    # matriz de projeçao (window + NDC)
    P =[
        [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
        [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
        [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] -1
    yndc = (2*(ywin-viewport[1]))/viewport[3] -1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc,wndc])

    
    # transformação de projeção inversa
    world = np.matmul(invP, vndc)

    # coordenadas no sistema WCS do OpenGL
    return world[0], world[1]

# ----------------------------------------------------- #
# Funcao principal do programa                          #
# ----------------------------------------------------- #
def main():
    global wind
    global red
    global green
    global blue
    global sliderR 
    global sliderG
    global sliderB
    global resetButton
    
    sliderR= Slider(0, 70, 100, 10, 255, 0, 0)
    sliderG= Slider(0, 50, 100, 10, 0, 255, 0)
    sliderB= Slider(0, 30, 100, 10, 0, 0, 255)

    red = int(sliderR.value * 255)
    green = int(sliderG.value * 255)
    blue = int(sliderB.value * 255)

    resetButton = Button(70, 10, 10, 20, 2)

   
    glutInit()
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow("IFC - Exemplo Color Picker - 2024")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutKeyboardFunc(onKeyboard)
    glutMouseFunc(onMouseButton)
    glutMotionFunc(mouseMotion)
    init()
    glutMainLoop()
    
    
if __name__ == "__main__":
    main()
