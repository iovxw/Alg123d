import copy
from typing import List
from dataclasses import dataclass

import build123d as bd
from .direct_api import Workplane

from OCP.BRepBuilderAPI import (  # pyright: ignore[reportMissingImports]
    BRepBuilderAPI_Copy,
)

Obj1d = bd.Compound | bd.Wire | bd.Edge
Obj2d = bd.Compound | bd.Face
Obj3d = bd.Compound | bd.Solid
Obj12d = Obj1d | Obj2d
Obj23d = Obj2d | Obj3d
Obj123d = Obj1d | Obj2d | Obj3d

CTX = [None, bd.BuildLine, bd.BuildSketch, bd.BuildPart]

__all__ = [
    "AlgCompound",
    "create_compound",
]

#
# Algebra operations enhanced Compound
#


class AlgCompound(bd.Compound):
    def __init__(self, compound=None, params=None, dim: int = None):
        self.wrapped = None if compound is None else compound.wrapped
        self.dim = dim
        self._params = [] if params is None else params

    def create_part(
        self,
        cls,
        part=None,
        faces=None,
        planes=None,
        params=None,
    ):
        if params is None:
            params = {}

        with bd.BuildPart() as ctx:
            if part is not None:
                ctx._add_to_context(part)

            if faces is not None:
                ctx.pending_faces = faces

            if planes is not None:
                ctx.pending_face_planes = planes

            self.wrapped = cls(**params, mode=bd.Mode.PRIVATE).wrapped

        self._params = params
        self.dim = 3

    def create_sketch(self, cls, objects=None, params=None):
        if params is None:
            params = {}

        with bd.BuildSketch():
            if objects is None:
                self.wrapped = cls(**params, mode=bd.Mode.PRIVATE).wrapped
            else:
                self.wrapped = cls(*objects, **params, mode=bd.Mode.PRIVATE).wrapped

        self._params = params
        self.dim = 2

    def _place(
        self,
        mode: bd.Mode,
        obj: Obj23d,
        at: bd.Location = None,
    ):
        if at is None:
            located_obj = obj
            loc = obj.location
        else:
            if isinstance(at, bd.Location):
                loc = at
            elif isinstance(at, Workplane):
                loc = at.to_location()
            elif isinstance(at, tuple):
                loc = bd.Location(at)
            else:
                raise ValueError(f"{at } is no location or plane")

            located_obj = obj.located(loc)

        if self.wrapped is None:
            if mode == bd.Mode.ADD:
                compound = located_obj
            else:
                raise RuntimeError("Can only add to empty object")
        else:
            compound = self
            if mode == bd.Mode.ADD:
                compound = compound.fuse(located_obj).clean()
            elif mode == bd.Mode.SUBTRACT:
                compound = compound.cut(located_obj).clean()
            elif mode == bd.Mode.INTERSECT:
                compound = compound.intersect(located_obj).clean()

        return AlgCompound(compound, {}, self.dim)

    def __add__(self, other: Obj23d):
        return self._place(bd.Mode.ADD, other)

    def __sub__(self, other: Obj23d):
        return self._place(bd.Mode.SUBTRACT, other)

    def __and__(self, other: Obj23d):
        return self._place(bd.Mode.INTERSECT, other)

    def __matmul__(self, obj):
        if isinstance(obj, bd.Location):
            loc = obj
        elif isinstance(obj, tuple):
            loc = bd.Location(obj)
        elif isinstance(obj, Workplane):
            loc = obj.to_location()
        else:
            raise ValueError(f"Cannot multiply with {obj}")

        return self.located(loc)

    def __repr__(self):
        def r2(v):
            return tuple([round(e, 2) for e in v])

        p = ""
        for k, v in self._params.items():
            p += f"{k}={v},"

        loc_str = f"position={r2(self.location.position)}, rotation={r2(self.location.orientation)}"
        return f"{self.__class__.__name__}({p}); loc=({loc_str}); dim={self.dim}"

    def copy(self):
        memo = {}
        memo[id(self.wrapped)] = bd.downcast(BRepBuilderAPI_Copy(self.wrapped).Shape())

        return copy.deepcopy(self, memo)


#
# Function wrapper
#


def create_compound(cls, objects, ctx_add=None, mode=bd.Mode.PRIVATE, **kwargs):
    objs = objects if isinstance(objects, (list, tuple)) else [objects]

    if ctx_add is None:
        dim = max([o.dim for o in objs])
    else:
        dim = ctx_add.dim

    if mode is not None:
        kwargs["mode"] = mode

    with CTX[dim]() as ctx:
        if ctx_add is not None:
            ctx._add_to_context(bd.Compound(ctx_add.wrapped))
        compound = cls(*objs, **kwargs)

    return AlgCompound(compound, {}, dim)
