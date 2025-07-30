from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from FDLib.types import *
from FDLib.utils import *
from .ploy import *

__all__ = ["Path"]


class Path(Polygon):
    def __init__(
            self,
            *,
            location: T_Points,
            width: float,
            path_type: str,  # TODO: Literal[xxx, yyy]
            corner_type: str,  # TODO: Literal[xxx, yyy]
            metalLayer: str = "mental layer",
            pins: List[str] = None,
            pins_location: List[T_Points] = None,
            vias: List[str] = None,
            net: str = ""
    ):
        super().__init__(
            location=location,
            pins=pins,
            pins_location=pins_location,
            metalLayer=metalLayer,
            vias=vias,
            net=net
        )
        self.width = width
        self.path_type = path_type
        self.corner_type = corner_type

    def __repr__(self) -> "str":
        return (
            f"<Path:\n"
            f"  pins={self.pins}, pins_location={self.pins_location}\n"
            f"  metalLayer={self.metalLayer}, vias={self.vias}, net={self.net}\n"
            f"  width={self.width}, path_type={self.path_type}, corner_type={self.corner_type}\n"
            f"  location={self.location}\n"
            f">"
        )

    def draw_body(self, axes: plt.Axes):
        xs, ys = zip(*self.location)
        line = Line2D(xs, ys, linewidth=self.width, color=get_color(self.metalLayer), alpha=0.5)
        axes.add_line(line)

    def draw_net(self, axes: plt.Axes):
        ...
