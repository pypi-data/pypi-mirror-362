from typing import List, Tuple, Literal, Union

__all__ = [
    "List", "Tuple", "Literal", "Union",
    "T_Number", "T_Point", "T_Points",
]
T_Number = Union[int, float]
T_Point = Tuple[T_Number, T_Number]
T_Points = List[T_Point]
