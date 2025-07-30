from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle as PlotRect
from .ploy import *
from FDLib.types import *
from FDLib.utils import *

__all__ = ["Rectangle"]


class Rectangle(Polygon):
    def __init__(
            self,
            *,
            location: T_Point,
            width: T_Number,
            height: T_Number,
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
        self.height = height

    def draw_body(self, axes: plt.Axes):
        patch = PlotRect(
            self.location,
            self.width,
            self.height,
            linewidth=0,
            color=get_color(self.metalLayer),
            alpha=0.5
        )
        axes.add_patch(patch)

    def draw_net(self, axes: plt.Axes):
        ...
