# Software code

These are some experimental software implementations of the standard to read and write coil data to and from the EEPROM.

The read process, including verification of data integrity, is described in the flowchart below.

!\[read flowchart](../figures/EEPROM\_read\_flowchart.svg)

## Python

The Python code assumes that a CH341T programmer/reader is connected using USB.

### Requirements

The following packages must be installed in your Python environment (e.g., using `pip`):

* i2cpy (interfaces to the I2C bus through the CH341T)
* zlib (calculating checksum)
* time (to provide required time delays during write)
* json (to read from and write to a JSON file)
* pymongo (includes the version of the `bson` package that is actively maintained)
* datetime (to create datetime objects suitable for passing to BSON)

N.B.: **DO NOT** install the bson package using `pip install bson`. It installs an incomplete and unmaintained library.

