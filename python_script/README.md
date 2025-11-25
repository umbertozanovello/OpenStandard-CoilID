# Python EEPROM Coil Data Management

The Python code assumes that a CH341T programmer/reader is connected using USB. In this example we used an AT24C256 EEPROM which holds 256kib (262144 bits) or 32kiB.
Note the 10k resistors on the EEPROM PCB. The programmer chip has internal resistors.

![programmer connected to EEPROM](/figures/CH341T_EEPROM.jpg)

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
The following functions are provided in the `MRCoDS.py` file:
- `EEPROM_find()`: scans the I<sup>2</sup>C bus and returns an `int` array of addresses at which a device is present.
- `write_coil_data(coil_data, EEPROM_address = 0x50)`: writes the `coil_data` `dict` to the EEPROM at the I<sup>2</sup>C address provided.
- `read_coil_data(EEPROM_address = 0x50)`: reads data stored in the EEPROM at the I<sup>2</sup>C address provided and checks it against the checksum stored in the EEPROM itself.
- `is_json_serializable(data)`: checks if `data` (`type: dict`) is formatted according to what is expected from JSON.

### Test Script
The `MRCoDS_test.py` script performs the following operations:
- reads the `test_coil.json` file
- adds current date and time to the `calDate` key
- verifies that the *estimated* total data to be written <= EEPROM_size
- if the EEPROM is present at the specified I<sup>2</sup>C address
  - writes the coil data to the EEPROM
  - reads back the coil data from the EEPROM (automatically verifying the checksum)

### EEPROM Memory Screenshot
A separate programmer app was used to read the EEPROM. This screenshot shows what the binary BSON data looks like for the test script above.

![EEPROM memory dump](/figures/programmer_screenshot.png)

