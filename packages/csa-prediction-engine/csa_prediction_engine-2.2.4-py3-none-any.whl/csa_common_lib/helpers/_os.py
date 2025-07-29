import os
import crcmod
import io

from tempfile import _TemporaryFileWrapper, SpooledTemporaryFile

def is_valid_path(path:str):
    """Checks if the specified path's directoryexists and is writable.

    Parameters
    ----------
    path : str
        The file path to validate. This function checks if the directory 
        part of the path exists and is writable.

    Returns
    -------
    bool
        True if the directory exists and is writable.

    Raises
    ------
    FileNotFoundError
        If the directory in `path` does not exist.
    PermissionError
        If the directory in `path` is not writable.
    """    
    # Get the directory part of the path
    directory = os.path.dirname(path)
    
    # Check if the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    # Check if the directory is writable
    if not os.access(directory, os.W_OK):
        raise PermissionError(f"The directory '{directory}' is not writable.")

    # If no exceptions were raised, the path is valid
    return True


def is_file_path(s: str):
    """Checks to see if string passed in is for a file path that exists

    Parameters
    ----------
    s : str
        File path

    Returns
    -------
    bool
        True if s is a valid file path, False otherwise
    """    
    return os.path.isfile(s)


def is_file_obj(obj):
    """Check if object is a file object. This includes a temporary file
    wrapper and spooled temporary file buffer.

    Parameters
    ----------
    obj : _type_
        Input object to test

    Returns
    -------
    bool
        True if obj is a file object, False otherwise
    """    
    return isinstance(obj, (io.IOBase, _TemporaryFileWrapper, SpooledTemporaryFile))


def is_byte_data(obj):
    """Check if obj is bytes data

    Parameters
    ----------
    obj : 
        Input object to test

    Returns
    -------
    bool
        True if obj is byte data, False otherwise
    """    
    return isinstance(obj, bytes)


def calc_crc64(input_data):
    """Calculates the CRC64 checksum of a given file's data. We use CRC64
    because it is faster to compute than MD5 or SHA-1/256. Given tradeoffs
    between speed and risk of collisions, this is a good balance.

    Parameters
    ----------
    input_data : str or byte
        If string data, function assumes it is a path to a file and 
        calculates the checksum of the file's data. Otherwise, the 
        function assumes that input_data is bytes and calculates the
        checksum directly on input_data.

    Returns
    -------
    str
        Hex string of the CRC 64 checksum.
    """    
    
    # Define CRC64 parameters and get the function object from 
    # the library's factory function. These parameters will also
    # match 7-zip's CRC utility for testing.
    crc64 = crcmod.mkCrcFun(poly=0x142F0E1EBA9EA3693, initCrc=0, xorOut=0xFFFFFFFFFFFFFFFF)

    # open the file, read the data, and return the HEX CRC64 checksum
    data = None
    if input_data is not None:
        if is_file_obj(input_data):
            data = input_data.read() # read the file object buffer
            input_data.seek(0) # reset the file buffer pointer
            
        elif is_file_path(input_data):
            try:
                with open(input_data, 'rb') as f:
                    data = f.read()
            except IOError:
                # If not a file or some issue reading path
                data = None
                
        elif is_byte_data(input_data):
            data = input_data # assume byte data
        
    # calculate checksum    
    if data is None:
        checksum = hex(0)
    else:
        checksum = hex(crc64(data))[2:] # remove '0x' prefix
       
    # return checksum value (hex)
    return checksum