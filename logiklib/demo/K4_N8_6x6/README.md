# K4_N8_6x6 FPGA Virtual Architecture

The K4_N8_6x6 FPGA is a fixed-size virtual FPGA architecture consisting of configurable logic blocks (CLBs) and I/O blocks (IOBs).

A summary of K4_N8_6x6 resources is shown in the table below

Resource Type        | Count
---------------------|------
Lookup Tables (LUTs) | 288
Registers            | 288
GPIOs                | 192
Max Clock Domains    | 1

K4_N8_6x6 logic resources are organized into an 8x8 array of components.  A 6x6 array of CLBs is surrounded on the perimeter by four banks of IOBs, one per side of the array.  Corner array locations are unused.

## Logic Resources

A brief description for K4_N8_6x6 logic resources is shown below

### Configurable Logic Block (CLB)

Each configurable logic block (CLB) consists of 8 4-input lookup-tables (LUTs).  The LUTs in a CLB share common inputs through local routing called a crossbar.  All LUT outputs are fed back to the crossbar so that they may be used as inputs within the CLB.  Each LUT output can be paired with a flip-flop (register) to synchronize the LUT output to a common clock.  Flip-flops not paired with a LUT can accept crossbar inputs directly.  All flip-flop usage is automatically determined as part of the RTL-to-bitstream flow and is thus transparent to the user.  

### I/O Block (IOB)

General purpose I/O blocks (IOBs) are provided to provide a consistent signal interface between signals external to the FPGA and reconfigurable logic.  Each IOB contains eight iopad primitives.  Each iopad primitive can operate either in input mode or output mode.  The IOB thus supports a maximum of eight user I/O signals in any combination of inputs and outputs.

### Clocking

This architecture uses an ideal clock model; clocks are modeled as globally distributed to all logic resources with zero delay.

## K4_N8_6x6 Configuration

K4_N8_6x6 bitstreams are generated using Logik.  An 8-bit wide interface is used to load a generated bitstream.

