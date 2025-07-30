import math
from matplotlib.patches import Wedge
import matplotlib.pyplot as plt
from FDLib.types import *
from FDLib.utils import *
from .ploy import *

__all__ = ["Arc"]


class Arc(Polygon):
    def __init__(
            self,
            *,
            location: T_Point,
            innerRadius: float,
            outerRadius: float,
            beginAngle: float,
            endAngle: float,
            clockwise: int = 1,
            arc_type: str = "butt",  # TODO: Literal[xxx, yyy]
            metalLayer: str = "mental layer",
            pins: List[str] = None,
            pins_location: List[T_Points] = None,
            vias: List[str] = None,
            net: str = ""
    ):
        assert 0 < innerRadius < outerRadius
        super().__init__(
            location=location,
            pins=pins,
            pins_location=pins_location,
            metalLayer=metalLayer,
            vias=vias,
            net=net
        )
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.beginAngle = (beginAngle * 180 / math.pi) % 360
        self.endAngle = (endAngle * 180 / math.pi) % 360
        self.clockwise = clockwise
        self.arc_type = arc_type

    def __repr__(self) -> "str":
        return (
            f"<Arc:\n"
            f"  location={self.location}, pins={self.pins}, pins_location={self.pins_location}\n"
            f"  metalLayer={self.metalLayer}, vias={self.vias}, net={self.net}\n"
            f"  innerRadius={self.innerRadius}, outerRadius={self.outerRadius}\n"
            f"  beginAngle={self.beginAngle}, endAngle={self.endAngle}\n"
            f"  clockwise={self.clockwise}, arc_type={self.arc_type}\n"
            f">"
        )

    def draw_body(self, axes: plt.Axes):
        # print(f"clock: {self.clockwise}, start: {self.beginAngle}, end: {self.endAngle}")
        if self.clockwise:
            self.beginAngle, self.endAngle = self.endAngle, self.beginAngle
        width = self.outerRadius - self.innerRadius
        patch = Wedge(
            self.location,
            self.outerRadius,
            self.beginAngle,
            self.endAngle,
            width=width,
            color=get_color(self.metalLayer),
            linewidth=0,
            alpha=0.5
        )
        axes.add_patch(patch)

    def draw_net(self, axes: plt.Axes):
        ...
