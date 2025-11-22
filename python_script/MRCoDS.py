# -*- coding: utf-8 -*-
# functions to read and write to EEPROM according to the MR RF Coil Data Standard
# uses i2cpy and the "ch341" programmer board
# use the bson package installed with PyMongo (`pip install pymongo`)
# `pip install bson` installs an incompatible and unsupported package

from i2cpy import I2C
import bson
import zlib
import time
import json

#driver="ch341"  # driver used should be defined globally somewhere

def EEPROM_find():
    """
    scans I2C bus and returns addresses at which a device is present
    Returns
    -------
    i2c_devices : int array
 
    """
    
    i2c = I2C(driver="ch341")   # tried with ", freq=100e3" but not necessary 
    i2c.init()
    i2c_devices = i2c.scan()
    print('I2C bus devices found: ', i2c_devices)
    i2c.deinit()
    return i2c_devices


def write_coil_data(coil_data, EEPROM_address = 0x50):
    # check that coil_data is a dict
    if type(coil_data) != dict:
        print('write_coil_data ERROR: coil_data must be a dict!')
        return 0
        #quit()
    if is_json_serializable(coil_data) == False:
        print('write_coil_data ERROR: coil_data must be JSON-like!')
        return 0
        
    page_size = 64  # can only write one page at a time
    time_delay = 0.1 # [s] small delay between page writes otherwise it can only write one (doesn't increment to the next page)
    #if EEPROM_address == []:
    #    EEPROM_address = 0x50
        
    if EEPROM_address not in EEPROM_find():
        print('write_coil_data ERROR: no EEPROM present at address', EEPROM_address, '!')
        return 0
        
    i2c = I2C(driver="ch341")   # tried with ", freq=100e3" but not necessary 
    i2c.init()        
    i2c.writeto_mem(EEPROM_address, 0, bytes.fromhex("00"), addrsize=8)    # dummy write to reset address counter
    
    #encoded_bytes = bson.dumps(coil_data) # only works with old bson package
    encoded_bytes = bson.BSON.encode(coil_data)
    checksum = zlib.crc32(encoded_bytes)
    print('\noriginal CRC32 checksum of BSON data = ', checksum)
    data_length = len(encoded_bytes)
    assembled_bytes = encoded_bytes + checksum.to_bytes(4,'big')
    
    # write one page at a time as required to prevent rollover
    print('Writing', page_size, '-byte pages to EEPROM at address', EEPROM_address,'...')
    for page in range(data_length//page_size+1):
        print('page ', page)
        page_start = page * page_size   # memory address offset of nth page
        mod = page_start % 256
        bytes_page = mod.to_bytes(1,'big') + assembled_bytes[page_size*page:page_size*(page+1)]
        i2c.writeto_mem(EEPROM_address, page_start//256, bytes_page, addrsize=8)  #NB: memaddr field increments by 256 bytes so it's the 1st byte of the address
        time.sleep(time_delay)   # delay required for some reason
    print('writing done!')
    i2c.deinit()
    return checksum  # TODO: return 0 if there is an error


def read_coil_data(EEPROM_address = 0x50):

    if EEPROM_address not in EEPROM_find():
        print('read_coil_data ERROR: no EEPROM present at address', EEPROM_address, '!')
        return [], 0
 
    i2c = I2C(driver="ch341")   # tried with ", freq=100e3" but not necessary 
    i2c.init()        

    i2c.writeto_mem(EEPROM_address, 0, bytes.fromhex("00"), addrsize=8)    # dummy write to reset address counter
    read_data_length = int.from_bytes(i2c.readfrom(EEPROM_address, 4), byteorder='little')  # 1st 4 bytes of BSON are the length

    print('\nreading EEPROM at address', EEPROM_address)
    i2c.writeto_mem(EEPROM_address, 0, bytes.fromhex("00"), addrsize=8)    # dummy write to reset address counter
    read_bytes = i2c.readfrom(EEPROM_address, read_data_length)
    read_bytes_checksum = zlib.crc32(read_bytes)
    read_checksum = int.from_bytes(i2c.readfrom(EEPROM_address, 4), byteorder='big')

    if read_bytes_checksum == read_checksum:
        print('CRC32 checksum =', read_bytes_checksum, 'matches! \N{thumbs up sign}')
        #read_data = bson.loads(read_bytes)
        #read_data = read_bytes.decode()
        read_data = bson.BSON.decode(read_bytes)
        checksum = read_checksum
    else:
        print('CRC32 checksum =', read_bytes_checksum, 'DOES NOT match! \N{confused face}')
        read_data = []
        checksum = 0

    i2c.deinit()
    return read_data, checksum  # 0 if there is an error


def is_json_serializable(data):
    """
    check if somehow the dict is not formatted according to what is expected from JSON
  
    Parameters
    ----------
    data : dict 
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    """
    try:
        json.dumps(data)
        return True
    except TypeError:
        return False