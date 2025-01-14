from alg123d import *

# simple

simple = extrude(Text("O", font_size=10, align=Align.CENTER), amount=5)

# both

both = extrude(
    Text("O", font_size=10, align=Align.CENTER),
    amount=5,
    both=True,
)

# multiple

multiple = Box(10, 10, 10)
t = AlgCompound()
for plane in Planes(multiple.faces()):
    for loc in GridLocations(5, 5, 2, 2):
        t += Text("Ω", font_size=3, align=Align.CENTER) @ (plane * loc)
multiple = multiple + extrude(t, amount=1)

# single minus multiple

rect = Rectangle(7, 7)
single_multiple = Box(10, 10, 10)
for loc in Planes(single_multiple.faces()):
    single_multiple -= extrude(rect.faces()[0], amount=-2) @ loc

# Non-planar surface
non_planar = Cylinder(10, 20, align=(Align.CENTER, Align.MIN, Align.CENTER)) @ Rot(x=90)
non_planar &= Box(10, 10, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
non_planar = extrude(non_planar.faces().min(), 2)

# Taper Extrude and Extrude to "next" while creating a Cherry MX key cap
# See: https://www.cherrymx.de/en/dev.html

plan = Rectangle(18 * MM, 18 * MM)
key_cap = extrude(plan, amount=10 * MM, taper=15)

# Create a dished top
key_cap -= Sphere(40 * MM) @ Location((0, -3 * MM, 47 * MM), (90, 0, 0))

# Fillet all the edges except the bottom
key_cap = fillet(
    key_cap,
    key_cap.edges().filter_by_position(Axis.Z, 0, 30 * MM, inclusive=(False, True)),
    radius=1 * MM,
)

# Hollow out the key by subtracting a scaled version
key_cap -= scale(key_cap, by=(0.925, 0.925, 0.85))


# Add supporting ribs while leaving room for switch activation
ribs = Rectangle(17.5 * MM, 0.5 * MM)
ribs += Rectangle(0.5 * MM, 17.5 * MM)
ribs += Circle(radius=5.51 * MM / 2)

# Extrude the mount and ribs to the key cap underside
key_cap += extrude_until(ribs @ Pos(z=4 * MM), key_cap)

# Find the face on the bottom of the ribs to build onto
rib_bottom = key_cap.faces().filter_by_position(Axis.Z, 4 * MM, 4 * MM)[0]


# Add the switch socket
plane = Plane(rib_bottom)
socket = Circle(radius=5.5 * MM / 2)
socket -= Rectangle(4.1 * MM, 1.17 * MM)
socket -= Rectangle(1.17 * MM, 4.1 * MM)
key_cap += extrude(socket @ plane, amount=3.5 * MM)

if "show_object" in locals():
    show_object(simple @ Pos(-15, 0, 0), name="simple pending extrude")
    show_object(both @ Pos(20, 10, 0), name="simple both")
    show_object(multiple @ Pos(0, -20, 0), name="multiple pending extrude")
    show_object(single_multiple @ Pos(0, 20, 0), name="single multiple")
    show_object(non_planar @ Pos(20, -10, 0), name="non planar")
    show_object(key_cap, name="key cap", options={"alpha": 0.7})
