import sys, os, json, math
from typing import List, Tuple

from blob import Blob
from vertex import Vertex
from face import Face


ID = 1
VERTICES = []


def usage():
    print('Metaballs Generator')
    print('-----------------------------------------------')
    print('Usage: metaballs <description file (.json)>*')
    print('-----------------------------------------------')
    print('Input files format:')
    print(json.dumps({"grid_size": "<double>","threshold": "<double>","blobs": [{"position": ["x", "y", "z"],"energy": "<double>","radius": "<double>"}, '...']}, sort_keys=True, indent=4))
    print('-----------------------------------------------')


def parse_json(file: str) -> Tuple[float, float, List[Blob]]:
    """
    Parses input JSON to obtain:
        - grid_size
        - threshold
        - all defined metaballs
    """

    blobs = []

    with open(file) as f:
        data = json.load(f)
        
        grid_size = data['grid_size']
        threshold = data['threshold']
        
        for blob in data['blobs']:
            blobs.append(Blob(blob['position'], blob['energy'], blob['radius']))

    return grid_size, threshold, blobs


def create_grid(blobs: List[Blob], grid_size: float) -> List[List[List[Vertex]]]:
    """
    Creates 3D grid with the minimum length possible, depending on grid_size and the position of metaballs
    """

    x_max, x_min = 0, 0
    y_max, y_min = 0, 0
    z_max, z_min = 0, 0

    for blob in blobs:
        r = blob.radius

        x_max = max(blob.position.x + r, x_max)
        x_min = min(blob.position.x - r, x_min)

        y_max = max(blob.position.y + r, y_max)
        y_min = min(blob.position.y - r, y_min)

        z_max = max(blob.position.z + r, z_max)
        z_min = min(blob.position.z - r, z_min)

    X = x_max - x_min
    Y = y_max - y_min
    Z = z_max - z_min

    grid = []
    for i in range(math.ceil(X / grid_size)):
        ys = []
        for j in range(math.ceil(Y / grid_size)):
            zs = []
            for k in range(math.ceil(Z / grid_size)):
                zs.append(Vertex(x_min + i * grid_size, y_min + j * grid_size, z_min + k * grid_size))
            ys.append(zs)
        grid.append(ys)

    return grid


def calc_energy(blobs: List[Blob], vertex: Vertex) -> float:
    """
    Calculates energy in the given vertex
    """

    energy = 0
    for blob in blobs:
        d = vertex.distance(blob.position)

        if d < blob.radius:
            fallOff = 1 - (d / blob.radius)
            energy += blob.energy * math.pow(fallOff, 2)

    return energy


def calc_grid_energy(blobs: List[Blob], grid: List[List[List[Vertex]]], threshold: float) -> List[List[List[Vertex]]]:
    """
    Returns the whole grid in which all vertices have their corresponding energies
    """

    for x in grid:
        for y in x:
            for vertex in y:
                vertex.energy = calc_energy(blobs, vertex)

    return grid


def get_cubes(grid: List[List[List[Vertex]]]) -> List[List[Vertex]]:
    """
    Returns a list containing each possible cube (8 vertices) in the grid
    """
    
    cubes = []
    for i in range(len(grid) - 1):
        for j in range(len(grid[0]) - 1):
            for k in range(len(grid[0][0]) - 1):
                v1 = grid[i][j][k]
                v2 = grid[i + 1][j][k]
                v3 = grid[i + 1][j + 1][k]
                v4 = grid[i][j + 1][k]
                v5 = grid[i][j][k + 1]
                v6 = grid[i + 1][j][k +1]
                v7 = grid[i + 1][j + 1][k + 1]
                v8 = grid[i][j + 1][k + 1]

                cubes.append([v1, v2, v3, v4, v5, v6, v7, v8])

    return cubes


def get_tetrahedrons(cubes: List[List[Vertex]]) -> List[List[Vertex]]:
    """
    Returns a list containing each possible tetrahedron (4 vertices) for each cube (5 tetrahedrons per cube).
    """

    tetrahedrons = []
    for cube in cubes:
        tetrahedrons.append([cube[0], cube[1], cube[3], cube[4]])
        tetrahedrons.append([cube[1], cube[4], cube[5], cube[6]])
        tetrahedrons.append([cube[1], cube[3], cube[4], cube[6]])
        tetrahedrons.append([cube[1], cube[2], cube[3], cube[6]])
        tetrahedrons.append([cube[3], cube[4], cube[6], cube[7]])

    return tetrahedrons


def get_surface_points(tetrahedron: List[Vertex], threshold: float) -> List[Vertex]:
    """
    Returns vertices belonging to the surface of the metaball
    """

    global ID

    vs_below = [vertex for vertex in tetrahedron if vertex.energy < threshold]
    vs_beyond = [vertex for vertex in tetrahedron if vertex.energy > threshold]

    surface_points = []
    for a in vs_below:
        for b in vs_beyond:
            ratio = (threshold - a.energy) / (b.energy - a.energy)
            vec = b - a
            vertex = ratio * vec + a

            if vertex in VERTICES:
                surface_points.append(VERTICES[VERTICES.index(vertex)])
            else:
                vertex.id = ID
                ID += 1
                surface_points.append(vertex)
                VERTICES.append(vertex)
    
    return surface_points


def face_orientation(blobs: List[Blob], face: Face, threshold: float) -> Face:
    """
    Returns the well oriented face
    """

    p = face.v1 + face.normal() * 2
    p.energy = calc_energy(blobs, p)

    if p.energy < threshold:
        return face
    else:
        face.v1, face.v3 = face.v3, face.v1

        return face


def get_faces(blobs: List[Blob], tetrahedrons: List[List[Vertex]], threshold: float) -> List[Face]:
    """
    Returns a list containing all faces defining the surface to draw
    """

    faces = []
    for tetrahedron in tetrahedrons:
        if not all(vertex.energy > threshold for vertex in tetrahedron) and not all(vertex.energy < threshold for vertex in tetrahedron):
            surface_points = get_surface_points(tetrahedron, threshold)

            if surface_points:
                faces.append(face_orientation(blobs, Face(surface_points[0], surface_points[1], surface_points[2]), threshold))

                if len(surface_points) > 3:
                    faces.append(face_orientation(blobs, Face(surface_points[1], surface_points[2], surface_points[3]), threshold))

    return faces


def to_obj(vertices: List[Vertex], faces: List[Face], file: str):
    """
    Creates .obj file
    """

    new_file = os.path.splitext(file)
    with open(new_file[0] + '.obj', 'w') as f:
        f.write('# Metaballs created with metaballs.py\n')
        f.write('# Diego Pedregal Hidalgo, 2020\n\n')
        f.write('\n'.join([str(vertex) for vertex in vertices]))
        f.write('\n\n')
        f.write('\n'.join([str(face) for face in faces]))


def main(args: List[str]):
    print('Metaballs Generator')
    print('-----------------------------------------------')

    for file in args:
        print('Generating ' + file)

        grid_size, threshold, blobs = parse_json(file)

        grid = create_grid(blobs, grid_size)
        grid = calc_grid_energy(blobs, grid, threshold)

        cubes = get_cubes(grid)

        tetrahedrons = get_tetrahedrons(cubes)
        faces = get_faces(blobs, tetrahedrons, threshold)

        to_obj(VERTICES, faces, file)

    print('.obj file generated')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    else:
        main(sys.argv[1:])