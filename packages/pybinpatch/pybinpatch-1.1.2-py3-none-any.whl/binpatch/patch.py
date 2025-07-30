
from .types import Differences
from .utils import getBufferAtIndex, replaceBufferAtIndex


def patchFromDifferences(data: bytearray, differences: Differences) -> bytearray:
    if not isinstance(data, bytearray):
        raise TypeError(f'Data must be of type: {bytearray}')

    for difference in differences:
        buffer = getBufferAtIndex(data, difference.offset, difference.size)

        if buffer != difference.a:
            raise ValueError('A attribute not the same!')

        data = replaceBufferAtIndex(data, difference.b, difference.offset, difference.size)

    return data
