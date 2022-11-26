from typing import List
from dataclasses import dataclass
import build123d as bd
from .wrappers import AlgCompound
from build123d.build_enums import Transition

__all__ = [
    "Empty3",
    "Box",
    "Cylinder",
    "Cone",
    "Sphere",
    "Torus",
    "Wedge",
    "CounterBore",
    "CounterSink",
    "Bore",
    "extrude",
    "loft",
    "revolve",
    "sweep",
    "section",
]


class Empty3(AlgCompound):
    def __init__(self):
        super().__init__(dim=3)


class Box(AlgCompound):
    def __init__(
        self,
        length: float,
        width: float,
        height: float,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            length=length,
            width=width,
            height=height,
            centered=centered,
        )
        self.create_part(bd.Box, params=params)


class Cylinder(AlgCompound):
    def __init__(
        self,
        radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            radius=radius,
            height=height,
            arc_size=arc_size,
            centered=centered,
        )
        self.create_part(bd.Cylinder, params=params)


class Cone(AlgCompound):
    def __init__(
        self,
        bottom_radius: float,
        top_radius: float,
        height: float,
        arc_size: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            bottom_radius=bottom_radius,
            top_radius=top_radius,
            height=height,
            arc_size=arc_size,
            centered=centered,
        )
        self.create_part(bd.Cone, params=params)


class Sphere(AlgCompound):
    def __init__(
        self,
        radius: float,
        arc_size1: float = -90,
        arc_size2: float = 90,
        arc_size3: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            radius=radius,
            arc_size1=arc_size1,
            arc_size2=arc_size2,
            arc_size3=arc_size3,
            centered=centered,
        )
        self.create_part(bd.Sphere, params=params)


class Torus(AlgCompound):
    def __init__(
        self,
        major_radius: float,
        minor_radius: float,
        minor_start_angle: float = 0,
        minor_end_angle: float = 360,
        major_angle: float = 360,
        centered: tuple[bool, bool, bool] = (True, True, True),
    ):
        params = dict(
            major_radius=major_radius,
            minor_radius=minor_radius,
            minor_start_angle=minor_start_angle,
            minor_end_angle=minor_end_angle,
            major_angle=major_angle,
            centered=centered,
        )
        self.create_part(bd.Torus, params=params)


class Wedge(AlgCompound):
    def __init__(
        self,
        dx: float,
        dy: float,
        dz: float,
        xmin: float,
        zmin: float,
        xmax: float,
        zmax: float,
    ):
        params = dict(
            dx=dx,
            dy=dy,
            dz=dz,
            xmin=xmin,
            zmin=zmin,
            xmax=xmax,
            zmax=zmax,
        )
        self.create_part(bd.Wedge, params=params)


class CounterBore(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        counter_bore_radius: float,
        counter_bore_depth: float,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            counter_bore_radius=counter_bore_radius,
            counter_bore_depth=counter_bore_depth,
            depth=depth,
        )
        self.create_part(bd.CounterBoreHole, part, params=params)


class CounterSink(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        counter_sink_radius: float,
        counter_sink_angle: float = 82,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            counter_sink_radius=counter_sink_radius,
            counter_sink_angle=counter_sink_angle,
            depth=depth,
        )
        self.create_part(bd.CounterSinkHole, part, params=params)


class Bore(AlgCompound):
    def __init__(
        self,
        part: AlgCompound,
        radius: float,
        depth: float = None,
    ):
        params = dict(
            radius=radius,
            depth=depth,
        )
        self.create_part(bd.Hole, part, params=params)


#
# Functions
#


def extrude(
    to_extrude: bd.Compound,
    amount: float,
    until: bd.Until = None,
    until_part: bd.Compound = None,
    both: bool = False,
    taper: float = 0.0,
):
    with bd.BuildPart() as ctx:
        # store to_extrude's faces in context
        ctx.pending_faces = (
            [to_extrude] if isinstance(to_extrude, bd.Face) else to_extrude.faces()
        )
        ctx.pending_face_planes = [
            bd.Plane(face.to_pln()) for face in ctx.pending_faces
        ]

        if len(ctx.pending_faces) == 0:
            raise RuntimeError(f"No faces found in {to_extrude}")

        if until_part is not None:
            ctx._add_to_context(until_part)

        # with bd.Locations(bd.Location()):
        compound = bd.Extrude(
            amount=amount,
            until=until,
            both=both,
            taper=taper,
            mode=bd.Mode.PRIVATE,
        )

    return AlgCompound(compound, {}, 3)


def loft(sections: List[AlgCompound | bd.Face], ruled: bool = False):
    faces = []
    for s in sections:
        if isinstance(s, bd.Compound):
            faces += s.faces()
        else:
            faces.append(s)

    with bd.BuildPart():
        compound = bd.Loft(*faces, ruled=ruled)

    return AlgCompound(compound, {}, 3)


def revolve(
    profiles: List[bd.Face],
    axis: bd.Axis,
    arc: float = 360.0,
):
    for p in profiles:
        faces = []
        if isinstance(p, bd.Compound):
            faces += p.faces()
        else:
            faces.append(p)

    with bd.BuildPart():
        compound = bd.Revolve(*faces, axis=axis, revolution_arc=arc)

    return AlgCompound(compound, {}, 3)


def sweep(
    sections: List[bd.Face | bd.Compound],
    path: bd.Edge | bd.Wire = None,
    multisection: bool = False,
    is_frenet: bool = False,
    transition: Transition = Transition.TRANSFORMED,
    normal: bd.VectorLike = None,
    binormal: bd.Edge | bd.Wire = None,
):
    with bd.BuildPart():
        compound = bd.Sweep(
            *sections,
            path=path,
            multisection=multisection,
            is_frenet=is_frenet,
            transition=transition,
            normal=normal,
            binormal=binormal,
        )

    return AlgCompound(compound, {}, 3)


def section(
    part: AlgCompound,
    by: List[bd.Plane],
    height: float = 0.0,
):
    with bd.BuildPart() as ctx:
        ctx._add_to_context(part)
        bd.Section(*by, height=height, mode=bd.Mode.INTERSECT)
        compound = ctx.part

    return AlgCompound(compound, {}, 3)
