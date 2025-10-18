import pytest

from logiklib.zeroasic.z1000.z1000 import z1000
from logiklib.zeroasic.z1002.z1002 import z1002
from logiklib.zeroasic.z1010.z1010 import z1010
from logiklib.zeroasic.z1012.z1012 import z1012
from logiklib.zeroasic.z1060.z1060 import z1060
from logiklib.zeroasic.z1062.z1062 import z1062


all_parts = (z1000,
             z1002,
             z1010,
             z1012,
             z1060,
             z1062
             )


@pytest.mark.parametrize("part", all_parts)
def test_filepaths(part):
    fpga = part()

    assert fpga.name == fpga.__class__.__name__
