
from dataclasses import dataclass


@dataclass
class Difference:
    a: bytes
    b: bytes
    offset: int
    size: int


Differences = list[Difference]
