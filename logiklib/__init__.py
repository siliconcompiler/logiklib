__version__ = "0.1.0"


def register_part_data(fpga, package_name, part_name):
    fpga.set_dataroot(
        package_name,
        f"github://siliconcompiler/logiklib/v{__version__}/{part_name}_cad.tar.gz")
