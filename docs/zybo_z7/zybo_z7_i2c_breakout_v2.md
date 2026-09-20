---
SPDX-FileCopyrightText: AirSonar contributors
SPDX-License-Identifier: CERN-OHL-W-2.0
---

# Zybo Z7 I2C breakout (v2)

The JF Pmod connector (at the left edge of the Zybo Z7 when looking at the top) connects
to a number of GPIO lines from the ARM processor. This includes two [I2C][]
communication buses, I2C0 and I2C1. This PCB acts as a breakout board to connect a
number of devices to each bus.

There are four 4-pin IDC connectors (each with 3.3V, ground, clock and data lines)
connected to I2C0. As marked on the silkscreen, these are intended for communicating
with motor drivers. There are ten 4-pin connectors connected to I2C1, intended for
auxiliary sensors such as temperature sensors. Note that the actual use of the two buses
depend on the software running on the processor; the labels on the silkscreen are only
indicative of the original intent when the circuit was designed.

As the Zynq-7000 I2C lines are only rated to 3.3V, both sets of clock and data lines
have Schottky diodes for overvoltage protection if the connected devices use higher
voltages. The design also includes a power LED and a 2x6 surface mount IDC connector
which duplicates the Pmod layout allowing for testing or further development with other
GPIO lines.

[I2C]: https://en.wikipedia.org/wiki/I2C


## Design

The schematic and PCB layout were performed using the [KiCad][] design suite. If you
want the design files, it is recommended you clone the Git repository and access them
from there. A copy of the design files and associated libraries, templates etc as they
were when this documentation was built can be
```genzip
output: airsonar_zybo_z7_i2c_breakout_v2.zip
link_text: downloaded as a zipfile
%%%
directory: libraries
directory: templates
file: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_pro
file: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_sch
file: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_pcb
file: zybo_z7/i2c_breakout_v2/fp-lib-table
file: zybo_z7/i2c_breakout_v2/sym-lib-table
file: zybo_z7/i2c_breakout_v2/REUSE.toml
```
if you prefer.

A
```kipdf
output: airsonar_zybo_z7_i2c_breakout_v2.pdf
link_text: PDF of the schematics and PCB layout
%%%
source: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_sch
--no-background-color
%%%
source: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_pcb
--layers
F.Cu,F.Silkscreen,Edge.Cuts
--scale
0
%%%
source: zybo_z7/i2c_breakout_v2/zybo_z7_i2c_breakout_v2.kicad_pcb
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


Component | Description                      | Quantity | Cost
----------|----------------------------------|----------|------
C1        | 10µF 0603 ceramic capacitor      | 1        | [€0.33][dkc1]
C2-C14    | 100nF 0603 ceramic capacitor     | 13       | [€0.38][dkc2]
D1        | Orange LED (0603 package)        | 1        | [€0.21][dkd1]
D2-D5     | Schottky diode                   | 4        | [€0.84][dkd2]
J1-J14    | Through-hole 2x2 IDC header      | 14       | [€8.86][dkj1]
JF1       | Right-angle 2x6 edge connector   | 1        | [€0.92][dkjf1]
JF2       | Surface-mount 2x6 IDC header     | 1        | [€2.88][dkjf2]
R1        | 330Ω 0603 resistor               | 1        | [€0.10][dkr1]
R2-R5     | 33Ω 1/3W 0603 resistor           | 4        | [€0.52][dkr2]
          | **Total**                        |          | €15.04

[dkc1]: https://www.digikey.de/de/products/detail/cal-chip-electronics-inc/GMC10X5R106M25NT/18151144
[dkc2]: https://www.digikey.de/de/products/detail/samsung-electro-mechanics/CL10B104KB8NNND/22313108
[dkd1]: https://www.digikey.de/de/products/detail/harvatek-corporation/B1931UD-05D000314U1930/15861266
[dkd2]: https://www.digikey.de/en/products/detail/onsemi/BAT43XV2/2241875
[dkj1]: https://www.digikey.de/en/products/detail/amphenol-cs-fci/75869-130LF/1523859
[dkjf1]: https://www.digikey.de/en/products/detail/amphenol-cs-fci/10129382-912002BLF/7916140
[dkjf2]: https://www.digikey.de/de/products/detail/samtec-inc/HTST-106-01-L-DV/8473802
[dkr1]: https://www.digikey.de/de/products/detail/te-connectivity-passive-product/CRGH0603F330R/5586961
[dkr2]: https://www.digikey.de/en/products/detail/rohm-semiconductor/ESR03EZPJ330/1983466

<!-- component and software links -->

[KiCad]: https://www.kicad.org/
