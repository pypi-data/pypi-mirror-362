import matplotlib.pyplot as plt
from .base import FDBase
from FDLib.lib.ploy import *
from FDLib.utils import autoscale_axes

__all__ = ["FDLibrary"]


class FDLibrary(FDBase):
    def __init__(self):
        self.specifications: list[Polygon] = []

    def __repr__(self):
        inner = [repr(one) for one in self.specifications]
        children = "\n\n".join(inner)
        return f"<FDLibrary:\n{children}\n>"

    def show(self):
        fig, axes = plt.subplots()
        fig.set_size_inches(8, 8)
        axes.set_title("Result")
        for one in self.specifications:
            one.draw_body(axes)
            one.draw_pins(axes)
            one.draw_net(axes)
        autoscale_axes(axes)
        plt.show()
