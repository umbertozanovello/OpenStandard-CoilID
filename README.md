> Open points:
> - Do we want to leave all the standard in the README.md file? 
> - We have to discuss the final structure of the repo. I suggest to create a repository (e.g., OpenMRStandard) containing multiple sumbodules representing the different standards, like this one here. This would make the pair with the OpenConnector project...

# MRI RF Coil Open Data Standard (MRCODatS)

Magnetic resonance imaging (MRI) scanners are designed to accommodate different radio frequency (RF) coils depending on the region of the body being imaged and other scan requirements.
The scanner must therefore be able to identify the type of coil that is connected, its capabilities and operating parameters.
In the past this function was implemented using incompatible, vendor-specific proprietary protocols that typically identify the coil with a unique code which is then associated with a specific data file on the scanner.
In addition to being a closed, proprietary approach, it is also prone to accidental mismatching, spoofing (intentionally presenting a code belonging to another coil), missing data files, or other errors.
An open standard data format and transmission protocol are needed to allow the scanner to identify an RF coil's information consistently across different platforms.

## Interconnection Model

This open standard follows the spirit of the Open Systems Interconnection ([OSI](https://en.wikipedia.org/wiki/OSI_model)) model and is divided into layers as follows:
 - **Physical Layer**: It covers the storage device, connection sensor, operating voltages and communication bus.
 - **Communication Layer**: It covers the communication protocol connecting the scanner with the RF coil.
 - **Data Layer**: It covers the format and integrity of the stored data.

### Physical Layer

<img src="/figures/coilID_2v1.svg" width=600>

#### Storage Device
The storage device storing the RF Coil data must be affordable, non-volatile, easy to buy and interface. 

Standard EEPROMs comply with these requirements. They are available for ~1$ in different sizes, packages and support various operating voltages. 

#### Communication Bus

Considering the reduced space available on the coil-side, the communication bus must not add excessive complexity to the circuitry (e.g., many connector pins; many components occupying substantial PCB real estate).

The standard makes use of the I<sup>2</sup>C protocol to trasfer the data (see [Communication Layer](#Communication-Layer)). I<sup>2</sup>C requires only two lines (SDA, SCL) in addition to the DC supply and ground. The standards recommends to add 10 kOhm pull-up resistors both on the SDA and SDL lines and both on the coil- and system-side. This reference value helps to contain the bus time constant and guarantees a reliable low logic voltage level for the open-drain transistors. In extreme cases where resistors are not enough to guarantee reliable communication, circuits like buffers, extenders and accelerators can be added to the bus.

#### Connection Detection
When the RF connector is mated to the scanner, the scanner must be able to recognise the connection. This connection sensor must be simple to implement without excessively complicating the connector circuitry.

The proposed solution is to assert the status of a pulled-up pin on the system-side ($\overline{coil \textunderscore connected}$). When connected, this pin is forced to ground and a
falling/rising-edge on the pin raises an interrupt signalling the RF coil connection/disconnection. This pin should be the last to mate, first to break (i.e., shorter than the other pins in the connector).

#### Operating Voltages

Voltage levels must be safe and compatible with common standards. In addition it must be compatible with the voltage level used by common microcontrollers, low-power supplies and USB ports. 

The standard accepts voltage levels equal to 3.3 V and 5 V. While is compatible with the supply voltages of most microcontrollers and non-negotiated USB, their level is high enough to limit cross talk due to capacitive coupling compared to lower voltage levels[<sup>1</sup>](https://www.I2C-bus.org/voltage-level/)


### Communication Layer

Communication protocol and bus are closely related and one has to fit into the other's requirements. Taking into account the requirements on the communication bus, and the need to transmit data over short to medium distances (~1-2 m or less), the standard relies on the [I<sup>2</sup>C](https://www.I2C-bus.org/) communication protocol. I<sup>2</sup>C is a syncronous serial communication bus able to operate at different standard transfer rates. Being syncronous, I<sup>2</sup>C does not require a predetermined clock speed making it more flexible for the application of this standard. Considering that a very high transfer speed is not required for this application, the standard recommends to operate the I<sup>2</sup>C bus in [standard-mode](https://www.I2C-bus.org/standard-mode/) (100 kbit/s) or [fast-mode](https://www.I2C-bus.org/fastmode/) (400 kbit/s). This reduces the requirements on the maximum bus capacitance allowing the transfer of data over longer distances. 

### Data Layer

The data format must be flexible to represent different data types and must be stand-alone, i.e., it must not require external schemas for decoding the data. In addition, data must take minimal space on the storage device and the format must be supported by in-force standards and available software libraries. Finally, the standard requires an integrity check to improve the robusteness of data against communication errors.

The standard relies on the [BSON](https://bsonspec.org/) (Binary JSON) data format for storing the data in the EEPROM. BSON is a bin­ary-en­coded seri­al­iz­a­tion of JSON-like doc­u­ments and is somewhat more compact than JSON. A BSON document is composed in the following way
```
document ::= int32 e_list \0x00
```
where `int32` is the total number of bytes comprising the document and `e_list` is the actual content of the document whose format must comply with the BSON standard data format.

Data integrity is performed by appending at the end of the BSON document a 4-byte CRC32 checksum. The following figure clarifies how the data are stored in the EEPROM

<img src="/figures/EEPROM_data.svg" width=600>


## How to Contribute

Contributions are welcome. Please use the [issue tracker](https://github.com/umbertozanovello/OpenStandard-CoilID/issues) to submit comments and requests.
