from .base import FDBase

__all__ = ["FDLumpedElement"]


class FDLumpedElement(FDBase):
    def __init__(self):
        self.spice = []

    def __repr__(self):
        inner = "\n  ".join(self.spice)
        return f"<FDLumpedElement:\n{inner}\n>"

    def show(self):
        print(repr(self))
