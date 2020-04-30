from typing import List

from vertex import Vertex

class Blob:
    def __init__(self, position: List[float], energy: float, radius: float):
        self.position = Vertex(position[0], position[1], position[2])

        sign = lambda x: (x > 0) - (x < 0)
        self.energy = energy if energy <= 10 and energy >= -10 else sign(energy) * 10
        self.radius = radius if radius > 0 else 0