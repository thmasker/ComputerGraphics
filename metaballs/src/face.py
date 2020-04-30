from typing import List

from vertex import Vertex


class Face:
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def __eq__(self, f: 'Face') -> bool:
        if isinstance(f, Face):
            vertices = [f.v1, f.v2, f.v3]
            if self.normal == f.normal:
                return self.v1 in vertices and self.v2 in vertices and self.v3 in vertices
            else:
                return False
        else:
            return False

    def __str__(self) -> str:
        return 'f ' + str(self.v1.id) + ' ' + str(self.v2.id) + ' ' + str(self.v3.id)

    def normal(self) -> Vertex:
        vec1 = self.v2 - self.v1
        vec2 = self.v3 - self.v1

        return vec1.normal(vec2)

    def list_vertices(self) -> List[Vertex]:
        return [self.v1, self.v2, self.v3]