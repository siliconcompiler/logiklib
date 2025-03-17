# Copyright 2024 Zero ASIC Corporation

from logiklib import register_part_data

from siliconcompiler import FPGA


####################################################
# Setup for K6_N8_3x3 FPGA
####################################################
def setup():
    part_name = 'K6_N8_3x3'

    fpga = FPGA(part_name, package=f"logik-fpga-{part_name}")

    register_part_data(fpga, part_name, f"logik-fpga-{part_name}")

    fpga.set('fpga', part_name, 'vendor', 'zeroasic')

    fpga.set('fpga', part_name, 'var', 'vpr_device_code', 'K6_N8_3x3')

    fpga.set('fpga', part_name, 'lutsize', 6)

    fpga.set('fpga', part_name, 'var', 'vpr_clock_model', 'ideal')

    fpga.set('fpga', part_name, 'file', 'archfile', 'cad/K6_N8_3x3.xml')
    fpga.set('fpga', part_name, 'file', 'graphfile', 'cad/K6_N8_3x3_rr_graph.xml')

    for tool in ('vpr', 'yosys'):
        fpga.set('fpga', part_name, 'var', f'{tool}_registers', 'dff')

    fpga.set('fpga', part_name, 'file', 'bitstream_map', 'cad/K6_N8_3x3_bitstream_map.json')

    fpga.set('fpga', part_name, 'file', 'constraints_map', 'cad/K6_N8_3x3_constraint_map.json')

    fpga.set('fpga', part_name, 'var', 'channelwidth', 40)

    return fpga


#########################
if __name__ == "__main__":
    fpga = setup()
    assert fpga.check_filepaths()
    fpga.write_manifest(f'{fpga.design}.json')
