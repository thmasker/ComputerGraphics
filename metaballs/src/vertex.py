import math


class Vertex:
    def __init__(self, x: float, y: float, z: float, energy: float = 0, id: int = 0):
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.energy = energy

    def __eq__(self, v: 'Vertex') -> bool:
        if isinstance(v, Vertex):
            return self.x == v.x and self.y == v.y and self.z == v.z
        else:
            return False

    def __add__(self, v: 'Vertex') -> 'Vertex':
        return Vertex(self.x + v.x, self.y + v.y, self.z + v.z)

    def __radd__(self, v: 'Vertex') -> 'Vertex':
        return self - v

    def __sub__(self, v: 'Vertex') -> 'Vertex':
        return Vertex(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rsub__(self, v: 'Vertex') -> 'Vertex':
        return self - v

    def __mul__(self, n: float) -> 'Vertex':
        if isinstance(n, (float, int)):
            return Vertex(self.x * n, self.y * n, self.z * n)

    def __rmul__(self, n: float) -> 'Vertex':
        return self * n

    def __lt__(self, v: 'Vertex') -> bool:
        return self.id < v.id

    def __str__(self) -> str:
        return 'v ' + str(self.x) + ' ' + str(self.y) + ' ' + str(self.z)

    def distance(self, v: 'Vertex') -> float:
        return (v - self).module()

    def module(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normal(self, v: 'Vertex') -> 'Vertex':
        return Vertex((self.y * v.z - self.z * v.y) / self.module(), -(self.x * v.z - self.z * v.x) / self.module(), (self.x * v.y - self.y * v.x) / self.module())