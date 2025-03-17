# K6_N8_3x3 FPGA Virtual Architecture

The K6_N8_3x3 FPGA is a fixed-size virtual FPGA architecture consisting of configurable logic blocks (CLBs) and I/O blocks (IOBs).

A summary of K6_N8_3x3 resources is shown in the table below

Resource Type        | Count
---------------------|------
Lookup Tables (LUTs) | 72
Registers            | 72
GPIOs                | 96
Max Clock Domains    | 1

K6_N8_3x3 logic resources are organized into an 5x5 array of components.  A 3x3 array of CLBs is surrounded on the perimeter by four banks of IOBs, one per side of the array.  Corner array locations are unused.

## Logic Resources

A brief description for K6_N8_3x3 logic resources is shown below

### Configurable Logic Block (CLB)

Each configurable logic block (CLB) consists of 8 6-input lookup-tables (LUTs).  The LUTs in a CLB share common inputs through local routing called a crossbar.  All LUT outputs are fed back to the crossbar so that they may be used as inputs within the CLB.  Each LUT output can be paired with a flip-flop (register) to synchronize the LUT output to a common clock.  Flip-flops not paired with a LUT can accept crossbar inputs directly.  All flip-flop usage is automatically determined as part of the RTL-to-bitstream flow and is thus transparent to the user.  

### I/O Block (IOB)

General purpose I/O blocks (IOBs) are provided to provide a consistent signal interface between signals external to the FPGA and reconfigurable logic.  Each IOB contains eight iopad primitives.  Each iopad primitive can operate either in input mode or output mode.  The IOB thus supports a maximum of eight user I/O signals in any combination of inputs and outputs.

### Clocking

This architecture uses an ideal clock model; clocks are modeled as globally distributed to all logic resources with zero delay.

## K6_N8_3x3 Configuration

K6_N8_3x3 bitstreams are generated using Logik.  An 8-bit wide interface is used to load a generated bitstream.

