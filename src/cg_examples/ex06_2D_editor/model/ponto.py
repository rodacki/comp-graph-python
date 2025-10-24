class Ponto:
    def __init__(self, x=0.0, y=0.0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, novox):
        self._x = novox

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, novoy):
        self._y = novoy

    def __str__(self):
        return f"({self._x:.2f}, {self._y:.2f})"
