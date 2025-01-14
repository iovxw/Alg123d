from alg123d import *

obj = Box(5, 5, 1)
for plane in Planes(obj.faces().filter_by(Axis.Z)):
    obj -= Sphere(1.8) @ plane

if "show_object" in locals():
    show_object(obj)
