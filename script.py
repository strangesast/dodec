import bpy
import itertools
import math
from mathutils import Euler, Vector
from functools import reduce

o = (1 + 5**(1/2))/2
z = (o/2 + 1/2*(o - 5/27)**(1/2))**(1/3) + (o/2 - 1/2*(o - 5/27)**(1/2))**(1/3)
a = z - 1/z
b = z*o + o**2 + o/z

vector = (
    (2*a,                       2,           2*b),
    (a + b/o + o,  -a*o + b + 1/o, a/o + b*o - 1),
    (a + b/o - o,   a*o - b + 1/o, a/o + b*o + 1),
    (-a/o + b*o + 1, -a + b/o - o, a*o + b - 1/o),
    (-a/o + b*o - 1,  a - b/o - o, a*o + b + 1/o)
)

def perm_parity(lst):
    parity = 1
    for i in range(0,len(lst)-1):
        if lst[i] != i:
            parity *= -1
            mn = min(range(i,len(lst)), key=lst.__getitem__)
            lst[i],lst[mn] = lst[mn],lst[i]
    return parity   

# mutations with even number of positive signs
signs = (x for x in itertools.product([-1, 1], repeat=3) if reduce(lambda a, y: (1 if y > 0 else 0)+a, x, 0)%2==0)
orders = tuple(filter(lambda x: perm_parity(list(x)) == 1, itertools.permutations(range(3))))

verts = []
for sign in signs:
    for order in orders:
        for v in vector:
            arr = [float(a*b) for (a, b) in zip([v[i] for i in order], sign)]
            #print(', '.join(['{0:+.5}']*3).format(*arr))
            verts.append(arr)

for i, vert in enumerate(verts):
    bpy.ops.object.text_add(location=vert)
    ob = bpy.context.object
    v = Vector(vert)
    v.normalize()
    t = v.to_track_quat('Z', 'Y').to_euler()
    ob.rotation_euler = Euler(tuple(t), 'XYZ')
    ob.data.body = '{}'.format(i)
    ob.data.extrude = 0.2
    ob.data.align_x = ob.data.align_y = 'CENTER'


starts = [0, 15, 30, 45]

faces = [
  [ 0,  1,  3,  4,  2],
  [ 1,  0,  8],
  [ 1,  8,  6],
  [ 1,  6, 11],
  [ 1,  11, 3],
  #[ 5,  6,  8,  9,  7],
  #[ 10, 11, 13, 14, 12],
  #[ 15, 16, 18, 19, 17]
]

faces = [[i, i+1, i+3, i+4, i+2] for i in range(0, 60, 5)]

def fn(a):
    i = a.index(min(a))
    return tuple(a[i:] + a[0:i])

me = bpy.data.meshes.new('mesh')
me.from_pydata(verts, [], list(set(map(fn, faces))))

ob = bpy.data.objects.new('dodec', me)
scene = bpy.context.scene
scene.objects.link(ob)
scene.objects.active = ob
ob.select = True
