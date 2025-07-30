# -*- coding: utf-8 -*-
import math
from FDLib import *


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def rot(self, angle):
        res = Point(self.x, self.y)
        res.x = self.x * math.cos(angle) - self.y * math.sin(angle)
        res.y = self.x * math.sin(angle) + self.y * math.cos(angle)
        return res

    def offset(self, dx=0, dy=0):
        return Point(self.x + dx, self.y + dy)

    def val(self):
        return self.x, self.y


class Line:
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2

    def intersects(self, line):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x3, y3 = line.p1.x, line.p1.y
        x4, y4 = line.p2.x, line.p2.y

        _k = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if _k == 0:
            return None

        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / _k
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / _k

        return Point(x, y)


class Eight:
    _radio_8 = math.tan(math.pi / 8)

    def __init__(self, side, width):
        short_x, long_x = side, side + width
        short_y, long_y = side * self._radio_8, long_x * self._radio_8
        # inner points
        self.ips = [
            Point(short_y, -short_x),
            Point(short_x, -short_y),
            Point(short_x, short_y),
            Point(short_y, short_x),
            Point(-short_y, short_x),
            Point(-short_x, short_y),
            Point(-short_x, -short_y),
            Point(-short_y, -short_x)
        ]
        # outer points
        ops = [
            Point(long_y, -long_x),
            Point(long_x, -long_y),
            Point(long_x, long_y),
            Point(long_y, long_x),
            Point(-long_y, long_x),
            Point(-long_x, long_y),
            Point(-long_x, -long_y),
            Point(-long_y, -long_x)
        ]
        self.ops = ops[::-1]

        self.opi, self.opo = [], []

    def rot(self, angle):
        self.ips = [p.rot(angle) for p in self.ips]
        self.ops = [p.rot(angle) for p in self.ops]
        self.opi = [p.rot(angle) for p in self.opi]
        self.opo = [p.rot(angle) for p in self.opo]


class EightEdge(FDLibrary):
    metalLayers = ["Metal Layer"]
    Parameters = {
        "Inner": 40, "Width": 5, "Gap": 8,
        "Upper": 10, "Gate": 8, "Plus": 4, "Feet": 10,
        "Offset": 4
    }

    # plus是什么
    def option_e1e3(self, e1, e3):
        half = self.Upper / 2
        joint = self.line_joint_e1e3(e1, e3)
        # joint = self.edge_joint_e1e3(e1.ops[3].y)

        # e1 optional inner
        e1.opi = [Point(half, e1.ips[3].y), Point(-half, e1.ips[3].y)]
        # e1 optional outer
        e1.opo = [
            joint.offset(dx=-2 * joint.x),
            Point(-half, e1.ops[3].y),
            Point(half, e1.ops[3].y),
            joint
        ]
        # e3
        ix = self.Gate / 2 + self.Width + self.Plus
        idy = -self.Width - self.Feet
        ip2 = Point(ix, e3.ips[0].y)
        ip1 = ip2.offset(dy=idy)
        ip3 = Point(-ix, e3.ips[-1].y)
        ip4 = ip3.offset(dy=idy)
        e3.opi = [
            ip1, ip2,
            Point(joint.x, e3.ips[3].y),
            Point(half, e3.ips[3].y),
            Point(-half, e3.ips[3].y),
            Point(-joint.x, e3.ips[3].y),
            ip3, ip4
        ]
        ox = self.Gate / 2 + self.Width * 2 + self.Plus
        ody = -self.Feet
        op2 = Point(-ox, e3.ops[-1].y)
        op1 = op2.offset(dy=ody)
        op3 = Point(ox, e3.ops[0].y)
        op4 = op3.offset(dy=ody)
        e3.opo = [
            op1, op2,
            Point(-half, e3.ops[3].y),
            Point(half, e3.ops[3].y),
            op3, op4
        ]

    def option_e2(self, e2):
        half_upper = self.Upper / 2
        half = self.Gate / 2
        idy = self.Width * -2 - self.Gap - self.Feet
        ip2 = Point(half, e2.ips[0].y)
        ip1 = ip2.offset(dy=idy)
        ip3 = Point(-half, e2.ips[-1].y)
        ip4 = ip3.offset(dy=idy)
        e2.opi = [
            ip1, ip2,
            Point(half_upper, e2.ips[3].y),
            Point(-half_upper, e2.ips[3].y),
            ip3, ip4
        ]

        ody = -self.Width - self.Gap - self.Feet
        op2 = Point(-half - self.Width, e2.ops[-1].y)
        op1 = op2.offset(dy=ody)
        op3 = Point(half + self.Width, e2.ops[0].y)
        op4 = op3.offset(dy=ody)
        e2.opo = [
            op1, op2,
            Point(-half_upper, e2.ops[3].y),
            Point(half_upper, e2.ops[3].y),
            op3, op4
        ]

    def line_joint_e1e3(self, e1, e3):
        half = self.Upper / 2
        l1 = self.Gap + self.Width * 2
        l2 = self.Upper
        l3 = math.sqrt(l1 * l1 + l2 * l2)
        edge1 = math.asin(self.Width / l3)
        edge2 = math.asin(l1 / l3)
        edge3 = math.pi / 2 - (edge2 - edge1)
        dx, dy = self.Width * math.cos(edge3), self.Width * math.sin(edge3)
        p1s, p3s = Point(half, e1.ips[3].y), Point(-half, e3.ops[3].y)
        kp1 = p1s.offset(dx, dy)
        # e1-outer-top && (\)k-line-upper
        line1, line2 = Line(kp1, p3s), Line(e1.ops[3], e1.ops[4])

        return line1.intersects(line2)

    def edge_joint_e1e3(self, e1o3y):
        H = self.Gap + self.Width * 2
        W = self.Upper
        L = math.sqrt(H * H + W * W)
        edge1 = math.asin(W / L)
        edge2 = math.asin(self.Width / L)
        dx = math.tan(edge1 + edge2) * (self.Gap + self.Width)

        return Point(dx - self.Upper / 2, e1o3y)

    def get_e1e3_right(self, e1, e3):
        half = self.Offset / 2
        # go
        points = e3.opi[0:2]
        points.extend(e3.ips[0:4])
        points.extend([e3.opi[2], e1.opi[1]])
        points.extend(e1.ips[4:8])
        points.extend(e1.ips[0:4])
        # |back
        points.extend([
            e1.opo[3].offset(dx=half, dy=-self.Width),
            e1.opo[3].offset(dx=half)
        ])
        points.extend(e1.ops[4:8])
        points.extend(e1.ops[0:4])
        points.extend([e1.opo[0], e3.opo[3]])
        points.extend(e3.ops[4:8])
        points.extend(e3.opo[4:6])
        points.append(e3.opi[0])

        return [itr.val() for itr in points]

    def get_e1e3_left(self, e3):
        start = e3.opi[5].offset(dx=-self.Offset / 2)
        # go
        points = [start]
        points.extend(e3.ips[4:8])
        points.extend(e3.opi[6:8])
        # back
        points.extend(e3.opo[0:2])
        points.extend(e3.ops[0:4])
        points.extend([start.offset(dy=self.Width), start])

        return [itr.val() for itr in points]

    def get_e1e3_bridge(self, e1, e3):
        offset = self.Offset * 1.5
        points = [
            e1.opo[3].offset(dx=offset),  # A
            e1.opo[3],  # B
            e3.opo[2],  # C
            Point(e3.opi[5].x - offset, e3.opo[2].y),  # D
            e3.opi[5].offset(dx=-offset),  # E
            e3.opi[5],  # F
            e1.opi[0],  # G
            Point(e1.opo[3].x + offset, e1.opi[1].y),  # H
            e1.opo[3].offset(dx=offset)  # A
        ]

        return [itr.val() for itr in points]

    def get_e1e3_support(self, e1, e3):
        A = e3.opi[5].offset(dx=-self.Offset / 2)
        B = A.offset(dy=self.Width)
        C = B.offset(dx=-self.Offset)
        D = C.offset(dy=-self.Width)
        rect1 = [itr.val() for itr in [A, B, C, D, A]]

        E = e1.opo[3].offset(dx=self.Offset / 2)
        F = E.offset(dx=self.Offset)
        G = F.offset(dy=-self.Width)
        H = G.offset(dx=-self.Offset)
        rect2 = [itr.val() for itr in [E, F, G, H, E]]

        return rect1, rect2

    @staticmethod
    def get_e2_right(e2):
        points = e2.opi[0:2]
        points.extend(e2.ips[0:4])
        points.extend([e2.opi[2], e2.opo[3]])
        points.extend(e2.ops[4:8])
        points.extend(e2.opo[4:6])
        points.append(e2.opi[0])

        return [itr.val() for itr in points]

    @staticmethod
    def get_e2_left(e2):
        points = [e2.opi[3]]
        points.extend(e2.ips[4:8])
        points.extend(e2.opi[4:6])
        points.extend(e2.opo[0:2])
        points.extend(e2.ops[0:4])
        points.extend([e2.opo[2], e2.opi[3]])

        return [itr.val() for itr in points]

    def get_e2_bridge(self, e2):
        points = [
            e2.opi[2].offset(dx=self.Offset),
            e2.opi[3].offset(dx=-self.Offset),
            e2.opo[2].offset(dx=-self.Offset),
            e2.opo[3].offset(dx=self.Offset),
            e2.opi[2].offset(dx=self.Offset)
        ]

        return [itr.val() for itr in points]

    def get_e2_support(self, e2):
        A = e2.opi[2]
        B = e2.opo[3]
        C = B.offset(dx=self.Offset)
        D = A.offset(dx=self.Offset)
        rect1 = [itr.val() for itr in [A, B, C, D, A]]

        E = e2.opi[3]
        F = e2.opo[2]
        G = F.offset(dx=-self.Offset)
        H = E.offset(dx=-self.Offset)
        rect2 = [itr.val() for itr in [E, F, G, H, E]]

        return rect1, rect2

    def check_param(self):
        for k in self.Parameters:
            v = getattr(self, k)
            assert v > 0, "{0} = {1} should bigger than 0".format(k, v)

    def reload(self):
        self.check_param()

        # 分别拿到三个八边形的基础信息
        eight1 = Eight(self.Inner + (self.Width + self.Gap) * 0, self.Width)
        # eight1.rot(math.pi / 2)
        # self.specifications = [
        #     Polygon(
        #         location=[p.val() for p in eight1.ips] + [p.val() for p in eight1.ops],
        #         pins=[],
        #         pins_location=[],
        #         metalLayer=self.metalLayers[0],
        #         vias=[],
        #         net=""
        #     )
        # ]
        low = self.Upper / 2 + self.Offset
        if low >= eight1.ips[0].x:
            msg = "Param: \"Upper/2 + Offset\" = {0} >= {1}, try to raise \"Inner\"".format(low, eight1.ips[0].x)
            assert False, msg

        eight2 = Eight(self.Inner + (self.Width + self.Gap) * 1, self.Width)
        gaw = self.Gate / 2 + self.Width
        if gaw >= eight2.ops[-1].x:
            msg = "Param: \"Gate/2 + Width\" = {0} >= {1}, try to raise \"Inner\"".format(gaw, eight2.ops[-1].x)
            assert False, msg

        eight3 = Eight(self.Inner + (self.Width + self.Gap) * 2, self.Width)
        ga2w = self.Gate / 2 + 2 * self.Width + self.Plus
        if ga2w >= eight3.ops[-1].x:
            msg = "Param: \"Gate/2 + 2*Width + Plus\" = {0} >= {1}, try to raise \"Inner\"".format(ga2w,
                                                                                                   eight3.ops[-1].x)
            assert False, msg

        # e2没斜线，好算，也就是下边的两个脚脚要算
        self.option_e2(eight2)
        # 重点是这个斜线，涉及e1+e3
        self.option_e1e3(eight1, eight3)

        offset = eight1.opo[3].x + self.Offset * 1.5
        if offset >= eight1.ips[3].x:
            raise RuntimeError("Param: \"Offset\" is too big")

        e1e3_support = self.get_e1e3_support(eight1, eight3)
        e2_support = self.get_e2_support(eight2)

        self.specifications = [
            Polygon(
                location=self.get_e1e3_right(eight1, eight3),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=self.get_e1e3_left(eight3),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=self.get_e1e3_bridge(eight1, eight3),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=self.get_e2_right(eight2),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=self.get_e2_left(eight2),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=self.get_e2_bridge(eight2),
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=e1e3_support[0],
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=e1e3_support[1],
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=e2_support[0],
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            ),
            Polygon(
                location=e2_support[1],
                pins=[],
                pins_location=[],
                metalLayer=self.metalLayers[0],
                vias=[],
                net=""
            )
        ]


if __name__ == "__main__":
    EightEdge().run()
