# -*- coding: utf-8 -*-

from MRCoDS import EEPROM_find, write_coil_data, read_coil_data
import json
from datetime import datetime, timezone

file_name = "test_multinuclear_coil.json"  # input JSON file with desired coil data fields

with open(file_name, 'r') as file:
    coil_data = json.load(file)

# add current UTC datetime to coil_data as calDate
# probably not the best way to give BSON a date; the pymongo includes a proper implementation 
# https://stackoverflow.com/questions/78394629/bson-timestamp-for-mongodb-in-python
utc_now = datetime.now(timezone.utc)
#utc_timestamp = utc_now.timestamp()
#utc_int = int(1000*utc_timestamp) # in ms since the epoch (https://bsonspec.org/spec.html)
coil_data["calDate"] = datetime.utcnow()

# values for the Atmel AT24C256 EEPROM
EEPROM_address = 0x50  # 80 as decimal
EEPROM_size = int(262144/8)  # bytes

EEPROM_addresses = list(range(0x50, 0x58))     # acceptable range of standard EEPROM addresses

# verify that *estimated* total data to be written <= EEPROM_size
if len(str(coil_data)) > EEPROM_size: #sys.getsizeof(checksum) is actually way larger (28) than it should be (4)
    print('data too large for ' + EEPROM_size + ' byte EEPROM!!')
    quit()
    
i2c_devices = EEPROM_find()

# check EEPROM_address is present and execute operations
if any(num in i2c_devices for num in EEPROM_addresses):
    print(i2c_devices, 'is/are in the EEPROM address range')

    result = write_coil_data(coil_data, EEPROM_address)
    
    # check for write errors before proceeding
    if result == 0:
        quit()
    
    read_data, checksum = read_coil_data(EEPROM_address)
    
    read_data
    