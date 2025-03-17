# Copyright 2024 Zero ASIC Corporation

from logiklib import register_part_data

from siliconcompiler import FPGA


####################################################
# Setup for K4_N8_6x6 FPGA
####################################################
def setup():
    part_name = 'K4_N8_6x6'

    fpga = FPGA(part_name, package=f"logik-fpga-{part_name}")

    register_part_data(fpga, part_name, f"logik-fpga-{part_name}")

    fpga.set('fpga', part_name, 'vendor', 'zeroasic')

    fpga.set('fpga', part_name, 'var', 'vpr_device_code', 'K4_N8_6x6')

    fpga.set('fpga', part_name, 'lutsize', 4)

    fpga.set('fpga', part_name, 'var', 'vpr_clock_model', 'ideal')

    fpga.set('fpga', part_name, 'file', 'archfile', 'cad/K4_N8_6x6.xml')
    fpga.set('fpga', part_name, 'file', 'graphfile', 'cad/K4_N8_6x6_rr_graph.xml')

    for tool in ('vpr', 'yosys'):
        fpga.set('fpga', part_name, 'var', f'{tool}_registers', 'dff')

    fpga.set('fpga', part_name, 'file', 'bitstream_map', 'cad/K4_N8_6x6_bitstream_map.json')

    fpga.set('fpga', part_name, 'file', 'constraints_map', 'cad/K4_N8_6x6_constraint_map.json')

    fpga.set('fpga', part_name, 'var', 'channelwidth', 50)

    return fpga


#########################
if __name__ == "__main__":
    fpga = setup()
    assert fpga.check_filepaths()
    fpga.write_manifest(f'{fpga.design}.json')
