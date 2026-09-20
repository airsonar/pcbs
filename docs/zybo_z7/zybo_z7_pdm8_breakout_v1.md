---
SPDX-FileCopyrightText: AirSonar contributors
SPDX-License-Identifier: CERN-OHL-W-2.0
---

# Zybo Z7 PDM8 microphone array breakout (v1)

The Pmod connectors at the bottom of the Zybo Z7 (when viewed from the top side) connect
to various IO lines from the FPGA part of the Zynq-7000. These allow custom hardware to
be connected to the FPGA. This PCB acts as a breakout board to connect multiple [PDM8
microphone arrays](../microphone_array/airsonar_pdm8_v1.md) to the FPGA.

When connected to a Zybo Z7-20 variant, up to eight microphone arrays can be connected.
These are configured in a dual-edge mode with two microphones connected to each FPGA IO
pin, outputting data on alternate clock edges. One of the FPGA IO lines is used to
provide the clock to the microphones, leaving 31 pins available for input and thus a
maximum of 62 microphones can be read. The Zybo Z7-10 variant does not include the JB
Pmod connector. This reduces the available input pins to 23 for a maximum of 46
microphones.

The breakout includes a [LMK1C1108PWR][] clock buffer to duplicate the clock signal for
each connector. This avoids adding too much load to the FPGA IO providing the clock.

The breakout also includes a power LED and duplicates of each Pmod connector for
debugging or further development.

!!! Warning
    The connector footprint for the Pmod duplicates (the bottom row of connectors) is
    the same footprint as for the array connectors. However, it is not pin compatible
    with the array connectors; plugging a microphone array into the Pmod duplicate will
    short the power supply. Although the Zybo Z7 appears to handle and recover from
    this, it is recommended that these connectors only be populated if needed, or that a
    different style of connector is used to avoid accidental connections.


## Design

The schematic and PCB layout were performed using the [KiCad][] design suite. If you
want the design files, it is recommended you clone the Git repository and access them
from there. A copy of the design files and associated libraries, templates etc as they
were when this documentation was built can be
```genzip
output: airsonar_zybo_z7_pdm8_breakout_v1.zip
link_text: downloaded as a zipfile
%%%
directory: libraries
directory: templates
file: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_dru
file: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_pro
file: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_sch
file: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_pcb
file: zybo_z7/pdm8_breakout_v1/fp-lib-table
file: zybo_z7/pdm8_breakout_v1/sym-lib-table
file: zybo_z7/pdm8_breakout_v1/REUSE.toml
```
if you prefer.

A
```kipdf
output: airsonar_zybo_z7_pdm8_breakout_v1.pdf
link_text: PDF of the schematics and PCB layout
%%%
source: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_sch
--no-background-color
%%%
source: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_pcb
--layers
F.Cu,F.Silkscreen,Edge.Cuts
--scale
0
%%%
source: zybo_z7/pdm8_breakout_v1/zybo_z7_pdm8_breakout_v1.kicad_pcb
--layers
B.Cu,B.Silkscreen,Edge.Cuts
--scale
0
```
is also available. Again, this is the status of the design when this documentation was
built. The first page contains the schematic, the second page the copper and silkscreen
for the top layer, and the third page the copper and silkscreen for the bottom layer.


### Bill of materials

The following table lists the components needed to fully populate a single copy of the
PCB.  The prices given are to purchase the exact quantity needed for one PCB from
DigiKey (using the German storefront) as of 20 September 2026. Prices at other suppliers
will differ, using other component variants will change the cost, and buying larger
quantities will typically reduce the unit cost. Note that the cost of the ribbon cable
and IDC crimp connectors is not included.


Component                     | Description                      | Quantity | Cost
------------------------------|----------------------------------|----------|------
C1-C3, C5, C7, ..., C33       | 100nF 0603 ceramic capacitor     | 19       | [€0.55][dkc1]
C4, C6, ..., C32              | 10µF 0603 ceramic capacitor      | 16       | [€3.09][dkc4]
D1                            | Orange LED (0603 package)        | 1        | [€0.21][dkd1]
JB1-JE1                       | Right-angle 2x6 edge connector   | 4        | [€3.68][dkjb1]
JB2-JE2, JMA1-JMA4, JMB1-JMB4 | Surface-mount 2x6 IDC header     | 12       | [€29.34][dkjb2]
R1                            | 10kΩ 0603 resistor               | 1        | [€0.09][dkr1]
R2                            | 330Ω 0603 resistor               | 1        | [€0.10][dkr2]
U1                            | [LMK1C1108PWR][] clock buffer    | 1        | [€4.44][dku1]
                              | **Total**                        |          | €41.50

[dkc1]: https://www.digikey.de/de/products/detail/samsung-electro-mechanics/CL10B104KB8NNND/22313108
[dkc4]: https://www.digikey.de/de/products/detail/cal-chip-electronics-inc/GMC10X5R106M25NT/18151144
[dkd1]: https://www.digikey.de/de/products/detail/harvatek-corporation/B1931UD-05D000314U1930/15861266
[dkjb1]: https://www.digikey.de/en/products/detail/amphenol-cs-fci/10129382-912002BLF/7916140
[dkjb2]: https://www.digikey.de/de/products/detail/samtec-inc/HTST-106-01-L-DV/8473802
[dkr1]: https://www.digikey.de/de/products/detail/te-connectivity-passive-product/CRGH0603J10K/2385379
[dkr2]: https://www.digikey.de/de/products/detail/te-connectivity-passive-product/CRGH0603F330R/5586961
[dku1]: https://www.digikey.de/de/products/detail/texas-instruments/LMK1C1108PWR/13627117

## Array configuration

The connectors provide the 3.3V power supply from the Zybo Z7 to the microphones, and
the FPGA expected a 3.3V data signal from the microphones. The 3.3V variant of the
low-dropout regulator may still be used for additional power supply isolation as the
voltage drop is not large enough to cause problems. Alternatively, the regulator can be
removed and bypassed with the corresponding solder jumper on the array PCB.

The upper row of array connectors (labelled ROW A on the silkscreen) set the SEL
(select) line to ground, corresponding to data output on the rising edge. The lower row
of array connectors (ROW B on the silkscreen) sets the SEL line to 3.3V, corresponding
to data output on the falling edge. The microphone arrays should be configured through
the solder jumpers to use the SEL line from the connector. This ensures the output mode
of the microphones to be determined by which breakout connector they are connected to.


## FPGA IO pins

The following table lists the IO connections to the Zybo Z7 for each microphone line.
The first entry in each cell is the Pmod connector pin the microphone is connected to,
and the second entry is the FPGA IO pin it is connected to.

Microphone | Board 1    | Board 2    | Board 3       | Board 4
-----------|------------|------------|---------------|-----------
    0      | JE4 / H15  | JD4 / R14  | Not connected | JB4 / V7
    1      | JE10 / Y17 | JD10 / V18 | JC10 / U12    | JB10 / W6
    2      | JE3 / J15  | JD3 / P14  | JC3 / T11     | JB3 / U7
    3      | JE9 / T17  | JD9 / V17  | JC9 / T12     | JB9 / V6
    4      | JE2 / W16  | JD2 / T15  | JC2 / W15     | JB2 / W8
    5      | JE8 / U17  | JD8 / U15  | JC8 / Y14     | JB8 / Y6
    6      | JE1 / V12  | JD1 / T14  | JC1 / V15     | JB1 / V8
    7      | JE7 / V13  | JD7 / U14  | JC7 / W14     | JB7 / Y7


<!-- component and software links -->

[KiCad]: https://www.kicad.org/
[LMK1C1108PWR]: https://www.ti.com/product/de-de/LMK1C1108/part-details/LMK1C1108PWR
