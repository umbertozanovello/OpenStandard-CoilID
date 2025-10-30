# Software Code

These are some experimental software implementations of the standard to read and write coil data to and from the EEPROM.

The read process, including verification of data integrity, is described in the flowchart below. When the RF coil is connected, the scanner scans the I<sup>2</sup>C bus at the default address (0x50) looking for the EEPROM. If detected, the stored data are read and checked against the checksum.

![read flowchart](/figures/EEPROM\_read\_flowchart.svg)

## Python

The Python code assumes that a CH341T programmer/reader is connected using USB.
![programmer connected to EEPROM]/(figures/CH341T_EEPROM.jpg)

### Requirements

The following packages must be installed in your Python environment (e.g., using `pip`):

* `i2cpy` (interfaces to the I<sup>2</sup>C bus through the CH341T)
* `zlib` (calculating checksum)
* `time` (to provide required time delays during write)
* `json` (to read from and write to a JSON file)
* `pymongo` (includes the version of the `bson` package that is actively maintained)
* `datetime` (to create datetime objects suitable for passing to BSON)

**Note: DO NOT** install the bson package using `pip install bson`. It installs an incomplete and unmaintained library.

### Functions
The following functions are provided in the `???.py` file:
- `EEPROM_find()`: scans the I<sup>2</sup>C bus and returns an `int` array of addresses at which a device is present.
- `write_coil_data(coil_data, EEPROM_address = 0x50)`: writes the `coil_data` `dict` to the EEPROM at the I<sup>2</sup>C address provided.
- `read_coil_data(EEPROM_address = 0x50)`: reads data stored in the EEPROM at the I<sup>2</sup>C address provided and checks it against the stored checksum.
- `is_json_serializable(data)`: checks if `data` (`type: dict`) is formatted according to what is expected from JSON.

### Test Script
The `???_test.py` script performs the following operations:
- reads the `test_coil.json` file
- adds current date and time to the `calDate` key
- verifies that the *estimated* total data to be written <= EEPROM_size
- if the EEPROM is present at the specified I<sup>2</sup>C address
  - writes the coil data to the EEPROM
  - reads back the coil data from the EEPROM (automatically verifying the checksum)
