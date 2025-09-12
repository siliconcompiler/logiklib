__version__ = "0.1.2"


def register_part_data(fpga, part_name, package_name):
    fpga.register_source(
        package_name,
        f"github://siliconcompiler/logiklib/v{__version__}/{part_name}_cad.tar.gz",
        f"v{__version__}")
