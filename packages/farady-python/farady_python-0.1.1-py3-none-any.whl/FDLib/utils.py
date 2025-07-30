from matplotlib.transforms import Bbox
from matplotlib.pyplot import Axes
import hashlib
from .types import *

__all__ = ["get_color", "color_maker", "autoscale_axes"]


def get_color(s: str) -> str:
    digest = hashlib.md5(s.encode()).hexdigest()
    return f"#{digest[:6]}"


def color_maker():
    colors = {}

    def inner(s: str) -> str:
        if s not in colors:
            colors[s] = get_color(s)
        return colors[s]

    return inner


def autoscale_axes(axes: Axes, margin: float = 0.05):
    # 强制绘制一次，以便每个 Artist 都能生成 window_extent
    axes.figure.canvas.draw()

    bboxes = []
    renderer = axes.figure.canvas.get_renderer()
    for art in axes.get_children():
        try:
            bb = art.get_window_extent(renderer)
        except Exception:  # noqa
            continue
        if bb.width == 0 or bb.height == 0:
            continue
        bboxes.append(bb)

    if not bboxes:
        return

    # 合并所有 display 坐标下的包围盒
    disp_bbox = Bbox.union(bboxes)
    # 转回 data 坐标
    inv = axes.transData.inverted()
    (xmin, ymin), (xmax, ymax) = inv.transform(disp_bbox.get_points()).reshape(2, 2)

    dx, dy = xmax - xmin, ymax - ymin
    axes.set_xlim(xmin - dx * margin, xmax + dx * margin)
    axes.set_ylim(ymin - dy * margin, ymax + dy * margin)
