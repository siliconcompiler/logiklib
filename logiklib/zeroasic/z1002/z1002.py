
from siliconcompiler.tools.vpr import VPRFPGA
from siliconcompiler.tools.yosys import YosysFPGA
from siliconcompiler.tools.opensta import OpenSTAFPGA

from logiklib import register_part_data


####################################################
# Setup for z1002 FPGA
####################################################

class z1002(YosysFPGA, VPRFPGA, OpenSTAFPGA):
    '''
    Logik driver for z1002
    '''

    def __init__(self):
        super().__init__()
        self.set_name('z1002')

        self.define_tool_parameter('convert_bitstream', 'bitstream_map', 'file',
                                   'bitstream map')

        register_part_data(self, "logik-fpga-z1002", 'z1002')

        self.package.set_vendor("fpga_architect")

        self.set_vpr_devicecode("z1002")

        self.set_lutsize(4)
        yosys_featureset = []
        yosys_featureset.append("async_reset")
        yosys_featureset.append("enable")

        self.add_yosys_featureset(yosys_featureset)
        self.set_vpr_clockmodel("route")

        with self.active_dataroot("logik-fpga-z1002"):
            self.set_vpr_archfile('z1002/cad/z1002.xml')
            self.set_vpr_graphfile('z1002/cad/z1002_rr_graph.xml')
            self.set_yosys_config('z1002/cad/z1002_yosys_config.json')
            self.set_yosys_flipfloptechmap('z1002/cad/tech_flops.v')

        # Define the macros that can be techmapped to based on the modes
        # that exist in the design
        self.add_yosys_registertype(['dff', 'dffe', 'dffer', 'dffr'])
        self.add_vpr_registertype(['dff', 'dffe', 'dffer', 'dffr'])

        self.add_yosys_dsptype(['dsp_mult',
                                'efpga_acc',
                                'efpga_acc_regi',
                                'efpga_adder',
                                'efpga_adder_regi',
                                'efpga_adder_regio',
                                'efpga_adder_rego',
                                'efpga_macc',
                                'efpga_macc_pipe',
                                'efpga_macc_pipe_regi',
                                'efpga_macc_regi',
                                'efpga_mult',
                                'efpga_mult_addc',
                                'efpga_mult_addc_regi',
                                'efpga_mult_addc_regio',
                                'efpga_mult_addc_rego',
                                'efpga_mult_regi',
                                'efpga_mult_regio',
                                'efpga_mult_rego'])
        self.add_vpr_dsptype(['dsp_mult',
                              'efpga_acc',
                              'efpga_acc_regi',
                              'efpga_adder',
                              'efpga_adder_regi',
                              'efpga_adder_regio',
                              'efpga_adder_rego',
                              'efpga_macc',
                              'efpga_macc_pipe',
                              'efpga_macc_pipe_regi',
                              'efpga_macc_regi',
                              'efpga_mult',
                              'efpga_mult_addc',
                              'efpga_mult_addc_regi',
                              'efpga_mult_addc_regio',
                              'efpga_mult_addc_rego',
                              'efpga_mult_regi',
                              'efpga_mult_regio',
                              'efpga_mult_rego'])

        self.add_yosys_bramtype(['sdpram_1024x1',
                                 'sdpram_128x8',
                                 'sdpram_256x4',
                                 'sdpram_512x2',
                                 'spram_1024x1',
                                 'spram_128x8',
                                 'spram_256x4',
                                 'spram_512x2',
                                 'spram_64x16',
                                 'sram_sdp',
                                 'sram_sp',
                                 'sram_tdp',
                                 'tdpram_1024x1',
                                 'tdpram_128x8',
                                 'tdpram_256x4',
                                 'tdpram_512x2'])
        self.add_vpr_bramtype(['sdpram_1024x1',
                               'sdpram_128x8',
                               'sdpram_256x4',
                               'sdpram_512x2',
                               'spram_1024x1',
                               'spram_128x8',
                               'spram_256x4',
                               'spram_512x2',
                               'spram_64x16',
                               'sram_sdp',
                               'sram_sp',
                               'sram_tdp',
                               'tdpram_1024x1',
                               'tdpram_128x8',
                               'tdpram_256x4',
                               'tdpram_512x2'])

        # TODO: blackbox_options

        with self.active_dataroot("logik-fpga-z1002"):
            self.set("tool", "convert_bitstream", "bitstream_map", 'z1002/cad/z1002_bitstream_map.json')
            self.set_vpr_constraintsmap('z1002/cad/z1002_constraint_map.json')

        self.set_vpr_channelwidth(150)

        with self.active_dataroot("logik-fpga-z1002"):
            with self.active_fileset("z1002_opensta_liberty_files"):
                self.add_file('z1002/cad/vtr_primitives.lib')
                self.add_file(['z1002/cad/tech_flops.lib'])
                self.add_opensta_liberty_fileset()

        self.set_vpr_router_lookahead('classic')


#########################
if __name__ == "__main__":
    fpga = z1002
    assert fpga.check_filepaths()
    fpga.write_manifest(f'{fpga.design}.json')
