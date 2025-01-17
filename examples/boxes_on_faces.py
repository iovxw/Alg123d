from alg123d import *

b = Box(3, 3, 3)
for plane in Planes(b.faces()):
    b += Box(1, 2, 0.1) @ (plane * Rot(0, 0, 45))

if "show_object" in locals():
    show_object(b)
