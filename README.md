# Logiklib

The Logiklib repo is a library of open FPGA architecture descriptions compatible with the Logik FPGA tools.

# Installation:

## User Installation

```sh
    python3 -m pip install --upgrade logiklib
```

## Developer Installation

```sh
    git clone https://github.com/siliconcompiler/logiklib.git
    cd logiklib
    python3 -m pip install .

```

# Repository Organization

Logiklib is organized as a Python package of documented FPGA parts and their Logik part drivers.  The package is backed by release assets for each part that house any CAD data files required by a given part driver.

Currently, all part drivers support the same RTL-to-bitstream flow in Logik, which consists of the following steps:

* Logic synthesis (Yosys)
* FPGA placement (VPR)
* FPGA routing (VPR)
* Bitstream generation (genfasm)
* Bitstream finishing (fasm_to_bitstream)

Each of these steps requires certain data files to be specified in the part driver and available in the part's release asset.  The data files and their requirements are discussed in a later section.

# Contributing

To contribute a part to the library:

1. Review the logiklib/z1000 example
2. Create a folder in logiklib/<vendor_name>/<part_name>, where <vendor_name> is the name of the FPGA manufacturer and <part_name> is the name of your part.
3. Add a .json file describing the architecture
4. Add a .py file driver to be used by Logik
5. Add a /doc folder with descriptions and diagrams describing the architecture
6. Contact Zero ASIC to arrange delivery of a tarball containing all required CAD data files for the architecture and its flow.  The tarball must be named <part_name>_cad.tar.gz.

> **_NOTE:_**  Do not include a CAD data file tarball in a pull request.  The pull request will be rejected.

The section below describes CAD file tarball requirements.

# CAD File Tarball Requirements

Each FPGA in logiklib requires associated CAD files to support the Logik flow used by that FPGA.  When a part makes use of a given EDA software tool for a given step, the data files that the tool requires for that step must be specified correctly in the part driver and included in the part's release asset.  

The required data files are as follows:

* [Yosys technology library files](#yosys_techlib)
* [VPR architecture XML file](#vpr_arch_xml)
* [VPR routing graph XML file](#vpr_rr_graph_xml)
* [Bitstream map file (JSON)](#bitstream_map)
* [Constraint map file (JSON)](#constraint_map)

The following subsections detail the different data files that may be required for an FPGA part's release asset, which steps in the Logik flow graph they support, and how they are composed.

<a id="yosys_techlib"></a>
## Yosys Technology Library files

**Requiring Tool**:  Yosys

**Requiring Step(s)**:  syn

Yosys technology library files are required for any FPGA that contains hard macros to be emitted in the output netlist.  Typically, at least one technology library file is required for the part's flip-flop primitives.  If the part contains hard multipliers or memories, these also require technology library files.

Technology library files are specified as Verilog modules.  For memories, an additional plain text memory map file is also required.

As a guide to preparing these files, it is useful to consult Yosys documentation with examples of how technology mapping is performed.  This is available at https://yosyshq.readthedocs.io/projects/yosys/en/latest/yosys_internals/techmap.html.  For details specific to memory mapping, see https://yosyshq.readthedocs.io/projects/yosys/en/latest/using_yosys/synthesis/memory.html.

An example set of technology library files built directly into Yosys can be reviewed at https://github.com/YosysHQ/yosys/tree/main/techlibs/ice40

<a id="vpr_arch_xml"></a>
## Architecture XML file

**Requiring Tool**:  VPR

**Requiring Step(s)**:  place, route, bitstream generation

VPR encapsulates its model of an FPGA in an XML-based "architecture file".  The architecture file is comprised of several subsections, each of which is encapsulated by a particular top-level XML tag.  Most top-level XML tags are summarized here to provide an overview of the type of architecture information that must be provided in order to furnish a complete model.  Additional top-level tags may be required to handle specific architecture description requirements.  For complete documentation of VPR's architecture XML format, please consult https://docs.verilogtorouting.org/en/latest/arch/.

### Models Section

The models section of the XML file enumerates the hard macros that may appear in the input netlist.  For each model type, a model name and port list is specified.  For each port in the port list, certain port properties are specified to guide the placement and routing steps.  These port properties include but may not be limited to the port direction, whether the port is a clock, and whether the port is timed relative to a clock port in the model or not.

### Layout Section

The `<layout>` section of the XML file specifies how elements of the FPGA are assembled into an array.  For example, if an array is comprised of lookup tables (LUTs), DSP blocks, and memories, the layout section contains enough information for VPR to construct an (X,Y) coordinate system within which to specify the array size and which logic block type is present at each (X,Y) location in the array.  Support for a variety of shorthand methods of specifying this information are available.  However, these shorthand methods are not compatible with genfasm-based bitstream generation.  To correctly uniquify each array element in the FPGA for bitstream generation, the layout section must be specified using `<single>` tags to enumerate each element and its array location individually.  The beginning of a mock FPGA's `<layout>` section that correctly supports genfasm is shown below for illustration:

```
<layout>
    <fixed_layout name="baby_fpga" width="8" height="8">
        <single type="clock_iob" priority="10" x="1" y="1">
            <metadata>
                <meta name="fasm_prefix">baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_0 baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_1</meta>
            </metadata>
        </single>
        <single type="iob_left" priority="5" x="1" y="2">
            <metadata>
                <meta name="fasm_prefix">baby_fpga.tile_iob_left_sb_3_cb_0_1_2.iob_left_0_0.iopad_wrapper_0 baby_fpga.tile_iob_left_sb_3_cb_0_1_2.iob_left_0_0.iopad_wrapper_1 baby_fpga.tile_iob_left_sb_3_cb_0_1_2.iob_left_0_0.iopad_wrapper_2 baby_fpga.tile_iob_left_sb_3_cb_0_1_2.iob_left_0_0.iopad_wrapper_3</meta>
            </metadata>
        </single>
```

The first `<single>` tag specifies that a block of type "clock_iob" is located at array location (1, 1).  Its metadata specifies a list of prefixes for FASM features that map to the ordered list of block instances within the "clock_iob" block.  In the case of this block, there are two instances.  The first has prefix "baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_0" and the second has prefix "baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_1".

### Tiles section

The `<tiles>` section of the XML file provides supplemental information about array element (or "tile") contents to link the layout section (see above) to the complexblocklist section (see below).  This allows the XML file author to fill in gaps in information about the relationship between the physical construction of the array and the logical definitions of each block type provided in the `<complexblocklist>` section.

A common need for this type of specification is correctly constructing a model for an FPGA's I/O blocks (IOBs).  In a physical implementation, multiple I/O blocks per (X,Y) location are typically provided, but each must be distinguishable for the purposes of specifying pin constraints.  Additionally, unique physical tile types are frequently defined to differentiate the four sides of the array, but the underlying IOB within each tile type is the same.  The equivalence must be specified to allow the FPGA placement step to treat the IOBs on all four sides as equivalent to one another.

For a mock FPGA architecture, the resulting XML code that addresses these two issues is shown below for an I/O tile that contains two IOBs.  The enumeration of each IOB as a unique "sub_tile" enables differentiation when processing pin constraints.  The `<equivalent_sites>` tags map each sub_tile type to the same block named "iopad_wrapper" in the complexblocklist section.  Replicating the code below for tile types on the right, top and bottom sides and replacing "iob_left" with "iob_right", "iob_top" and "iob_bottom" allows VPR to treat all IOBs as equivalent during placement.

```
<tile name="iob_left" width="1" height="1" area="0.0">
    <input name="outpad_west" num_pins="4"/>
    <output name="inpad_east" num_pins="4"/>
    <sub_tile name="iopad_wrapper_0">
        <input name="outpad" num_pins="1"/>
        <output name="inpad" num_pins="1"/>
        <pinlocations pattern="custom">
            <loc side="left" xoffset="0" yoffset="0"/>
            <loc side="right" xoffset="0" yoffset="0">iopad_wrapper_0.outpad iopad_wrapper_0.inpad</loc>
            <loc side="top" xoffset="0" yoffset="0"/>
            <loc side="bottom" xoffset="0" yoffset="0"/>
        </pinlocations>
        <fc in_type="frac" in_val="0.125" out_type="frac" out_val="0.125"/>
        <equivalent_sites>
            <site pb_type="iopad_wrapper" pin_mapping="direct"/>
        </equivalent_sites>
    </sub_tile>
    <sub_tile name="iopad_wrapper_1">
        <input name="outpad" num_pins="1"/>
        <output name="inpad" num_pins="1"/>
        <pinlocations pattern="custom">
            <loc side="left" xoffset="0" yoffset="0"/>
            <loc side="right" xoffset="0" yoffset="0">iopad_wrapper_1.outpad iopad_wrapper_1.inpad</loc>
            <loc side="top" xoffset="0" yoffset="0"/>
            <loc side="bottom" xoffset="0" yoffset="0"/>
        </pinlocations>
        <fc in_type="frac" in_val="0.125" out_type="frac" out_val="0.125"/>
        <equivalent_sites>
            <site pb_type="iopad_wrapper" pin_mapping="direct"/>
        </equivalent_sites>
    </sub_tile>
</tile>
```

### Device section

The `<device>` section of the XML file enables specification for certain global properties of the FPGA.  These properties span a variety of topics, ranging from global variables that assist VPR in physically modeling the FPGA to specifying defaults and global parameters for the FPGA interconnect.  Consult 
https://docs.verilogtorouting.org/en/latest/arch/reference/#fpga-device-information for details.

### Switchlist section

The `<switchlist>` section enumerates a set of unique switch types that are present in the FPGA programmable interconnect.  The fewest switch types that can be used to accurately describe an architecture should be defined to help optimize VPR runtime.  Reasons to use different switch types for different portions of the interconnect include:  1) distinguishing between switch types that are driven by or drive different wire types (see also the segmentlist section); distinguishing between instances of the same switch that have different delay parameters.

### Segmentlist section

The `<segmentlist>` section enumerates a set of wire types that are present in the FPGA programmable interconnect.  Several properties are associated with each wire type to help construct the overall interconnect model:

* the switch type from the switch list that drives it
* a specification of the length of the wire in (X,Y) grid units
* connectivity patterns indicating how the wire interfaces to each switch point across its length
* resistance and capacitance properties that may be defined to assist in modeling delay in the FPGA, or set to 0 if unused

### Directlist section

The `<directlist>` is used to provide explicit 1:1 connections between array elements at different (X,Y) locations in the array.  This section is optional and in many architectures may be omitted.

### Complexblocklist section

The `<complexblocklist>` section provides a high-level specification for each logic block type in the array.  Each block is encapsulated within a `<pb_type>` tag that contains child tags to specify the block's port list and any local interconnect it may have.  Logic blocks may be specified with multiple levels of hierarchy by specifying additional `<pb_type>` blocks as child tags of an upper level `<pb_type>` tag.  For blocks that have multiple operating modes, operating modes are specified individually in a `<modes>` subsection.  Any local interconnect that the logic block may have (for example, CLB crossbars) are modeled with the `<interconnect>` section.  Delay parameters may also be specified for all block components.  Several syntax forms are possible for delay modeling; see https://docs.verilogtorouting.org/en/latest/arch/reference/#timing for details.

Decisions about how to represent block hierarchy are largely driven by the relationships between logic block hierarchy and the primitives that are mapped to during synthesis.  For example, consider a configurable logic block (CLB) that is comprised of multiple basic logic elements (BLEs), each of which contains a lookup table (LUT) and flip-flop.  Suppose the BLIF netlist for the architecture with this CLB uses the `.names` BLIF keyword for LUTs and `.subckt ff` for the flip-flop.  The architecture XML at the BLE level would look as shown below:

```
<pb_type name="ble" num_pb="6">
   <input name="in" num_pins="5"/>
   <input name="reset" num_pins="1"/>
   <input name="enable" num_pins="1"/>
   <output name="y" num_pins="1"/>
   <output name="ff_out" num_pins="1"/>
   <clock name="clk" num_pins="1"/>
   <pb_type name="lut" num_pb="1" blif_model=".names" class="lut">
       <input name="in" num_pins="5" port_class="lut_in"/>
       <output name="out" num_pins="1" port_class="lut_out"/>
       <metadata>
           <meta name="fasm_prefix">lut</meta>
           <meta name="fasm_type">LUT</meta>
           <meta name="fasm_lut">lu_table[31:0]</meta>
       </metadata>
   </pb_type>
   <pb_type name="ff" num_pb="1" blif_model=".subckt ff">
       <input name="D" num_pins="1"/>
       <output name="Q" num_pins="1"/>
       <input name="R" num_pins="1"/>
       <input name="E" num_pins="1"/>
       <clock name="clk" num_pins="1"/>
   </pb_type>
   <interconnect>
       <mux name="ble_output_mux" input="ff.Q[0] lut.out[0]" output="ble[0].y[0]">
       </mux>
       <direct name="ble_0_lut_direct_0" input="ble.in[4:0]" output="lut.in[4:0]"/>
       <direct name="ble_0_ff_direct_1" input="ble.clk" output="ff.clk"/>
       <direct name="lut_ff_direct_2" input="lut.out" output="ff.D"/>
       <direct name="ble_0_ff_direct_3" input="ff.Q" output="ble.ff_out"/>
       <direct name="ble_0_ff_direct_4" input="ble.reset" output="ff.R"/>
       <direct name="ble_0_ff_direct_5" input="ble.enable" output="ff.E"/>
   </interconnect>
</pb_type>
```

This entire block would then be embedded within a `<pb_type>` description for the CLB.  In addition to this content, the CLB would contain a complete description of its crossbar in its `<interconnect>` section.

### Switchblocklist section

The `<switchblocklist>` section is used only for FPGA architectures that have switch box topologies that are not pre-defined in VPR.  The three pre-defined switch block types are "universal", "subset", and "wilton".  For architectures that do not use one of these topologies, the `<switch_block>` `type` attribute in the `<device>` section is set to "custom" and this section must be included.  

> **_NOTE:_**  The connectivity specified in this section is overridden by the content of the VPR routing graph XML file.  As the VPR routing graph XML file is required for bitstream generation, modeling accuracy for this section may be relaxed at the discretion of the developer.

Custom switch blocks are specified in terms of a connectivity pattern between the four sides of the switch block plus specifications for what switch types drive the inputs and outputs of the switch blocks.  The specified switch types must appear in the `<switchlist>` section of the XML file.

In addition to VPR documentation, a useful reference for developing this section is https://utoronto.scholaris.ca/server/api/core/bitstreams/85e55c70-aaaf-4ebf-881f-10b477465371/content.

<a id="vpr_rr_graph_xml"></a>
## Routing Graph XML file

**Requiring Tool**:  VPR

**Requiring Step(s)**:  place, route, bitstream generation

VPR models the programmable interconnect of an FPGA as a directed graph where nodes represent wires in the programmable interconnect and edges represent individual input-to-output paths through switches in the interconnect.  The routing graph XML file contains a complete representation of this directed graph, enumerating all nodes and edges and their properties.  Node and edge properties include switch types, wire types, delay parameters, and other information used in the architecture model.

The routing graph XML file enables bitstream generation with genfasm by storing bitstream metadata for each graph edge.  The file must be provided with this metadata included to support genfasm execution.

Two possible development flows for producing a Logik-compatible routing graph XML file are:

1. Using the architecture XML file with VPR's `--write_rr_graph <file>` command-line option to write out a preliminary routing graph XML file, then annotating it with bitstream metadata using a post-processing script.
2. Generating a routing graph XML file with a dedicated XML generator for the architecture.

In most cases, the second of these two choices is preferred.  The first option is feasible only when the interconnect model can be exactly generated by VPR's internal routing graph generator.  In this case, the interconnect can be exactly described with the high-level interconnect model in the architecture XML file.  The graph that VPR generates must be exact node for node and edge for edge.  Any deviation between the interconnect in the FPGA and VPR's auto-generated graph model will lead to bitstream generation errors.  When VPR's built-in routing graph generator can only approximate, but not exactly replicate, an FPGA's programmable interconnect topology, the second option must be used.  

An FPGA architecture is incompatible with VPR if its interconnect topology cannot be represented in this format.  This can occur if the architecture does not have island-style interconnect, or has island-style interconnect but cannot be matched to VPR's channel model.  VPR assumes that an island-style interconnect can be described by mapping all wires in the interconnect into a three-dimensional coordinate-system, where the three dimensions are a horizontal coordinate (X), a vertical coordinate (Y), and a channel number (denoted in VPR XML files as "ptc").  These dimensions are used independently for both vertical and horizontal routing channels, i.e. a vertical channel may have the same (X, Y, ptc) tuple as a horizontal channel.

Even if the interconnect topology is hierarchical, it is usually feasible to map to this coordinate system by flattening the hierarchy and assigning different levels of interconnect hierarchy to different ptc values.  Note that for interconnect that does not physically correlate to an (X,Y) coordinate system, modeling physical properties or delay parameters accurately may be challenging even if a translation to VPR's interconnect coordinate system is feasible.

The routing graph XML file has seven major sections.  These are outlined below.  For complete documentation of VPR's routing graph XML format, please consult https://docs.verilogtorouting.org/en/latest/vpr/file_formats/#routing-resource-graph-file-format-xml

### Channels Section

The `<channels>` section enumerates the distribution of routing channels throughout the array by specifying how many horizontal and vertical channels are present at each (X,Y) location.  For many architectures, the channel count is invariant in (X,Y), but there is no requirement that this be the case.

The section is composed by specifying the minima and maxima for the horizontal and vertical channel counts, as well as the global maximum for the channel count in either direction across the entire array.  Individual horizontal channel counts are specified for each Y coordinate and individual vertical channel counts are specified for each X coordinate.

### Switches Section

The `<switches>` section enumerates the set of switch types in the architecture.  This set of switch types must match the set of switch types in the `<switchlist>` section of the architecture XML file with one exception:  an additional switch named `__vpr_delayless_switch__` must be provided for use in modeling graph edges between nodes that have zero delay.

The formatting of the switch type definitions in the routing graph file differs from that in the `<switchlist>` section of the architecture XML file.

### Segments Section

The `<segments>` section enumerates the set of wire types in the architecture.  This set of wire types must match the set of wire types in the `<segmentlist>` section of the architecture XML file.

### Block Types Section

The `<block_types>` section enumerates the different logic block types in the architecture and assigns each an integer ID.  The list of block types specified must match the top level blocks specified in the `<complexblocklist>` section of the architecture XML file.

Within each block type section, it is required to specify a pin list for the block as a list of `<pin_class>` tags.  Each `<pin_class>` tag specifies the port direction and matching port name in the corresponding `<pb_type>` definition in the architecture XML file.  It also specifies a "ptc" integer ID for each pin; this ID is used to match pins to their equivalent nodes in the routing graph.

### Grid Section

The grid section enumerates the block_type at each (X,Y) location in the array, denoting it by integer ID defined in the `<block_types>` section.  All (X,Y) coordinates are specified individually.  A single block may occupy more than one (X,Y) location.  To account for this, X and Y offsets are also specified for each (X,Y) location.  The location of a block's lower left corner is assigned an offset of (0,0), and each other location it occupies is assigned an offset relative to the lower left corner.  For example, if a memory block is of size 2x2 and occupies locations (4,4), (4,5), (5, 4), and (5, 5), location (5, 4) receives an offset assignment of (1, 0).  Blocks of size 1x1 are always assigned an offset of (0, 0).

### Graph Nodes Section

The `<rr_nodes>` section of the routing graph XML file enumerates all nodes in VPR's routing resource graph (RR graph) model of the FPGA interconnect.  Each node is assigned a type according to whether it is a logic block input/output, an interface between logic and routing, a vertical routing channel, or a horizontal routing channel.  Each node is also assigned an integer ID.  If the interconnect conists of unidirectional routing channels, a routing direction is also specified.  To map the node to VPR's three-dimensional coordinate system, each node is assigned a low (X,Y) coordinate, a high (X,Y) coordinate, and an integer id named "ptc".  The use of two (X,Y) coordinates allows the node to model a single wire that spans multiple (X,Y) locations.  The ptc ID that such a node is assigned may not be used by another node if that node is of the same type and spans any of the (X,Y) locations within that node's low and high coordinates.

To ensure the correct relationship between each node and the wire type it is modeling, each node is assigned a segment ID.  The segment ID is an integer ID that matches one of the segment definitions in the segments section of the routing graph XML file.

For architectures that model wire resistance and capacitance, these data may be embedded in the node specifications as well.  The data should match that of the corresponding segment type assigned to the node.

### Graph Edges Section

The `<rr_edges>` section of the routing graph XML enumerates the set of edges that connect the nodes in the routing resource graph.  The edges in the routing resource graph are directed and specified in terms of a source node ID, a sink node ID, and a switch ID.  The switch ID must match the integer ID assigned to a switch type in the switches section of the routing graph XML file.  VPR then models the edge as routing through that switch type.

In addition to these specifications, each edge must contain metadata tags to specify the FASM features that are emitted when the edge participates in the routing solution.  Equivalently, this means specifying what configuration bits are set to one when a routing solution uses each edge.  Any number of features, including zero, may be specified for each edge.

An example XML representation of a routing graph edge with associated genfasm metadata is shown below.

```
<edge src_node="5780" sink_node="5980" switch_id="969">
    <metadata>
        <meta name="fasm_features"> baby_fpga.tile_clb_sb_3_cb_4.sb_3.sb_out_north_mux_30.s[1]</meta>
    </metadata>
</edge>
```

<a id="bitstream_map"></a>
## Bitstream Map File

**Requiring Tool**: fasm_to_bitstream

**Requiring Step(s)**: convert_bitstream

The Logik flow provides bitstream finishing (FASM to binary conversion) with the fasm_to_bitstream Python utility.  This utility takes as input a JSON file defining a mapping of FASM features to a four-dimensional address space.  The dimensions are (X, Y, address, bit index), where

* X is the array X coordinate
* Y is the array Y coordinate
* address is an integer specifying a specific configuration word with an (X,Y) location
* bit index is an integer specifying a specific bit within a configuration word

The JSON file is prepared as JSON object with a single key/value pair.  The key is required to be "bitstream".  The value is an array that matches the four-dimensional structure of the bitstream address space.  Each array element must be a valid FASM feature generated by genfasm using the architecture's VPR XML files.  Unused locations in the address space are provisioned with empty lists.

The beginning of an example bitstream map file is shown below.  In this example, array location (0, 0) does not contain any configuration bits.  The first FASM features are specified at location (0, 1).  The configuration words have eight bits each.  Address 0 at (0, 1) uses only two of the eight available bits in the word, while address 1 and 2 each use all eight.  FASM features are listed from address word LSB to address word MSB.

```
{
"bitstream" : [
  [
    [

    ],
    [
      [
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_0.iopad.iob_config",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.clock_iob_0_0.iopad_wrapper_1.iopad.iob_config"
      ],
      [
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_0.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_0.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_1.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_1.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_2.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_2.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_3.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_3.s[1]"
      ],
      [
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_4.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_4.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_5.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_5.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_6.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_6.s[1]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_7.s[0]",
	"baby_fpga.tile_clock_iob_sb_8_cb_5_1_1.sb_8_0_0.sb_out_west_mux_7.s[1]"
      ],
```

<a id="constraint_map"></a>
## Constraint Map File

**Requiring Tool**:  VPR (pre-processing)

**Requiring Step(s)**: place

The Silicon Compiler tool driver for VPR includes a pre-processing step that converts pin constraints specified in a JSON file format to constraints specified in the XML format required by VPR.  To enable this pin constraint conversion, a part's CAD tarball must include a constraint map file that contains the mapping between pin names used in the JSON pin constraints file and pin information required for the VPR XML file.  The constraint map file is implemented as JSON document where each entry in the document is a JSON object with form showed below:

```
  "<pin_name>": {
    "x": <x_loc>,
    "y": <y_loc>,
    "subtile": <subtile_loc>
  },
```

In the above template, `<pin_name>` represents a pin name that consumers of the FPGA architecture may use in their pin constraints files.  (`<x_loc>`, `<y_loc>`) is a valid array location for an I/O block in the FPGA Architecture, `<subtile_loc>` is an integer ID that is less than the number of I/O blocks at (`<x_loc>`, `<y_loc>`), i.e. it is used to specify which of the I/O blocks at (`<x_loc>`, `<y_loc>`) maps to `<pin_name>`.  The same (`<x_loc>`, `<y_loc>`, `<subtile_loc>`) tuple may be repeated for multiple pin names to handle the case where an I/O block is configurable to either an input mode or an output mode.  This is commonly done in practice; it falls to the FPGA consumer to compose pin constraints that do not use the same location twice, and to VPR to report an error when the consumer attempts to do this.

All pins must be specified in a bitwise fashion.  Square brackets are permitted as part of `<pin_name>` if `<pin_name>` is one of several bits in a bus, but all bits of the bus should be specified separately.  For example, to specify four pins in a bus at array location (1, 2), the section of the constraint map file for (1, 2) would look as follows:

```
  "pad_out_1_2[0]": {
    "x": 1,
    "y": 2,
    "subtile": 0
  },
  "pad_out_1_2[1]": {
    "x": 1,
    "y": 2,
    "subtile": 1
  },
  "pad_out_1_2[2]": {
    "x": 1,
    "y": 2,
    "subtile": 2
  },
  "pad_out_1_2[3]": {
    "x": 1,
    "y": 2,
    "subtile": 3
  },
  "pad_in_1_2[0]": {
    "x": 1,
    "y": 2,
    "subtile": 0
  },
  "pad_in_1_2[1]": {
    "x": 1,
    "y": 2,
    "subtile": 1
  },
  "pad_in_1_2[2]": {
    "x": 1,
    "y": 2,
    "subtile": 2
  },
  "pad_in_1_2[3]": {
    "x": 1,
    "y": 2,
    "subtile": 3
  },
```

# Issues / Bugs

We use [GitHub Issues](https://github.com/siliconcompiler/logiklib/issues)
for tracking requests and bugs.

# License

[Apache License 2.0](LICENSE)
