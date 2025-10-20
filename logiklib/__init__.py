__version__ = "0.1.2"


def register_part_data(fpga, package_name, part_name):
    fpga.set_dataroot(
        package_name,
        f"https://github.com/siliconcompiler/logiklib/releases/download/v{__version__}/{part_name}_cad.tar.gz",
        f'v{__version__}'
    )
