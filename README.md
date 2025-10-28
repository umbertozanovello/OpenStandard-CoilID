# MRI RF Coil Open Data Standard (MRCODatS)

Magnetic resonance imaging (MRI) scanners are designed to accommodate different radio frequency (RF) coils depending on the region of the body being imaged and other scan requirements.
The scanner must therefore be able to identify the type of coil that is connected, its capabilities and operating parameters.
In the past this function was implemented using incompatible, vendor-specific proprietary protocols that typically identify the coil with a unique code which is then associated with a specific data file on the scanner.
In addition to being a closed, proprietary approach, it is also prone to accidental mismatching, spoofing (intentionally presenting a code belonging to another coil), missing data files, or other errors.
...
An open standard data format and transmission protocol are needed to allow the scanner to identify an RF coil's information.

## Interconnection Model

This open standard follows the spirit of the Open Systems Interconnection ([OSI](https://en.wikipedia.org/wiki/OSI_model)) model and is divided into layers as follows:
### Physical Layer
It covers storage device, connection sensor, operating voltages and communication bus.

### Communication Layer
It covers communication protocol connecting the scanner with the RF coil.

### Data Layer
It covers format and integrity of the stored data.

Contributions are welcome. Please use the [issue tracker](https://github.com/umbertozanovello/OpenStandard-CoilID/issues) to submit comments and requests.
