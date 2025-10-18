
from siliconcompiler.tools.vpr import VPRFPGA
from siliconcompiler.tools.yosys import YosysFPGA
from siliconcompiler.tools.opensta import OpenSTAFPGA

from logiklib import register_part_data


####################################################
# Setup for z1062 FPGA
####################################################

class z1062(YosysFPGA, VPRFPGA, OpenSTAFPGA):
    '''
    Logik driver for z1062
    '''

    def __init__(self):
        super().__init__()
        self.set_name('z1062')

        self.define_tool_parameter('convert_bitstream', 'bitstream_map', 'file',
                                   'bitstream map')

        register_part_data(self, "logik-fpga-z1062", 'z1062')

        self.package.set_vendor("fpga_architect")

        self.set_vpr_devicecode("z1062")

        self.set_lutsize(6)
        yosys_featureset = []
        yosys_featureset.append("async_reset")
        yosys_featureset.append("enable")

        self.add_yosys_featureset(yosys_featureset)
        self.set_vpr_clockmodel("route")

        with self.active_dataroot("logik-fpga-z1062"):
            self.set_vpr_archfile('z1062/cad/z1062.xml')
            self.set_vpr_graphfile('z1062/cad/z1062_rr_graph.xml')
            self.set_yosys_config('z1062/cad/z1062_yosys_config.json')
            self.set_yosys_flipfloptechmap('z1062/cad/tech_flops.v')
            self.set_yosys_memorymap(techmap='z1062/cad/tech_bram.v')
            self.set_yosys_memorymap(libmap='z1062/cad/bram_memory_map.txt')
            self.set_yosys_dsptechmap('z1062/cad/tech_dsp.v',
                                      options={'DSP_SIGNEDONLY': '1',
                                               'DSP_A_MAXWIDTH': '18',
                                               'DSP_B_MAXWIDTH': '18',
                                               'DSP_A_MINWIDTH': '2',
                                               'DSP_B_MINWIDTH': '2',
                                               'DSP_Y_MINWIDTH': '2',
                                               'DSP_NAME': '_dsp_block_'})
            self.add_yosys_macrolib('z1062/cad/tech_dsp_blackbox.v')

        # Define the macros that can be techmapped to based on the modes
        # that exist in the design
        self.add_yosys_registertype(['dff',
                                     'dffe',
                                     'dffeh',
                                     'dffehl',
                                     'dffehlr',
                                     'dffehr',
                                     'dffel',
                                     'dffelr',
                                     'dffer',
                                     'dffh',
                                     'dffhl',
                                     'dffhlr',
                                     'dffhr',
                                     'dffl',
                                     'dfflr',
                                     'dffr'])
        self.add_vpr_registertype(['dff',
                                   'dffe',
                                   'dffeh',
                                   'dffehl',
                                   'dffehlr',
                                   'dffehr',
                                   'dffel',
                                   'dffelr',
                                   'dffer',
                                   'dffh',
                                   'dffhl',
                                   'dffhlr',
                                   'dffhr',
                                   'dffl',
                                   'dfflr',
                                   'dffr'])

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

        self.add_yosys_bramtype(['sdpram_1024x16',
                                 'sdpram_16384x1',
                                 'sdpram_2048x8',
                                 'sdpram_4096x4',
                                 'sdpram_8192x2',
                                 'spram_1024x16',
                                 'spram_16384x1',
                                 'spram_2048x8',
                                 'spram_4096x4',
                                 'spram_512x32',
                                 'spram_8192x2',
                                 'sram_sdp',
                                 'sram_sp',
                                 'sram_tdp',
                                 'tdpram_1024x16',
                                 'tdpram_16384x1',
                                 'tdpram_2048x8',
                                 'tdpram_4096x4',
                                 'tdpram_8192x2'])
        self.add_vpr_bramtype(['sdpram_1024x16',
                               'sdpram_16384x1',
                               'sdpram_2048x8',
                               'sdpram_4096x4',
                               'sdpram_8192x2',
                               'spram_1024x16',
                               'spram_16384x1',
                               'spram_2048x8',
                               'spram_4096x4',
                               'spram_512x32',
                               'spram_8192x2',
                               'sram_sdp',
                               'sram_sp',
                               'sram_tdp',
                               'tdpram_1024x16',
                               'tdpram_16384x1',
                               'tdpram_2048x8',
                               'tdpram_4096x4',
                               'tdpram_8192x2'])

        # TODO: blackbox_options

        with self.active_dataroot("logik-fpga-z1062"):
            self.set("tool", "convert_bitstream", "bitstream_map", 'z1062/cad/z1062_bitstream_map.json')
            self.set_vpr_constraintsmap('z1062/cad/z1062_constraint_map.json')

        self.set_vpr_channelwidth(150)

        with self.active_dataroot("logik-fpga-z1062"):
            with self.active_fileset("z1062_opensta_liberty_files"):
                self.add_file('z1062/cad/vtr_primitives.lib')
                self.add_file(['z1062/cad/tech_flops.lib', 'z1062/cad/tech_dsp.lib', 'z1062/cad/tech_bram.lib'])
                self.add_opensta_liberty_fileset()

        self.set_vpr_router_lookahead('classic')


#########################
if __name__ == "__main__":
    fpga = z1062
    assert fpga.check_filepaths()
    fpga.write_manifest(f'{fpga.design}.json')
