import time

from alg123d import *
from alg123d.shortcuts import *

# %%
diam = 200  # 175
meshop = 2
gridxy = int(diam / meshop / 2)

a = time.time()
with LazyZero() as holes:
    r = Rectangle(meshop, meshop)
    for loc in GridLocations(meshop * 2, meshop * 2, gridxy, gridxy):
        if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - meshop * 0.9) ** 2:
            holes += r @ loc

c = Circle(diam / 2) - holes
print(time.time() - a)
show(c)

# %%

a = time.time()

r = Rectangle(meshop, meshop)
holes = [
    r @ loc
    for loc in GridLocations(meshop * 2, meshop * 2, gridxy, gridxy)
    if loc.position.X**2 + loc.position.Y**2 < (diam / 2 - meshop * 0.9) ** 2
]

c = Circle(diam / 2) - holes
print(time.time() - a)
show(c)

# %%

a = time.time()

rectangles = []
r = Face.make_rect(meshop, meshop)
for loc in GridLocations(meshop * 2, meshop * 2, gridxy, gridxy):
    rectangles.append(r.located(loc))

holes = rectangles.pop().fuse(*rectangles).clean()
c = Circle(diam / 2) - AlgCompound(holes, 2)
print(time.time() - a)

# %%