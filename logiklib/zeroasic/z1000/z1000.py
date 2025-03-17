# Copyright 2025 Zero ASIC Corporation
# Licensed under the Apache 2.0 License (see LICENSE for details)

from logiklib import register_part_data

from siliconcompiler import FPGA


####################################################
# Setup for z1000 FPGA
####################################################
def setup():
    '''
    z1000 is the first in a series of open FPGA architectures.
    The baseline z1000 part is an architecture with 2K LUTs
    and no hard macros.
    '''

    part_name = 'z1000'

    fpga = FPGA(part_name, package=f"zeroasic-efpga-{part_name}")

    register_part_data(fpga, part_name, f"zeroasic-efpga-{part_name}")

    fpga.set('fpga', part_name, 'vendor', 'zeroasic')

    # Set a variable for VPR to use to detect the correct <fixed_layout> section
    # of the architecture XML file
    fpga.set('fpga', part_name, 'var', 'vpr_device_code', part_name)

    fpga.set('fpga', part_name, 'lutsize', 4)
    fpga.set('fpga', part_name, 'var', 'feature_set', [
        'async_reset', 'enable'])

    fpga.set('fpga', part_name, 'var', 'vpr_clock_model', 'route')

    fpga.set('fpga', part_name, 'file', 'archfile',  f'cad/{part_name}.xml')
    fpga.set('fpga', part_name, 'file', 'graphfile', f'cad/{part_name}_rr_graph.xml')

    for tool in ('vpr', 'yosys'):
        fpga.set('fpga', part_name, 'var', f'{tool}_registers', [
            'dff',
            'dffr',
            'dffe',
            'dffer'])

    fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', 'techlib/tech_flops.v')

    fpga.set('fpga', part_name, 'file', 'bitstream_map', f'cad/{part_name}_bitstream_map.json')

    fpga.set('fpga', part_name, 'file', 'constraints_map', f'cad/{part_name}_constraint_map.json')

    fpga.set('fpga', part_name, 'var', 'channelwidth', 100)

    return fpga


#########################
if __name__ == "__main__":
    fpga = setup()
    fpga.write_manifest(f'{fpga.design}.json')
