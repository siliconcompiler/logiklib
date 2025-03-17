import os
import pytest

from siliconcompiler import Chip

import logiklib
from logiklib.demo.K6_N8_3x3 import K6_N8_3x3
from logiklib.demo.K4_N8_6x6 import K4_N8_6x6
from logiklib.demo.K6_N8_12x12_BD import K6_N8_12x12_BD
from logiklib.demo.K6_N8_28x28_BD import K6_N8_28x28_BD
from logiklib.zeroasic.z1000 import z1000


all_modules = (K6_N8_3x3,
               K4_N8_6x6,
               K6_N8_12x12_BD,
               K6_N8_28x28_BD,
               z1000)


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


@pytest.mark.parametrize("module", all_modules)
def test_filepaths(module):
    '''
    Loads a module and ensures their filepaths are available
    '''
    chip = Chip('<test>')
    chip.use(module)

    assert chip.check_filepaths()
