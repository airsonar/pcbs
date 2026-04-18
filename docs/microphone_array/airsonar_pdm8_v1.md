---
SPDX-FileCopyrightText: AirSonar contributors
SPDX-License-Identifier: CERN-OHL-W-2.0
---

# 8-channel PDM microphone array (v1)

This is the first microphone array designed for the AirSonar project. It is based around
eight Syntiant[^knowles] [SPG08P4HM4H MEMS microphones][SPG08P4HM4H] arranged in a
linear array. The centre-to-centre spacing of the microphones is 8.5mm, approximately
half a wavelength at 20kHz in air. The microphones digitise the recorded pressure using
a single-bit [sigma-delta modulator][] to generate a [pulse-density modulated
(PDM)][PDM] output. The array is designed to be connected via a 12-pin ribbon cable, and
includes a [LMK1C1108PWR][] clock buffer to drive the microphones from a single input
clock and a [MAX8891][] linear regulator to control the supply voltage.

[^knowles]: Syntiant purchased the consumer MEMS microphones section of Knowles at the
    end of 2024. Some sources may still refer to these microphones as a Knowles product.

[sigma-delta modulator]: https://en.wikipedia.org/wiki/Delta-sigma_modulation
[PDM]: https://en.wikipedia.org/wiki/Pulse-density_modulation


## Design

The schematic and PCB layout were performed using the [KiCad][] design suite. If you
want the design files, it is recommended you clone the Git repository and access them
from there. A copy of the design files and associated libraries, templates etc as they
were when this documentation was built can be
```genzip
output: airsonar_pdm8_v1.zip
link_text: downloaded as a zipfile
%%%
directory: libraries
directory: templates
file: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_pro
file: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_sch
file: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_pcb
file: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_dru
file: microphone_array/pdm8_v1/fp-lib-table
file: microphone_array/pdm8_v1/sym-lib-table
file: microphone_array/pdm8_v1/REUSE.toml
```
if you prefer.

A
```kipdf
output: airsonar_pdm8_v1.pdf
link_text: PDF of the schematics and PCB layout
%%%
source: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_sch
--no-background-color
%%%
source: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_pcb
--layers
F.Cu,F.Silkscreen,Edge.Cuts
--scale
0
%%%
source: microphone_array/pdm8_v1/airsonar_pdm8_v1.kicad_pcb
--layers
B.Cu,B.Silkscreen,Edge.Cuts
--scale
0
```
is also available. Again, this is the status of the design when this documentation was
built. The first page contains the schematic, the second page the copper and silkscreen
for the top layer, and the third page the copper and silkscreen for the bottom layer.


### Bill of materials

The following table lists the components needed to populate a single copy of the PCB.
The prices given are to purchase the exact quantity needed for one PCB from DigiKey
(using the German storefront) as of 6 April 2026, using the 3.3V variant of the voltage
regulator and an orange LED. Prices at other suppliers will differ, using other
component variants will change the cost, and buying larger quantities will typically
reduce the unit cost.  Note that the cost of the ribbon cable and IDC crimp connectors
is not included.


Component | Description                      | Quantity | Cost
----------|----------------------------------|----------|------
C0-C10    | 100nF 0603 ceramic capacitor     | 11       | [€0.20][dkc0]
C11       | 10µF 0603 ceramic capacitor      | 1        | [€0.23][dkc11]
C12, C13  | 1µF 0603 ceramic capacitor       | 2        | [€0.14][dkc12]
D1        | Orange LED (0603 package)        | 1        | [€0.21][dkd1]
J1        | Surface-mount 2x6 IDC header     | 1        | [€2.67][dkj1]
MK0-MK7   | [SPG08P4HM4H][] MEMS microphone  | 8        | [€12.56][dkmk]
R0-R7     | 0Ω 0603 resistor                 | 8        | [€0.72][dkr0]
R8        | 330Ω 0603 resistor               | 1        | [€0.09][dkr8]
R9        | 10kΩ 0603 resistor               | 1        | [€0.09][dkr9]
U1        | [MAX8891][] linear regulator     | 1        | [€1.61][dku1]
U2        | [LMK1C1108PWR][] clock buffer    | 1        | [€3.25][dku2]
          | **Total**                        |          | €21.77

[dkc0]: https://www.digikey.de/de/products/detail/samsung-electro-mechanics/CL10B104KB8NNWC/3887593
[dkc11]: https://www.digikey.de/de/products/detail/cal-chip-electronics-inc/GMC10X5R106M25NT/18151144
[dkc12]: https://www.digikey.de/de/products/detail/taiyo-yuden/TMK107B7105KA-T/2714177
[dkd1]: https://www.digikey.de/de/products/detail/harvatek-corporation/B1931UD-05D000314U1930/15861266
[dkj1]: https://www.digikey.de/de/products/detail/samtec-inc/HTST-106-01-L-DV/8473802
[dkmk]: https://www.digikey.de/de/products/detail/syntiant/SPG08P4HM4H-1/10130506
[dkr0]: https://www.digikey.de/de/products/detail/walsin-technology-corporation/WR06X000-PTL/5978108
[dkr8]: https://www.digikey.de/de/products/detail/te-connectivity-passive-product/CRGH0603F330R/5586961
[dkr9]: https://www.digikey.de/de/products/detail/te-connectivity-passive-product/CRGH0603J10K/2385379
[dku1]: https://www.digikey.de/de/products/detail/analog-devices-inc-maxim-integrated/MAX8891EXK33-T/10461057
[dku2]: https://www.digikey.de/de/products/detail/texas-instruments/LMK1C1108PWR/13627117

A bill of materials with this particular choice of components can be [downloaded as a
CSV](airsonar_pdm8_v1_bom.csv) and used with your preferred supplier or BOM tool.


### Power budget

The microphones can operate with a supply voltage between 1.65V and 3.6V; the clock
buffer has specifications for supply voltages of 1.8V, 2.5V and 3.3V. The highest
required supply current for any of these voltages has been used for the power budget in
the table below. It is also worth noting that the current required by the clock buffer
depends on the clock frequency. The values in section 6.5 of its datasheet (revision A)
are for a 100MHz clock. The figure in section 6.7 indicates the supply current will be
less than 20mA from a 3.3V supply at 5MHz; this value is used for the power budget. A
current of 5mA has been allowed for the power LED.

| Component                     | Max current | Quantity | Required current |
|-------------------------------|:-----------:|:--------:|:----------------:|
| [SPG08P4HM4H][] microphone    |    2 mA     |     8    |       16 mA      |
| [LMK1C1108PWR][] clock buffer |   20 mA     |     1    |       20 mA      |
| Power LED                     |    5 mA     |     1    |        5 mA      |
| **Total**                     |             |          |     **41 mA**    |


## Configuration

The design has several hardware configuration options for the user. The supply voltage
can be set as needed by selecting the appropriate variant of the voltage regulator, and
a number of solder bridges need to be set to determine how the PDM outputs of the
microphones operate.


### Power supply

The circuit includes a [MAX8891][] low-dropout linear regulator (U1). There are a number
of pin-compatible variants of the regulator with different output voltages. The supply
voltage (Vdd) for the circuit can be between 1.8V and 3.3V.

There are three types of logic signals on the connector: the clock input (routed through
the clock buffer), the select input, and the data outputs. The valid voltages for these
signals are summarised in the following table.

Signal          | Logic low        | Logic high
----------------|------------------|--------------------
Clock (input)   | -0.5V to 0.3Vdd  | 0.7Vdd to 3.6V
Select (input)  | -0.3V to 0.2V    | Vdd - 0.2V to 3.6V
Data (output)   |  0V to 0.45V     | Vdd - 0.45V to Vdd

The inputs are tolerant to 3.6V (preferably 3.3V) regardless of the supply voltage. The
output level is dependent on the supply voltage. As such, the regulator variant should
be selected to ensure the output logic level is compatible with the system reading it.

Alternatively, the regulator can be skipped and the voltage supply from the connecting
cable used to directly power the circuit. To achieve this, do not place the regulator
and use a solder bridge to short JP13.

Note that the regulator has a sufficiently low dropout (approximately 50mV at the 41mA
from the power budget) to be usable with an input voltage that is the same as the
desired supply voltage.


### Microphone select line

The data output from each microphone is driven around one edge of the clock and is high
impedance around the other edge of the clock. The desired output edge is set by the SEL
input (pin 6) to the microphone:

* If SEL = VDD, the data output should be sampled on the falling edge of the clock.
* If SEL = GND, the data output should be sampled on the rising edge of the clock.

The circuit has a number of jumpers (corresponding to solder bridges on the PCB) which
must be set to configure the output edge of each microphone. The eight jumpers JP0
through JP7 configure the corresponding microphone (MK0 through MK7). These can be used
to directly set its microphone SEL line to either VDD or GND as desired. Alternatively,
the jumper can be set to the BSEL line (denoted BOARD on the PCB silkscreen) which
corresponds to a setting for the entire PCB.

This board-level setting is configured by JP8. This can be connected to VDD or GND, or
to the SEL line from the connector (labelled CONNECTOR on the PCB silkscreen). The
latter option allows the edge to use for the board to be configured by setting pin 3 of
the connector cable to VDD or GND as desired. This means that the output edge is
determined by the system that the board is connected to.

!!! Warning
    The microphone datasheet does have a figure (Figure 5 in Rev D-1) which suggests the
    SEL pin can be left unconnected for single-microphone applications (i.e., if not
    multiplexing a stereo pair). It is unclear which clock edge the data line is driven
    on in this case; the voltage may remain long enough to be read on either edge. It is
    recommended that the solder bridges are explicitly set to define the desired edge.


### Output multiplexing

As their data outputs are high-impedance around the unused clock edge, two
microphones using opposite clock edges can be connected to a single data line as a
stereo pair.[^micddr] This can be done at a board level by connecting two PCBs to the
same data lines with one PCB configured to use the rising edge and the other the falling
edge (it is recommended that the CONNECTOR option for the microphone select line is used
in this case to prevent mismatches, with one receiver connector setting SEL to ground
and the other setting it to Vdd).

Alternatively, this multiplexing can be done on a single PCB. The jumpers JP9 through
JP12 each connect the data outputs from two microphones (the pairs are MK0 and MK4, MK1
and MK5, MK2 and MK6, MK3 and MK7). In this case, the connector can be replaced by an
eight-pin connector omitting pins 9-12 of the full connector if desired.

[^micddr]: Note that this requires the system receiving the microphone data to be able
    to handle double data rate (DDR) inputs.


## Usage notes

### Microphone clock speeds

The microphones have three power modes (excluding the powered off state) depending on
the frequency of the supplied clock signal:

* Sleep mode: clock less than 250kHz
* Low power mode: clock between 600kHz and 950kHz
* Normal mode: clock between 1.2MHz and 4.8MHz

Note that there are gaps between these frequency bands in which the mode is undefined.


### Microphone wake-up time

When transitioning from the sleep mode to an active mode, the datasheet specifies a
maximum wake-up time of 20ms (Table 2 of revision D-1). From the same table, the startup
from an unpowered microphone to an active state takes a maximum of 50ms. If putting the
microphones in sleep mode to save power, make sure they are woken up a sufficient time
before you wish to record.


### DC offset

As the microphone is a capacitive sensor, it typically has a DC offset, and this offset
changes over time. The datasheet gives a range of -3.25% to 0.1% of the full-scale
output for the DC offset.


### Microphone polarity

The microphone datasheet states that an increasing sound pressure results in a
decreasing density of 1s in the PDM output stream. If downsampled directly, the waveform
will be inverted from the original pressure wave incident at the microphones. To
correct this, the PDM stream can be bit-inverted on collection or before processing
starts. Alternatively, the final waveform can be negated, but note that the microphone
typically has a drifting DC offset which may complicate this.


<!-- component and software links -->

[KiCad]: https://www.kicad.org/
[MAX8891]: https://www.analog.com/en/products/max8891.html
[LMK1C1108PWR]: https://www.ti.com/product/de-de/LMK1C1108/part-details/LMK1C1108PWR
[SPG08P4HM4H]: https://www.syntiant.com/s/SPG08P4HM4H-1_Baracus_Datasheet_RevD-1.pdf
