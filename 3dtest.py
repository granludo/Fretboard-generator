from madcad import *

# define points
O = vec3(0)
A = vec3(2,0,0)
B = vec3(1,2,0)
C = vec3(0,2,0)

# create a list of primitives
line = [
	Segment(O, A),
	ArcThrough(A, B, C),
	Segment(C,O),
	]

# create and solve constraints
solve([
		Tangent(line[0], line[1], A),
		Tangent(line[1], line[2], C),
		Radius(line[1], 1.5),
	], fixed=[O])

# generate surfaces
part = extrusion(vec3(0,0,1), web(line))

# display in a 3D scene
show([part])
