import math
from typing import List, Tuple

def toVertex(line: str) -> List[float]:
    '''
    Input: 'v x y z' => Output: [x, y, z]
    '''
    coordinates = line.split(' ')[1:]
    return list(map(float, coordinates))


def toFace(line: str) -> List[int]:
    '''
    Input: 'f v1 v2 v3' => Output: [v1, v2, v3]
    Input: 'l v1 v2' => Output: [v1, v2]
    '''
    vertices = line.split(' ')[1:]
    return list(map(int, vertices))


def module(vector: List[float]) -> float:
    '''
    Input: [x, y, z] => Output: module of such vector
    '''
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)


def unitary(vector: List[float]) -> List[float]:
    '''
    Input: [x, y, z] => Output: Its unitary vector
    '''
    mod = module(vector)
    return [v / mod for v in vector]


def toVector(v1: List[float], v2: List[float]) -> List[float]:
    '''
    Input: Two vertices [x, y, z] => Output: Vector [x, y, z] composed by such vertices
    '''
    return [b - a for (b, a) in zip(v2, v1)]


def crossProduct(v1: List[float], v2: List[float]) -> List[float]:
    '''
    Input: Two vectors [x, y, z] => Output: Vector [x, y, z], result of the cross product
    '''
    return [v1[1] * v2[2] - v1[2] * v2[1], - (v1[0] * v2[2] - v1[2] * v2[0]), v1[0] * v2[1] - v1[1] * v2[0]]


def normalVector(vertices: List[List[float]], faces: List[List[int]]) -> List[float]:
    '''
    Input: Vertices and faces of object => Output: Vector [x, y, z] normal to the surface of the object
    '''
    face = faces[0]
    a = vertices[face[0] - 1]
    b = vertices[face[1] - 1]
    c = vertices[face[2] - 1]

    ab = toVector(a, b)
    ac = toVector(a, c)

    normal = crossProduct(ab, ac)
    return unitary(normal)


def toString(element: List[List[float]], e_type: str) -> List[str]:
    '''
    Input: [v1, v2, v3] => Output: 'f v1 v2 v3'
    Input: [x, y, z] => Output: 'v x y z'
    '''
    s = ''
    for e in element:
        e = [round(n, 6) for n in e]
        e = list(map(str, e))

        s += e_type + ' '
        s += ' '.join(e)
        s += '\n'

    return s


def getBoundaryEdges(edges: List[Tuple[int]]) -> List[Tuple[int]]:
    '''
    Input: [(v1, v2), (v2, v3) ...] => Output: [(v1, v2), ...] only the boundary edges
    '''
    i = 0
    while i < len(edges):
        j = i + 1
        removed = False
        while j < len(edges):
            if sorted(edges[i]) == sorted(edges[j]):
                edges.pop(i)
                edges.pop(j - 1)

                removed = True

            j += 1
        if not removed:
            i += 1

    return edges


def multiply(matrix: List[List[float]], vertex: List[float]) -> List[float]:
    '''
    Simple matrix multiplication function. Computationally expensive as we increase dimensionality, but, working with 3D, dimensionality is fixed. In further improvements we could optimize this function
    '''
    result = [0, 0, 0]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            m = matrix[i][j]
            v = vertex[j]
            result[i] += m * v

    return result


def toRadians(angle: float) -> float:
    '''
    Input: degrees => Output: radians
    '''
    return angle * math.pi / 180


def rotate(vertex: List[float], angle: float, axis: str) -> List[float]:
    '''
    Input: [x, y, z] => Output: [x, y, z] with rotated coordinates
    '''
    angle = toRadians(angle)

    if axis == 'x':
        matrix = [[1, 0, 0], [0, math.cos(-angle), -math.sin(-angle)], [0, math.sin(-angle), math.cos(-angle)]]
    elif axis == 'y':
        matrix = [[math.cos(angle), -math.sin(angle), 0], [math.sin(angle), math.cos(angle), 0 ], [0, 0, 1]]
    else:
        matrix = [[math.cos(-angle), 0, math.sin(-angle)], [0, 1, 0], [-math.sin(-angle), 0, math.cos(-angle)]]

    return multiply(matrix, vertex)