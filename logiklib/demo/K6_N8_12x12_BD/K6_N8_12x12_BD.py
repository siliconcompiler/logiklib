# Copyright 2025 Zero ASIC Corporation

from logiklib import register_part_data

from siliconcompiler import FPGA


####################################################
# Setup for K6_N8_12x12_BD FPGA
####################################################
def setup():
    part_name = 'K6_N8_12x12_BD'

    fpga = FPGA(part_name, package=f"logik-fpga-{part_name}")

    register_part_data(fpga, part_name, f"logik-fpga-{part_name}")

    fpga.set('fpga', part_name, 'vendor', 'zeroasic')

    fpga.set('fpga', part_name, 'var', 'vpr_device_code', part_name)

    fpga.set('fpga', part_name, 'lutsize', 6)
    fpga.set('fpga', part_name, 'var', 'feature_set', [
        'async_reset', 'async_set', 'enable'])

    fpga.set('fpga', part_name, 'var', 'vpr_clock_model', 'ideal')

    fpga.set('fpga', part_name, 'file', 'archfile', 'cad/K6_N8_12x12_BD.xml')
    fpga.set('fpga', part_name, 'file', 'graphfile', 'cad/K6_N8_12x12_BD_rr_graph.xml')

    for tool in ('vpr', 'yosys'):
        fpga.set('fpga', part_name, 'var', f'{tool}_registers', [
            'dff', 'dffe', 'dffer', 'dffers', 'dffes', 'dffr', 'dffrs', 'dffs',
            'dsp_mult', 'bram_sp'
        ])

    fpga.set('fpga', part_name, 'file', 'yosys_flop_techmap', 'techlib/tech_flops.v')
    fpga.set('fpga', part_name, 'file', 'yosys_memory_techmap', 'techlib/tech_bram.v')
    fpga.set('fpga', part_name, 'file', 'yosys_memory_libmap', 'techlib/bram_memory_map.txt')
    fpga.set('fpga', part_name, 'file', 'yosys_dsp_techmap', 'techlib/tech_dsp.v')

    # Set the dsp options for the yosys built-in DSP correctly for this
    # architecture
    fpga.set('fpga', part_name, 'var', 'yosys_dsp_options', [
        'DSP_A_MAXWIDTH=18', 'DSP_A_MINWIDTH=2',
        'DSP_B_MAXWIDTH=18', 'DSP_B_MINWIDTH=2',
        'DSP_NAME=_dsp_block_'])

    fpga.set('fpga', part_name, 'var', 'dsp_blackbox_options', 'BLACKBOX_MACROS')

    fpga.set('fpga', part_name, 'file', 'bitstream_map', 'cad/K6_N8_12x12_BD_bitstream_map.json')

    fpga.set('fpga', part_name, 'file', 'constraints_map', 'cad/K6_N8_12x12_BD_constraint_map.json')

    fpga.set('fpga', part_name, 'var', 'channelwidth', 80)

    return fpga


#########################
if __name__ == "__main__":
    fpga = setup()
    assert fpga.check_filepaths()
    fpga.write_manifest(f'{fpga.design}.json')
