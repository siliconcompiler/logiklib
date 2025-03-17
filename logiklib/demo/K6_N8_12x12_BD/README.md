# K6_N8_12x12_BD FPGA Virtual Architecture

The K6_N8_12x12_BD FPGA is a fixed-size virtual FPGA architecture consisting of configurable logic blocks (CLBs), multipliers (DSP blocks), single-port SRAM blocks (BRAMs), and I/O blocks (IOBs).

A summary of K6_N8_12x12_BD resources is shown in the table below

Resource Type        | Count
---------------------|------
Lookup Tables (LUTs) | 736
Registers            | 736
18x18 Multipliers    | 1
4KB SRAM Blocks      | 1
GPIOs                | 352
Max Clock Domains    | 1

K6_N8_12x12_BD logic resources are organized into an 14x14 array of components.  A 12x12 array of logic blocks is surrounded on the perimeter by four banks of IOBs, one per side of the array.  Corner array locations are unused.

## Logic Resources

A brief description for K6_N8_12x12_BD logic resources is shown below

### Configurable Logic Block (CLB)

Each configurable logic block (CLB) consists of 8 6-input lookup-tables (LUTs).  The LUTs in a CLB share common inputs through local routing called a crossbar.  All LUT outputs are fed back to the crossbar so that they may be used as inputs within the CLB.  Each LUT output can be paired with a flip-flop (register) to synchronize the LUT output to a common clock.  Flip-flops not paired with a LUT can accept crossbar inputs directly.  All flip-flop usage is automatically determined as part of the RTL-to-bitstream flow and is thus transparent to the user.  

### I/O Block (IOB)

General purpose I/O blocks (IOBs) are provided to provide a consistent signal interface between signals external to the FPGA and reconfigurable logic.  Each IOB contains eight iopad primitives.  Each iopad primitive can operate either in input mode or output mode.  The IOB thus supports a maximum of eight user I/O signals in any combination of inputs and outputs.

### 18x18 Multiplier Block (DSP)

To demonstrate hard arithmetic technology mapping, hard multipliers are offered.  The multipliers take two 18-bit inputs and produce a 36-bit output.  The block is fully combinational to keep the model as simple as possible.  The multipliers are modeled as occupying a 2x2 footprint within the 12x12 array of logic blocks.  This sizing is chosen for demonstration purposes and does not reflect the relative sizing of the multiplier to the CLB in any process technology.

### SRAM Block (BRAM)

A fixed size single port SRAM is provided to demonstrate memory technology mapping.  The memory macro is 4096x8 bits.  Each macro is modeled as occupying a 2x2 footprint within the 12x12 array of logic blocks.  This sizing is chosen for demonstration purposes and does not reflect the relative sizing of the SRAM to the CLB in any process technology.

### Clocking

This architecture uses an ideal clock model; clocks are modeled as globally distributed to all logic resources with zero delay.

## K6_N8_12x12_BD Configuration

K6_N8_12x12_BD bitstreams are generated using Logik.  An 8-bit wide interface is used to load a generated bitstream.

