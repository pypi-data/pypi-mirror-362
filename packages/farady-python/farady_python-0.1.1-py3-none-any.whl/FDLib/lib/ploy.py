from matplotlib.patches import Polygon as PlotPloy, Circle, Rectangle
import matplotlib.pyplot as plt
from FDLib.types import *
from FDLib.utils import *

__all__ = ["Polygon"]


class Polygon:
    def __init__(
            self,
            *,
            location: Union[T_Point, T_Points],
            metalLayer: str = "mental layer",
            pins: List[str] = None,
            pins_location: List[T_Points] = None,
            vias: List[str] = None,
            net: str = ""
    ):
        assert len(location), "location is required"
        self._many = True
        if isinstance(location[0], T_Number):
            self._many = False

        pins = pins or []
        pins_location = pins_location or []
        vias = vias or []

        self.location = location
        self.pins = pins
        self.pins_location = pins_location
        self.metalLayer = metalLayer
        self.vias = vias
        self.net = net

    def __repr__(self) -> "str":
        return (
            f"<Polygon:\n"
            f"  pins={self.pins}, pins_location={self.pins_location}\n"
            f"  metalLayer={self.metalLayer}, vias={self.vias}, net={self.net}\n"
            f"  location={self.location}\n"
            f">"
        )

    def draw_body(self, axes: plt.Axes):
        if not self._many:
            patch = Circle(self.location, radius=2, color="black", fill=True, alpha=0.5, linewidth=0)
        else:
            patch = PlotPloy(self.location, color=get_color(self.metalLayer), fill=True, alpha=0.5, linewidth=0)
        axes.add_patch(patch)
        self.draw_pins(axes)

    def draw_pins(self, axes: plt.Axes):
        side = 5.0
        for locations in self.pins_location:
            for location in locations:
                x, y = location[0] - side / 2, location[1] - side / 2
                patch = Rectangle(
                    (x, y),
                    side, side,
                    angle=45,
                    rotation_point="center",
                    fill=True,
                    facecolor="red",
                    edgecolor="black",
                    alpha=0.5
                )
                axes.add_patch(patch)

    def draw_net(self, axes: plt.Axes):
        ...
