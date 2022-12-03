from typing import List, Union
from .wrappers import AlgCompound, Empty
from .direct_api import *


def tupleize(arg):
    if isinstance(arg, (tuple, list)):
        return tuple(arg)
    else:
        return (arg,)


class Shortcuts:
    @staticmethod
    def planes(objs: List[Union[Plane, Location, Face]]) -> List[Plane]:
        return [Plane(obj) for obj in objs]

    @staticmethod
    def min_solid(a: Compound, axis=Axis.Z) -> Solid:
        return a.solids().sort_by(axis)[0]

    @staticmethod
    def max_solid(a: Compound, axis=Axis.Z) -> Solid:
        return a.solids().sort_by(axis)[-1]

    @staticmethod
    def min_solids(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.solids().group_by(axis)[0]

    @staticmethod
    def max_solids(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.solids().group_by(axis)[-1]

    @staticmethod
    def min_face(a: Compound, axis=Axis.Z) -> Face:
        return a.faces().sort_by(axis)[0]

    @staticmethod
    def max_face(a: Compound, axis=Axis.Z) -> Face:
        return a.faces().sort_by(axis)[-1]

    @staticmethod
    def min_faces(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.faces().group_by(axis)[0]

    @staticmethod
    def max_faces(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.faces().group_by(axis)[-1]

    @staticmethod
    def min_edge(a: Compound, axis=Axis.Z) -> Edge:
        return a.edges().sort_by(axis)[0]

    @staticmethod
    def max_edge(a: Compound, axis=Axis.Z) -> Edge:
        return a.edges().sort_by(axis)[-1]

    @staticmethod
    def min_edges(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.edges().group_by(axis)[0]

    @staticmethod
    def max_edges(a: Compound, axis=Axis.Z) -> ShapeList:
        return a.edges().group_by(axis)[-1]
