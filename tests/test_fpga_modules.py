import os
import pytest

import siliconcompiler
from siliconcompiler import Design
from siliconcompiler import Project

import logiklib
# from logiklib.zeroasic.z1000 import z1000 as z1000_driver
from logiklib.zeroasic.z1000.z1000 import z1000
# from logiklib.zeroasic.z1002.z1002 import z1002
# from logiklib.zeroasic.z1010.z1010 import z1010
# from logiklib.zeroasic.z1012.z1012 import z1012
# from logiklib.zeroasic.z1060.z1060 import z1060
# from logiklib.zeroasic.z1062.z1062 import z1062


#all_modules = (z1000_driver,
               #z1002_driver,
               #z1010_driver,
               #z1012_driver,
               #z1060_driver,
               #z1062_driver
#               )

all_parts = (z1000,
               #z1002,
               #z1010,
               #z1012,
               #z1060,
               #z1062
               )


@pytest.mark.skip(reason="importing classes instead of modules right now")
def test_all_modules():
    '''
    Test to ensure all available modules are in the testing list
    '''
    base_dir = os.path.abspath(os.path.dirname(logiklib.__file__))
    found_modules = []
    for pathdir, _, files in os.walk(base_dir):
        if len(os.path.relpath(pathdir, base_dir).split("/")) == 2:
            for f in files:
                if f != "__init__.py" and f.endswith(".py"):
                    found_modules.append(os.path.join(pathdir, f))

    assert set(found_modules) == set([mod.__file__ for mod in all_modules])


@pytest.mark.parametrize("part", all_parts)
def test_filepaths(part):
    fpga = part()

    assert fpga.name == fpga.__class__.__name__
