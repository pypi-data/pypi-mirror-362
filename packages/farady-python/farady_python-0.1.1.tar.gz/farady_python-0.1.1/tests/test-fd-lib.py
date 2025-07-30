from FDLib import *
import math


class TestArc(FDLibrary):
    def reload(self):
        self.specifications = [
            Arc(
                location=(14, 14),
                innerRadius=10,
                outerRadius=14,
                beginAngle=0,
                endAngle=math.pi / 3,
                clockwise=1,
                arc_type="butt"
            )
        ]


if __name__ == "__main__":
    TestArc().run()
