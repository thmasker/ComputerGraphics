'''
Algorithm designed following the slide 15 of Session 8
'''
import sys, getopt, os.path
from typing import List

import utils


def usage():
	print('Simple Extrusion')
	print('------------------------------------')
	print('Usage: extrude <options> <.obj file>*')
	print('<options>:')
	print('\t-d, --distance=')
	print('------------------------------------')
	print('IMPORTANT: Input files MUST define triangulated faces')

def main(argv: List[str]):
	distance = 0
	try:
		opts, args = getopt.getopt(argv, "d:", ['help', 'distance='])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '--help':
			usage()
			sys.exit()
		elif opt in ('-d', '--distance'):
			try:
				distance = float(arg)
			except ValueError:
				print("Distance '" + arg +  "' is not a valid number (int or float)")
				sys.exit(2)

	for file in args:
		try:
			f = open(file)
		except FileNotFoundError as fne:
			print(fne.strerror + ": '" + file + "'")
			sys.exit(2)

		lines = f.readlines()
		f.close()

		vertices = []
		faces = []
		info = []
		for line in lines:
			if line[0] == 'v':
				vertices.append(utils.toVertex(line))
			elif line[0] == 'f':
				faces.append(utils.toFace(line))
			else:
				info.append(line)

		n_vertices = len(vertices)
		n_faces = len(faces)

		'''
		Step 1
		For each vertex, add distance * normalVector to it, appending result to the vertex array
		'''
		normal = utils.normalVector(vertices, faces)
		normal = [n * distance for n in normal]
		for i in range(n_vertices):
			vertices.append([v + n_i for (v, n_i) in zip(vertices[i], normal)])
		
		'''
		Step 2
		Create list of boundary edges
		'''
		combinations = []
		for face in faces:
			combinations.append([(face[0], face[1]), (face[1], face[2]), (face[2], face[0])])

		edges = [edge for face in combinations for edge in face]
		boundary_edges = utils.getBoundaryEdges(edges)

		'''
		Step 3
		For each face, create the extruded face, adding distance * normalVector to its vertices
		'''
		for i in range(n_faces):
			faces.append([v + n_vertices for v in faces[i]])

		'''
		Step 4
		Create sides of extruded shape. For each boundary edge, add the new faces
		'''
		for edge in boundary_edges:
			faces.append([edge[0], edge[1], edge[1] + n_vertices])
			faces.append([edge[1] + n_vertices, edge[0] + n_vertices, edge[0]])

		'''
		Step 5
		Invert normal vector of original faces
		'''
		for i in range(n_faces):
			faces[i].reverse()

		new_file = os.path.splitext(file)
		with open(new_file[0] + '_extruded' + new_file[1], 'w') as f:
			f.write(''.join(info))
			f.write(''.join(utils.toString(vertices, 'v')))
			f.write(''.join(utils.toString(faces, 'f')))


if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()
	else:
		main(sys.argv[1:])