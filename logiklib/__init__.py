__version__ = "0.1.0"


def register_part_data(fpga, part_name, package_name):
    fpga.register_source(
        package_name,
        f"github://siliconcompiler/logiklib/v{__version__}/{part_name}_cad.tar.gz",
        f"v{__version__}")


def setup():
    from .demo import setup as demo_setup
    from .zeroasic import setup as zeroasic_setup

    return [
        *demo_setup(),
        *zeroasic_setup()
    ]
