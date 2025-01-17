from alg123d import *

width = 1.6
fillet_radius = 0.08
dist = 0.9
eye_radius = 0.23
eye_offset = 0.15

eye_locs = list(GridLocations(dist, dist / 2, 2, 3)) + [Location((0, 0, 0))]


def eyes(face, ind):
    p = Plane(face) * Location((0, 0, eye_offset))  # eye_offset above plane
    rv = AlgCompound()
    for loc in [eye_locs[i] for i in ind]:
        rv += Sphere(eye_radius) @ (p * loc)
    return rv


dice = Box(width, width, width)
dice = fillet(dice, dice.edges(), fillet_radius)

sides = [
    (dice.faces().min(Axis.Z), [6]),  # 1
    (dice.faces().max(Axis.Z), [0, 1, 2, 3, 4, 5]),  # 6
    (dice.faces().min(Axis.Y), [0, 5]),  # 2
    (dice.faces().max(Axis.Y), [0, 2, 3, 5, 6]),  # 5
    (dice.faces().min(Axis.X), [2, 3, 6]),  # 3
    (dice.faces().max(Axis.X), [0, 2, 3, 5]),  # 4
]

dice -= [eyes(*side) for side in sides]


if "show_object" in locals():
    show_object(dice, "dice", options={"color": "silver"})
