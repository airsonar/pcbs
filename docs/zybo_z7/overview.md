---
SPDX-FileCopyrightText: AirSonar contributors
SPDX-License-Identifier: CERN-OHL-W-2.0
---

# Zybo Z7 ARM/FPGA development board

The [Digilent Zybo Z7][zybo-z7] is a development board based around the [AMD (formerly
Xilinx) Zynq-7000][zynq-7000] system-on-a-chip (SoC). The Zynq-7000 combines a dual-core
ARM Cortex-A9 processor with a Artix-7 FPGA logic. These communicate over standard
[AXI][] communication buses, allowing custom peripherals to be designed in the
programmable logic to communicate with the processor. For the AirSonar project, this
allows many PDM microphones to be simultaneously handled in programmable logic with the
captured data being transferred to processor memory for subsequent processing and
transfer to the client.

The development board contains a number of peripherals, including gigabit Ethernet and a
Analog Devices SSM2603 audio codec outputting to a standard 3.5mm audio jack. It also
has a number of [Pmod connectors][Pmod] allowing custom circuits to be connected to the
development board.

Note that there are two variants of the Zybo Z7, the -10 and -20. These correspond to
different variants of the Zync-700, and the -10 variant has one fewer PMOD connector.
The designs in this repository are tested with the -20 variant but should be usable with
the -10.


[AXI]: https://en.wikipedia.org/wiki/Advanced_eXtensible_Interface
[Pmod]: https://en.wikipedia.org/wiki/Pmod_Interface
[zybo-z7]: https://digilent.com/reference/programmable-logic/zybo-z7/start
[zynq-7000]: https://www.amd.com/en/products/adaptive-socs-and-fpgas/soc/zynq-7000.html
