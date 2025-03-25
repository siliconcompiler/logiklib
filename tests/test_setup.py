import logiklib

from siliconcompiler import Chip


def test_logiklib_setup():
    chip = Chip('')

    pre_load = len(chip.getkeys('fpga'))

    chip.use(logiklib)

    assert len(chip.getkeys('fpga')) == 5 + pre_load
