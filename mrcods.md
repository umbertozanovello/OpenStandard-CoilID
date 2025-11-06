# MRCODS - MRI RF Coil Open Data Standard

## Interconnection Model

This open standard follows the spirit of the Open Systems Interconnection ([OSI](https://en.wikipedia.org/wiki/OSI_model)) model and is divided into layers as follows:
 - **Physical Layer**: It covers the storage device, connection sensor, operating voltages and communication bus.
 - **Communication Layer**: It covers the communication protocol connecting the scanner with the RF coil.
 - **Data Layer**: It covers the format and integrity of the stored data.

### Physical Layer

<img src="/figures/coilID_2v1.svg" width=600>

#### Storage Device
The storage device storing the RF Coil data must be affordable, non-volatile, easy to buy and interface. 

Standard EEPROMs comply with these requirements. They are available for ~1$ in different sizes, packages and support various operating voltages. A means of write-protecting the EEPROM shall be implemented to prevent accidental overwriting of the coil data. Depending on the EEPROM package, the memory may come along with a number of pins that are used to set the I<sup>2</sup>C address of the memory on the bus. This stadard requires the pin to be set to logical zero which defaults to a I<sup>2</sup>C bus address of 0x50

#### Communication Bus

Considering the limited space available on the coil-side, the communication bus must not add excessive complexity to the circuitry (e.g., many connector pins; many components occupying substantial PCB real estate).

The standard makes use of the I<sup>2</sup>C protocol to trasfer the data (see [Communication Layer](#Communication-Layer)). I<sup>2</sup>C requires only two lines (SDA, SCL) in addition to the DC supply and ground. The standards recommends to add 10 kOhm pull-up resistors both on the SDA and SDL lines and both on the coil- and system-side. This reference value helps to contain the bus time constant and guarantees a reliable low logic voltage level for the open-drain transistors. In extreme cases where resistors are not enough to guarantee reliable communication, circuits like buffers, extenders and accelerators can be added to the bus.

#### Connection Detection

When the RF connector is mated to the scanner, the scanner must be able to recognise the connection. This connection sensor must be simple to implement without excessively complicating the connector circuitry.
The proposed solution is to assert the status of a pulled-up pin on the system-side ($\overline{\rm coil\_{connected}}$). When connected, this pin is forced to ground and a falling/rising-edge on the pin raises an interrupt signalling the RF coil connection/disconnection. This pin should be the last to mate, first to break (i.e., shorter than the other pins in the connector).

#### Operating Voltages

Voltage levels must be safe and compatible with common standards. In addition it must be compatible with the voltage level used by common microcontrollers, low-power supplies and USB ports. 

The standard accepts voltage levels equal to 3.3 V and 5 V. While is compatible with the supply voltages of most microcontrollers and non-negotiated USB, their level is high enough to limit cross talk due to capacitive coupling compared to lower voltage levels[<sup>1</sup>](https://www.I2C-bus.org/voltage-level/).


### Communication Layer

Communication protocol and bus are closely related and one has to fit into the other's requirements. Taking into account the requirements on the communication bus, and the need to transmit data over short to medium distances (~1-2 m or less), the standard relies on the [I<sup>2</sup>C](https://www.I2C-bus.org/) communication protocol. I<sup>2</sup>C is a syncronous serial communication bus able to operate at different standard transfer rates. Being syncronous, I<sup>2</sup>C does not require a predetermined clock speed making it more flexible for the application of this standard. Considering that a very high transfer speed is not required for this application, the standard recommends to operate the I<sup>2</sup>C bus in [standard-mode](https://www.I2C-bus.org/standard-mode/) (100 kbit/s) or [fast-mode](https://www.I2C-bus.org/fastmode/) (400 kbit/s). This reduces the requirements on the maximum bus capacitance allowing the transfer of data over longer distances. 

### Data Layer

The data format must be flexible to represent different data types and must be stand-alone, i.e., it must not require external schemas for decoding the data. In addition, data must take minimal space on the storage device and the format must be supported by in-force standards and available software libraries. Finally, the standard requires an integrity check to improve the robusteness of data against communication errors.

The standard relies on the [BSON](https://bsonspec.org/) (Binary JSON) data format for storing the data in the EEPROM. BSON is a binary-encoded serialization of JSON-like documents and is somewhat more compact than JSON (it is also more structured than JSON, e.g., for time and date information). A BSON document is composed in the following way
```
document ::= int32 e_list \0x00
```
where `int32` is the total number of bytes comprising the document and `e_list` is the actual content of the document whose format must comply with the BSON standard data format.

Data is stored beginning at address 0x0000 of the EEPROM and integrity checking is performed by appending a 4-byte CRC32 checksum at the end of the BSON document. The following figure clarifies how the data are stored in the EEPROM.

<img src="/figures/EEPROM_data.svg" width=600>

#### Data Fields

Data are stored in [BSON](https://bsonspec.org/) as key/value pairs. The following table defines a range of possible key names that are relevant to MR coils. *At minimum*, the BSON data shall include the *cID* tag, but the spirit of this standard is to include as many relevant keys as possible to eliminate the need for a coil file on the scanner.

|Field Name|BSON Key|Type|Comment|
|---|---|---|---|
|Coil ID|cID|int32|unique identifier|
| Manufacturer | mfg | cstring |  |
| Manufacturer part \# | PN | cstring |  |
| Revision | rev | cstring |  |
| Device Serial \# | SN | cstring |  |
| Coil name | name | cstring |  |
| Coil type | type | cstring | TX, RX, T/R |
| Number of TX Channels  | nTX | int32 |  |
| Number of RX Channels  | nRX | int32 |  |
| Creation Date | mfgDate | uint64 |  |
| Calibration Date | calDate | uint64 |  |
| Magnetic Field Strength | b0 | double |  |
| Resonant Nucleus | nucleus | cstring | Isotope in standard AZE notation (with Z omitted), e.g., 1H, 31P, etc. |
| Nominal Frequency | f0 | double |  |
| Nominal bandwidth | bw | double |  |
| RF coil sensitivity | sens | double |  |
| Nominal loading factor | qDamping | double | QU/QL, sometimes determined at run time |
| Maximum Incident Power | maxP | double | for TX coils |
| Maximum B1 | maxB1 | double | for RX coils |
| Tunable | tuneMatch | bool | True if capable of remote automatic tune/match |
| Malfunction detection | faultCheck | bool | True if capable of triggering malfunction signal in real time during scan |
| RX delay | rxDelay | double | Minimum tune/detune delay to allow coil state to stabilize |
| TX delay | txDelay | double | Minimum tune/detune delay to allow coil state to stabilize |
| Nominal FOV in x | xFov | double | ↓ |
| Nominal FOV in y | yFov | double | To check if scan FOV is compatible with the coil's FOV |
| Nominal FOV in z | zFov | double | ↑ |
| Local SAR | localSar | double |  |
| Body SAR | bodySar | double |  |
| Temperature sensors | tempSens | int32 | Number of temperature sensors (addressable via I2C) |
| diagnostics | diag | bool | True if diagnostic information is available via I2C |


**Notes**
- Wherever possible we have used names compatible with those used in [DICOM](https://www.dicomstandard.org) tags to facilitate including coil data in DICOM headers of the resulting images.
- quantities that require units shall use SI units without multiplier (prefix).
- BSON dates are encoded as `uint64` but programmatically they should be created from a date or datetime object according to what is available in the software language and environment used (see [Available Implementations](README.md#available-implementations)).


## Read Workflow

![read flowchart](/figures/EEPROM\_read\_flowchart.svg)

The read process, including verification of data integrity, is described in the flowchart above. When the RF coil is connected, the scanner scans the I<sup>2</sup>C bus at the default address (0x50) looking for the EEPROM. If detected, the first 4 bytes are decoded to assess the document length. The remaining bytes are read and checked against the checksum. If the check is passed, the binary data are decoded in a human readable format and made available to the scan control software.

## License
![CClicense](https://i.creativecommons.org/l/by-nd/4.0/88x31.png)\
The MRCODS standard is licensed under a [Creative Commons Attribution-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nd/4.0/).
